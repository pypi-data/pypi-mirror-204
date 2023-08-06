#!/usr/bin/env python

import argparse
import sys
from pathlib import Path
from typing import get_args

import ml.api as ml
import torch
from transformers import GPT2Tokenizer

from roboformer.models.opt.model import OPTKey, opt
from roboformer.models.opt.sampling import Sampler, SamplingMode


def main() -> None:
    parser = argparse.ArgumentParser(description="Performs sampling from the OPT model")
    parser.add_argument("key", choices=get_args(OPTKey), help="OPT model key")
    parser.add_argument("mode", choices=get_args(SamplingMode), help="Sampling mode")
    parser.add_argument("-s", "--steps", type=int, default=32, help="Sampling steps")
    parser.add_argument("-p", "--prompt", help="Specific prompt or path to text file")
    parser.add_argument("-n", "--nucleus-prob", type=float, default=0.8)
    args = parser.parse_args()

    device = ml.AutoDevice.detect_device()  # CPU, GPU, Metal...

    tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained("facebook/opt-125m")
    model = opt(args.key, device=device.get_device(), dtype=device.get_floating_point_type())
    sampler = Sampler(
        model,
        mode=args.mode,
        max_steps=args.steps,
        nucleus_prob=args.nucleus_prob,
    )

    def print_func(s: str) -> None:
        # print(s, end="", flush=True)
        sys.stdout.buffer.write(s.encode("utf-8"))
        sys.stdout.buffer.flush()

    def sample_from_prompt(prompt: str) -> str:
        with torch.inference_mode():  # , device.autocast_context():
            prev_tokens = tokenizer(prompt, return_attention_mask=False, return_tensors="pt")["input_ids"]
            prev_tokens = prev_tokens.to(device.get_device())
            sampled_tokens = sampler(prev_tokens)
            return tokenizer.decode(sampled_tokens[0, prev_tokens.shape[1] :])

    if args.prompt is None:
        while True:
            prompt = input("Prompt: ")

            print_func(prompt)
            print_func(sample_from_prompt(prompt))
            print_func("\n")
    else:
        if Path(args.prompt).exists():
            with open(args.prompt, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
        else:
            prompt = args.prompt
        print_func(prompt)
        print_func(sample_from_prompt(prompt))
        print_func("\n")


if __name__ == "__main__":
    # python -m roboformer.models.opt.scripts.sample
    main()
