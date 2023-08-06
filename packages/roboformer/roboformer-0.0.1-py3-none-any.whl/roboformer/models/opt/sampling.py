from typing import Literal

import torch
import torch.nn.functional as F
from torch import Tensor, nn

from roboformer.models.opt.model import OPT

SamplingMode = Literal["multinomial", "greedy", "nucleus"]


def sample_step(next_logits: Tensor, mode: str, nucleus_prob: float) -> Tensor:
    """Does a single sampling step on a given set of logits.

    Args:
        next_logits: The logits to sample from, with shape (B, C)
        mode: The sampling mode to use
        nucleus_prob: Nucleus sampling probability

    Returns:
        The sampled tokens, with shape (B, 1)

    Raises:
        NotImplementedError: If the mode is invalid
    """

    if mode == "multinomial":
        return torch.multinomial(next_logits.softmax(1), num_samples=1)

    if mode == "greedy":
        return next_logits.argmax(dim=1, keepdim=True)

    if mode == "nucleus":
        probs = next_logits.softmax(dim=1)
        sorted_probs, indices = torch.sort(probs, dim=-1, descending=True)
        cumsum_probs = torch.cumsum(sorted_probs, dim=-1)
        nucleus = cumsum_probs < nucleus_prob
        nucleus = torch.cat([nucleus.new_ones(nucleus.shape[:-1] + (1,)), nucleus[..., :-1]], dim=-1)
        sorted_log_probs = torch.log(sorted_probs)
        sorted_log_probs[~nucleus] = float("-inf")
        # sampled_sorted_indices = Categorical(logits=sorted_log_probs).sample()
        probs = F.softmax(sorted_log_probs, dim=-1)
        probs_2d = probs.flatten(0, -2)
        samples_2d = torch.multinomial(probs_2d, 1, True).T
        sampled_sorted_indices = samples_2d.reshape(probs.shape[:-1]).unsqueeze(-1)
        res = indices.gather(-1, sampled_sorted_indices)
        return res

    raise NotImplementedError(f"Invalid mode: {mode}")


class Sampler(nn.Module):
    __constants__ = ["mode", "max_steps", "nucleus_prob"]

    def __init__(
        self,
        model: OPT,
        mode: SamplingMode,
        max_steps: int,
        *,
        nucleus_prob: float = 0.8,
    ) -> None:
        """Defines a wrapper module to sample from an OPT model.

        Args:
            model: The model to sample from
            mode: The sampling mode to use
            max_steps: The maximum number of steps to sample
            nucleus_prob: Nucleus sampling probability
        """

        super().__init__()

        self.model = model
        self.mode = mode
        self.max_steps = max_steps
        self.nucleus_prob = nucleus_prob

    def sample(self, prev_token: Tensor) -> Tensor:
        """Samples a sequence for a given prefix.

        Args:
            prev_token: The prefix to use, with shape (B, T)

        Returns:
            The sampled tokens, with shape (B, T)
        """

        offset = 0
        all_tokens = prev_token

        # Runs the first step to get the caches.
        next_logits, kv_caches = self.model(prev_token)
        offset += next_logits.size(2)
        prev_token = sample_step(next_logits[..., -1], self.mode, self.nucleus_prob)
        all_tokens = torch.cat((all_tokens, prev_token), dim=1)

        for _ in range(self.max_steps):
            next_logits, kv_caches = self.model(
                prev_token,
                kv_caches=kv_caches,
                offset=offset,
            )
            offset += next_logits.size(2)
            next_logits = next_logits[..., -1]
            prev_token = sample_step(next_logits, self.mode, self.nucleus_prob)
            all_tokens = torch.cat((all_tokens, prev_token), dim=1)

        return all_tokens

    def forward(self, prev_token: Tensor) -> Tensor:
        return self.sample(prev_token)
