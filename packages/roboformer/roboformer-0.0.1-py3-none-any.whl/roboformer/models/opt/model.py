import math
from contextlib import contextmanager
from functools import reduce
from pathlib import Path
from typing import (
    Callable,
    Iterator,
    List,
    Literal,
    NamedTuple,
    Optional,
    Sequence,
)

import torch
import torch.nn.functional as F
from torch import Tensor, nn

from roboformer.models.opt.utils import download_sharded_weights

OPTKey = Literal["opt_mini", "opt_125m", "opt_1.3b", "opt_2.7b", "opt_6.7b", "opt_13b", "opt_30b", "opt_66b"]
Device = torch.device | None
Dtype = torch.dtype | None


class KVCache(NamedTuple):
    """Caches the key and value for iterative decoding."""

    k: Tensor
    v: Tensor


def get_mask(tsz: int, *, device: Device = None, dtype: Dtype = None) -> Tensor:
    return torch.triu(torch.full((tsz, tsz), float("-inf"), device=device, dtype=dtype), diagonal=1)


def attention(q: Tensor, k: Tensor, v: Tensor, mask: Optional[Tensor] = None) -> tuple[Tensor, Tensor]:
    """Performs attention computation.

    Args:
        q: Query tensor with shape (B, C, Tq)
        k: Key tensor with shape (B, C, Tk)
        v: Value tensor with shape (B, C, Tk)
        mask: Optional boolean mask with shape (Tq, Tk)

    Returns:
        Attended tensor, with shape (B, C, Tq)
    """

    # return F.scaled_dot_product_attention(q, k, v, attn_mask=mask)

    kq = q @ k.transpose(-1, -2)  # (..., Tq, Tk)
    if mask is not None:
        kq = kq + mask
    attn = torch.softmax(kq, dim=-1)
    out = attn @ v  # (..., Tq, C)
    return out, attn


class ConvLayerNorm(nn.Module):
    __constants__ = ["channels", "eps", "elementwise_affine", "w_shape"]

    def __init__(
        self,
        channels: int,
        *,
        rank: int | None = None,
        eps: float = 1e-5,
        elementwise_affine: bool = True,
        device: Device = None,
        dtype: Dtype = None,
    ) -> None:
        """Implements layer norm for (B, C, T) tensors.

        Normally, layer-norm is applied from the right-most dimension, and
        expects an input tensor with shape (B, T, C). Since this implementation
        uses Conv1d instead of Linear layers for TensorRT compatibility, we need
        a separate layer norm implementation which doesn't require us to perform
        two transpose operations.

        There is a unit test that checks that this implementation is equivalent
        to `nn.LayerNorm` with the dimensions swapped:

            pytest tests/test_layer_norm.py

        Args:
            channels: The number of input and output channels
            rank: The expected rank of the input tensor; if not provided, it
                can be inferred at runtime, but providing it allows us to
                do more optimizations in TorchScript
            eps: Epsilon for making sure denominator is non-zero
            elementwise_affine: Add learnable scale after normalizing
            device: Default device for the layer weights
            dtype: Default data type for the layer weights
        """

        super().__init__()

        self.channels = channels
        self.eps = eps
        self.elementwise_affine = elementwise_affine

        if self.elementwise_affine:
            weight = torch.empty(self.channels, device=device, dtype=dtype)
            bias = torch.empty(self.channels, device=device, dtype=dtype)
            self.weight = nn.Parameter(weight)
            self.bias = nn.Parameter(bias)
        else:
            self.register_parameter("weight", None)
            self.register_parameter("bias", None)

        # At runtime, reshape the weight and bias to this shape so that they
        # broadcast correctly. If `rank` is not provided, then the shape is
        # inferred from the input tensor, but this is not TorchScript-friendly.
        self.w_shape = None if rank is None else (1, -1) + (1,) * (rank - 2)

        self.reset_parameters()

    def reset_parameters(self) -> None:
        if self.elementwise_affine:
            nn.init.ones_(self.weight)
            nn.init.zeros_(self.bias)

    def forward(self, inputs: Tensor) -> Tensor:
        mean = inputs.mean(dim=1, keepdim=True)
        var = torch.square(inputs - mean).mean(dim=1, keepdim=True)
        normalized_inputs = (inputs - mean) / (var + self.eps).sqrt()
        if self.elementwise_affine:
            if self.w_shape is None:
                w_shape = (-1,) + (1,) * (len(inputs.shape) - 2)
                weight = self.weight.unflatten(0, w_shape)
                bias = self.bias.unflatten(0, w_shape)
            else:
                weight = self.weight.view(self.w_shape)
                bias = self.bias.view(self.w_shape)
            normalized_inputs = normalized_inputs * weight + bias
        return normalized_inputs


class PositionalEmbeddings(nn.Embedding):
    __constants__ = [
        "num_embeddings",
        "embedding_dim",
        "padding_idx",
        "max_norm",
        "norm_type",
        "scale_grad_by_freq",
        "sparse",
        "magic_offset",
    ]

    def __init__(
        self,
        num_embeddings: int,
        embedding_dim: int,
        *,
        magic_offset: int = 2,
        device: Device = None,
        dtype: Dtype = None,
    ) -> None:
        self.magic_offset = magic_offset

        super().__init__(num_embeddings, embedding_dim, device=device, dtype=dtype)

        self.register_buffer(
            "positions",
            torch.arange(num_embeddings, device=device),
            persistent=False,
        )

    def forward(  # pylint: disable=arguments-renamed
        self,
        token_embedding: Tensor,
        offset: int = 0,
    ) -> Tensor:
        _, tsz, _ = token_embedding.shape

        position_embedding = F.embedding(
            input=self.positions[None, :tsz] + (offset + self.magic_offset),  # type: ignore
            weight=self.weight,
            padding_idx=self.padding_idx,
            max_norm=self.max_norm,
            norm_type=self.norm_type,
            scale_grad_by_freq=self.scale_grad_by_freq,
            sparse=self.sparse,
        )

        return position_embedding + token_embedding


class FullyConnected(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        *,
        use_relu: bool = True,
        use_norm: bool = True,
        bias: bool = True,
        device: Device = None,
        dtype: Dtype = None,
    ) -> None:
        """Defines a 1D convolution layer, with layer norm and activation.

        Args:
            in_channels: Number of input channels
            out_channels: Number of output channels
            bias: Should the layer use bias
            use_relu: Should the layer use ReLU activation
            use_norm: Should the layer use layer norm
            device: Default device for the layer weights
            dtype: Default data type for the layer weights
        """

        super().__init__()

        self.conv = nn.Conv1d(
            in_channels,
            out_channels,
            1,
            bias=bias,
            device=device,
            dtype=dtype,
        )
        self.norm = ConvLayerNorm(out_channels, rank=3) if use_norm else nn.Identity()
        self.act = nn.ReLU(inplace=True) if use_relu else nn.Identity()

    def forward(self, x: Tensor) -> Tensor:
        """Applies the fully connected layer.

        Args:
            x: Float tensor with shape (B, in_channels, T), with B and T arbitrary

        Returns:
            Float tensor with shape (B, out_channels, T)
        """

        x = self.conv(x)
        x = self.norm(x)
        x = self.act(x)
        return x


@contextmanager
def init_meta_weights(include_buffers: bool = False) -> Iterator[None]:
    """Avoid instantiating weights when initializing a model.

    A context manager under which models are initialized with all parameters on
    the meta device, therefore creating an empty model. Useful when just
    initializing the model would blow the available RAM.

    Args:
        include_buffers: Whether or not to also put all buffers on the meta
            device while initializing.

    Yields:
        An empty context manager
    """

    old_register_parameter = nn.Module.register_parameter
    if include_buffers:
        old_register_buffer = nn.Module.register_buffer

    def register_empty_parameter(
        module: nn.Module,
        name: str,
        param: nn.Parameter | None,
    ) -> None:
        old_register_parameter(module, name, param)
        if param is not None:
            param_cls = type(module._parameters[name])
            kwargs = module._parameters[name].__dict__
            meta_param = module._parameters[name].to(torch.device("meta"))  # type: ignore
            module._parameters[name] = param_cls(meta_param, **kwargs)  # type: ignore

    def register_empty_buffer(
        module: nn.Module,
        name: str,
        buffer: Tensor | None,
    ) -> None:
        old_register_buffer(module, name, buffer)
        if buffer is not None:
            module._buffers[name] = module._buffers[name].to(torch.device("meta"))  # type: ignore

    try:
        nn.Module.register_parameter = register_empty_parameter  # type: ignore
        if include_buffers:
            nn.Module.register_buffer = register_empty_buffer  # type: ignore
        yield
    finally:
        nn.Module.register_parameter = old_register_parameter  # type: ignore
        if include_buffers:
            nn.Module.register_buffer = old_register_buffer  # type: ignore


def meta_to_empty_func(device: Device, dtype: Dtype) -> Callable[[Tensor], Tensor]:
    def _func(t: Tensor) -> Tensor:
        if not t.is_meta:
            return t
        return torch.empty(
            t.shape,
            device=device,
            dtype=dtype if t.is_floating_point() else None,
        )

    return _func


class Projection(nn.Module):
    __constants__ = ["channels"]

    def __init__(
        self,
        channels: int,
        *,
        mult: int = 4,
        device: Device = None,
        dtype: Dtype = None,
        parallel_rank: int = 0,
        parallel_world_size: int = 1,
    ) -> None:
        """Implements a projection layer that goes after the attention layer.

        Input:
            Float tensor with shape (B, channels, T), with B and T arbitrary

        Output:
            Float tensor with the same shape as the input tensor

        Args:
            channels: The number of input and output channels
            mult: The multiplier for the channel dimension
            device: A default parameter device
            dtype: The default parameter dtype
            parallel_rank: For model parallelism, this layer's rank
            parallel_world_size: For model parallelism, the total world size

        Raises:
            ValueError: If the parallel world size is invalid for the given
                number of projection dimensions
        """

        super().__init__()

        if (projection_dims := (channels * mult)) % parallel_world_size != 0:
            raise ValueError(f"Cannot divide {projection_dims=} among {parallel_world_size=}")

        self.channels = channels

        self.norm_in = ConvLayerNorm(
            channels=channels,
            rank=3,
            device=device,
            dtype=dtype,
        )

        self.in_mlp = FullyConnected(
            in_channels=channels,
            out_channels=projection_dims // parallel_world_size,
            use_norm=False,
            bias=True,
            device=device,
            dtype=dtype,
        )

        self.out_mlp = FullyConnected(
            in_channels=projection_dims // parallel_world_size,
            out_channels=channels,
            bias=parallel_rank == 0,
            use_relu=False,
            use_norm=False,
            device=device,
            dtype=dtype,
        )

    def forward(self, x: Tensor) -> Tensor:
        h = self.norm_in(x)
        h = self.in_mlp(h)
        h = self.out_mlp(h)
        return h


class SelfAttention(nn.Module):
    __constants__ = ["channels", "norm_factor", "num_heads", "num_parallel_heads", "hidden_channels"]

    def __init__(
        self,
        channels: int,
        num_heads: int,
        *,
        hidden_channels: int | None = None,
        device: Device = None,
        dtype: Dtype = None,
        parallel_rank: int = 0,
        parallel_world_size: int = 1,
    ) -> None:
        """Creates a layer for performing self-attention.

        The parallel rank and world size are for OPT compatibility; in order
        to match the original OPT behavior, we can only use bias on parallel
        rank 0. Also, the other parameters to this module are for the entire
        parallel model; the parallel rank and world size parameters are used
        to compute what the parameters should be for the model running on
        each rank.

        Args:
            channels: The number of input and output channels
            num_heads: Total number of attention heads
            hidden_channels: Number of channels to use for the attention layer,
                if different from the number of input / output channels
            device: The default device for weights
            dtype: The default dtype for weights
            parallel_rank: For model parallelism, this layer's rank
            parallel_world_size: For model parallelism, the total world size

        Raises:
            ValueError: If some combination of parameters is invalid
        """

        super().__init__()

        self.hidden_channels = channels if hidden_channels is None else hidden_channels
        if self.hidden_channels % num_heads != 0:
            msg = f"Cannot divide {self.hidden_channels=} among {num_heads=}"
            raise ValueError(msg)
        if num_heads % parallel_world_size != 0:
            msg = f"Cannot divide {num_heads=} among {parallel_world_size=}"
            raise ValueError(msg)

        self.channels = channels
        self.norm_factor = math.sqrt(self.hidden_channels // num_heads)
        self.num_heads = num_heads
        self.num_parallel_heads = num_heads // parallel_world_size

        self.norm_in = ConvLayerNorm(
            channels=channels,
            rank=3,
            device=device,
            dtype=dtype,
        )

        self.in_proj = FullyConnected(
            in_channels=self.channels,
            out_channels=(self.hidden_channels // parallel_world_size) * 3,
            use_norm=False,
            device=device,
            dtype=dtype,
        )

        self.out_proj = FullyConnected(
            in_channels=(self.hidden_channels // parallel_world_size),
            out_channels=self.channels,
            bias=parallel_rank == 0,
            use_relu=False,
            use_norm=False,
            device=device,
            dtype=dtype,
        )

    def forward(
        self,
        x: Tensor,
        kv_cache: Optional[KVCache] = None,
        mask: Optional[Tensor] = None,
    ) -> tuple[Tensor, KVCache]:
        """Runs the self attention layer for one decoding step.

        Args:
            x: The input tensor, with shape (B, C, Tq)
            kv_cache: The key-value cache tensors; the cached key and value
                are both float tensors with shape (B, H, Tk, C / H)
            mask: An optional self-attention mask, with shape (Tq, Tk)

        Returns:
            The attended tensor, with shape (B, C, Tq), and the new cache, with
            the new key and value having shape (B, H, Tk + 1, C / H)
        """

        x = self.norm_in(x)
        # (3 * H, C / H)
        qkv_shape = (
            3 * self.num_parallel_heads,
            self.hidden_channels // self.num_heads,
        )
        # (B, C, T) -> (B, 3 * H, T, C / H)
        qkv = self.in_proj(x).unflatten(1, qkv_shape).transpose(2, 3)
        # 3 * (B, H, T, C / H)
        k, v, q = qkv.chunk(3, dim=1)
        q = q / self.norm_factor
        if kv_cache is not None:
            k = torch.cat((kv_cache.k, k), dim=2)
            v = torch.cat((kv_cache.v, v), dim=2)
        out, _ = attention(q, k, v, mask)
        # (B, H, T, C / H) -> (B, C, T)
        out = out.transpose(2, 3).flatten(1, 2)
        out = self.out_proj(out)
        return out, KVCache(k=k, v=v)


class SelfAttentionStack(nn.Module):
    def __init__(
        self,
        channels: int,
        num_heads: int,
        num_layers: int,
        *,
        hidden_channels: int | None = None,
        mult: int = 4,
        device: Device = None,
        dtype: Dtype = None,
    ) -> None:
        """Defines a stack of self attention layers.

        Args:
            channels: The number of input and output channels
            num_heads: Total number of attention heads
            num_layers: Number of self-attention layers
            hidden_channels: Number of channels to use for the attention layer,
                if different from the number of input / output channels
            mult: The multiplier for the channel dimension
            device: The default device for weights
            dtype: The default dtype for weights
        """

        super().__init__()

        self.attns: list[SelfAttention] = nn.ModuleList(  # type: ignore
            [
                SelfAttention(
                    channels=channels,
                    num_heads=num_heads,
                    hidden_channels=hidden_channels,
                    device=device,
                    dtype=dtype,
                )
                for _ in range(num_layers)
            ]
        )

        self.projs: list[Projection] = nn.ModuleList(  # type: ignore
            [
                Projection(
                    channels=channels,
                    mult=mult,
                    device=device,
                    dtype=dtype,
                )
                for _ in range(num_layers)
            ]
        )

    def forward(
        self,
        x: Tensor,
        kv_caches: Optional[List[KVCache]] = None,
        mask: Optional[Tensor] = None,
    ) -> tuple[Tensor, List[KVCache]]:
        """Runs the self attention block for one decoding step.

        Args:
            x: The input tensor, with shape (B, C, T)
            kv_caches: The key-value caches
            mask: The self-attention mask to use

        Returns:
            The attended tensor, with shape (B, C, T), and the new caches
        """

        kv_caches_out: List[KVCache] = []
        for i, (attn, proj) in enumerate(zip(self.attns, self.projs)):
            kv_cache = None if kv_caches is None else kv_caches[i]
            x_attn, kv_cache_out = attn(x, kv_cache=kv_cache, mask=mask)
            kv_caches_out.append(kv_cache_out)
            x_attn = x_attn + x
            x = proj(x_attn) + x_attn
        return x, kv_caches_out


def weight_init(module: nn.Module) -> None:
    if isinstance(module, nn.Conv1d):
        torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
        if module.bias is not None:
            torch.nn.init.zeros_(module.bias)
    elif isinstance(module, nn.Embedding):
        torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
    elif isinstance(module, ConvLayerNorm) and module.elementwise_affine:
        torch.nn.init.zeros_(module.bias)
        torch.nn.init.ones_(module.weight)


class OPT(nn.Module):
    __constants__ = [
        "vocab_size",
        "hidden_size",
        "max_position_embeddings",
        "num_attn_heads",
        "num_layers",
        "mult",
    ]

    def __init__(
        self,
        vocab_size: int,
        hidden_size: int,
        max_position_embeddings: int,
        num_attn_heads: int,
        num_layers: int,
        *,
        sharded_weight_urls: list[str] | None = None,
        mult: int = 4,
        device: Device = None,
        dtype: Dtype = None,
        keep_meta: bool = False,
    ) -> None:
        super().__init__()

        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.max_position_embeddings = max_position_embeddings
        self.num_attn_heads = num_attn_heads
        self.num_layers = num_layers
        self.mult = mult

        with init_meta_weights():
            self.pos_emb = PositionalEmbeddings(
                num_embeddings=max_position_embeddings,
                embedding_dim=hidden_size,
            )

            self.tok_emb = nn.Embedding(
                num_embeddings=vocab_size,
                embedding_dim=hidden_size,
            )

            self.self_attn = SelfAttentionStack(
                channels=hidden_size,
                num_heads=num_attn_heads,
                num_layers=num_layers,
                mult=mult,
            )

            self.final_layernorm = ConvLayerNorm(channels=hidden_size)

            self.logits_out = nn.Conv1d(
                in_channels=hidden_size,
                out_channels=vocab_size,
                kernel_size=1,
                bias=False,
            )

        mask = get_mask(max_position_embeddings)
        self.register_buffer("attention_mask", mask, persistent=False)

        # Optionally, keep the module weights as meta tensors, which can be useful
        # for unit tests where we don't want to load the entire model.
        if keep_meta:
            return

        self._apply(meta_to_empty_func(device, dtype))
        if sharded_weight_urls is None:
            self.reset_parameters()
        else:
            shard_paths = download_sharded_weights(sharded_weight_urls)
            load_sharded_weights(self, shard_paths, device=device, dtype=dtype)

        # Move remaining buffers over to the device.
        self._apply(lambda t: t if t.device == device else t.to(device))

    def reset_parameters(self) -> None:
        self.apply(weight_init)

    def forward(
        self,
        cond_tokens: Tensor,
        kv_caches: Optional[List[KVCache]] = None,
        offset: int = 0,
    ) -> tuple[Tensor, List[KVCache]]:
        """Runs the decoding pass of the OPT model.

        Args:
            cond_tokens: The token or tokens to condition on, with shape (B, T)
            kv_caches: The optional key-value caches
            offset: The positional embedding offset

        Returns:
            The sequence of predicted next token logits, and the caches
        """

        tsz = cond_tokens.shape[1] + offset
        assert tsz <= self.max_position_embeddings
        attention_mask = self.attention_mask[offset:tsz, offset:tsz] if kv_caches is None else None  # type: ignore
        x = self.tok_emb(cond_tokens)
        x = self.pos_emb(x, offset=offset)
        x = x.transpose(1, 2)
        x, kv_caches_out = self.self_attn(x, kv_caches=kv_caches, mask=attention_mask)
        x = self.final_layernorm(x)
        x = self.logits_out(x)
        return x, kv_caches_out


def load_sharded_weights(
    model: OPT,
    shard_paths: list[Path],
    *,
    device: Device = None,
    dtype: Dtype = None,
) -> None:
    """Loads sharded OPT weights.

    Args:
        model: The model to load weights for
        shard_paths: Paths to where the shards are downloaded
        device: The device to load weights to
        dtype: The data type to load weights to
    """

    num_shards = len(shard_paths)

    ffn_dim = model.hidden_size * model.mult
    vocab_size_per_shard = model.vocab_size // num_shards
    heads_per_shard = model.num_attn_heads // num_shards
    hidden_size_per_shard = model.hidden_size // num_shards
    ffn_dim_per_shard = ffn_dim // num_shards

    class ShardLoader:
        def __init__(self, flat_params: Tensor) -> None:
            self.flat_params = flat_params

        def take_out_(self, shape: Sequence[int]) -> Tensor:
            sp = int(reduce(lambda a, b: a * b, shape))
            tensor = self.flat_params[:sp].view(*shape).to(device, dtype)
            self.flat_params = self.flat_params[sp:]
            return tensor

        def load_(self, weight: Tensor, skip: bool = False) -> None:
            data = weight.data
            new_data = self.take_out_(data.shape)
            if not skip:
                data.copy_(new_data, non_blocking=True)

        def is_empty(self) -> bool:
            return self.flat_params.numel() == 0

    for shard_i, shard_path in enumerate(shard_paths):
        ckpt = torch.load(shard_path, map_location="cpu")

        def get_slice(s: int) -> slice:
            start, end = shard_i, shard_i + 1  # pylint: disable=cell-var-from-loop
            return slice(s * start, s * end)

        is_125m = ffn_dim == 3072
        if is_125m:  # Specific to 125m model
            flat_params = ckpt["model"]["flat_param_0"]
        else:
            flat_params = torch.cat([v.flatten() for k, v in ckpt["model"].items() if k != "decoder.version"])

        loader = ShardLoader(flat_params)

        # Loads vocabulary embeddings.
        emb_slice = get_slice(vocab_size_per_shard)
        tok_emb, logits_out = model.tok_emb.weight, model.logits_out.weight
        loader.load_(tok_emb[emb_slice])
        logits_out.data[emb_slice].copy_(tok_emb[emb_slice].unsqueeze(-1).data)

        # Loads positional embeddings.
        loader.load_(model.pos_emb.weight, skip=shard_i != 0)

        if not is_125m:
            loader.load_(model.final_layernorm.weight, skip=shard_i != 0)
            loader.load_(model.final_layernorm.bias, skip=shard_i != 0)

        for layer_i in range(model.num_layers):
            attn = model.self_attn.attns[layer_i]
            proj = model.self_attn.projs[layer_i]

            attn_norm_in_w, attn_norm_in_b = attn.norm_in.weight, attn.norm_in.bias
            attn_in_w, attn_in_b = attn.in_proj.conv.weight, attn.in_proj.conv.bias
            attn_out_w, attn_out_b = attn.out_proj.conv.weight, attn.out_proj.conv.bias
            proj_norm_in_w, proj_norm_in_b = proj.norm_in.weight, proj.norm_in.bias
            proj_in_w, proj_in_b = proj.in_mlp.conv.weight, proj.in_mlp.conv.bias
            proj_out_w, proj_out_b = proj.out_mlp.conv.weight, proj.out_mlp.conv.bias

            # Loads the K / V / Q weights.
            attn_in_w = attn_in_w.unflatten(0, (3, model.num_attn_heads, -1))
            loader.load_(attn_in_w[0, get_slice(heads_per_shard)])
            loader.load_(attn_in_w[1, get_slice(heads_per_shard)])
            loader.load_(attn_in_w[2, get_slice(heads_per_shard)])

            # Loads the K / V / Q biases.
            attn_in_b = attn_in_b.unflatten(0, (3, -1))  # type: ignore
            loader.load_(attn_in_b[0, get_slice(hidden_size_per_shard)])
            loader.load_(attn_in_b[1, get_slice(hidden_size_per_shard)])
            loader.load_(attn_in_b[2, get_slice(hidden_size_per_shard)])

            # Loads the output projection.
            attn_out_w = attn_out_w.unflatten(1, (model.num_attn_heads, -1))
            loader.load_(attn_out_w[:, get_slice(heads_per_shard)])
            loader.load_(attn_out_b, skip=shard_i != 0)  # type: ignore

            # Loads the attention input layer norm.
            loader.load_(attn_norm_in_w, skip=shard_i != 0)
            loader.load_(attn_norm_in_b, skip=shard_i != 0)

            # Loads the projection input MLP.
            loader.load_(proj_in_w[get_slice(ffn_dim_per_shard)])
            loader.load_(proj_in_b[get_slice(ffn_dim_per_shard)])  # type: ignore

            # Loads the projection output MLP.
            loader.load_(proj_out_w[:, get_slice(ffn_dim_per_shard)])
            loader.load_(proj_out_b, skip=shard_i != 0)  # type: ignore

            # Loads the projection input layer norm.
            loader.load_(proj_norm_in_w, skip=shard_i != 0)
            loader.load_(proj_norm_in_b, skip=shard_i != 0)

        if is_125m:
            loader.load_(model.final_layernorm.weight, skip=shard_i != 0)
            loader.load_(model.final_layernorm.bias, skip=shard_i != 0)

        assert loader.is_empty()


def opt(
    key: OPTKey,
    *,
    device: Device = None,
    dtype: Dtype = None,
    keep_meta: bool = False,
) -> OPT:
    """Returns a pre-trained OPT model.

    Args:
        key: The OPT model key
        device: The default device for the model
        dtype: The default data type for the model
        keep_meta: If set, keep the model's parameters as meta tensors

    Returns:
        The constructed OPT model

    Raises:
        NotImplementedError: If the key is invalid
    """

    if key == "opt_mini":
        return OPT(
            vocab_size=50_272,
            hidden_size=128,
            max_position_embeddings=128,
            num_attn_heads=2,
            num_layers=2,
            device=device,
            dtype=dtype,
            keep_meta=keep_meta,
        )
    if key == "opt_125m":
        return OPT(
            vocab_size=50_272,
            hidden_size=768,
            max_position_embeddings=2050,
            num_attn_heads=12,
            num_layers=12,
            sharded_weight_urls=[
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/125m/reshard-model_part-0.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/125m/reshard-model_part-1.pt",
            ],
            device=device,
            dtype=dtype,
            keep_meta=keep_meta,
        )
    if key == "opt_1.3b":
        return OPT(
            vocab_size=50_272,
            hidden_size=2048,
            max_position_embeddings=2050,
            num_attn_heads=32,
            num_layers=24,
            sharded_weight_urls=[
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/1.3b/reshard-model_part-0.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/1.3b/reshard-model_part-1.pt",
            ],
            device=device,
            dtype=dtype,
            keep_meta=keep_meta,
        )
    if key == "opt_2.7b":
        return OPT(
            vocab_size=50_272,
            hidden_size=2560,
            max_position_embeddings=2050,
            num_attn_heads=32,
            num_layers=32,
            sharded_weight_urls=[
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/2.7b/reshard-model_part-0.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/2.7b/reshard-model_part-1.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/2.7b/reshard-model_part-2.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/2.7b/reshard-model_part-3.pt",
            ],
            device=device,
            dtype=dtype,
            keep_meta=keep_meta,
        )
    if key == "opt_6.7b":
        return OPT(
            vocab_size=50_272,
            hidden_size=4096,
            max_position_embeddings=2050,
            num_attn_heads=32,
            num_layers=32,
            sharded_weight_urls=[
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/6.7b/reshard-model_part-0.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/6.7b/reshard-model_part-1.pt",
            ],
            device=device,
            dtype=dtype,
            keep_meta=keep_meta,
        )
    if key == "opt_13b":
        return OPT(
            vocab_size=50_272,
            hidden_size=5120,
            max_position_embeddings=2050,
            num_attn_heads=40,
            num_layers=40,
            sharded_weight_urls=[
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/13b/reshard-model_part-0.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/13b/reshard-model_part-1.pt",
            ],
            device=device,
            dtype=dtype,
            keep_meta=keep_meta,
        )
    if key == "opt_30b":
        return OPT(
            vocab_size=50_272,
            hidden_size=7168,
            max_position_embeddings=2050,
            num_attn_heads=56,
            num_layers=48,
            sharded_weight_urls=[
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/30b/reshard-model_part-0.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/30b/reshard-model_part-1.pt",
            ],
            device=device,
            dtype=dtype,
            keep_meta=keep_meta,
        )
    if key == "opt_66b":
        return OPT(
            vocab_size=50_272,
            hidden_size=9216,
            max_position_embeddings=2050,
            num_attn_heads=72,
            num_layers=64,
            sharded_weight_urls=[
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/66b/reshard-model_part-0-shard0.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/66b/reshard-model_part-0-shard1.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/66b/reshard-model_part-0-shard2.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/66b/reshard-model_part-0-shard3.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/66b/reshard-model_part-0-shard4.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/66b/reshard-model_part-0-shard5.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/66b/reshard-model_part-0-shard6.pt",
                "https://dl.fbaipublicfiles.com/opt/v1_20220502/66b/reshard-model_part-0-shard7.pt",
            ],
            device=device,
            dtype=dtype,
            keep_meta=keep_meta,
        )

    raise NotImplementedError(f"Invalid OPT model: {key}")
