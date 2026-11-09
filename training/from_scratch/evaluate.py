"""Evaluate a from-scratch checkpoint on a held-out corpus split."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import torch
from model import TinyNexusLM


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="training/from_scratch/corpus.txt")
    parser.add_argument("--checkpoint", default="artifacts/nexus-tiny.pt")
    parser.add_argument("--batches", type=int, default=64)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.batches < 1:
        raise SystemExit("--batches must be at least 1")

    corpus_path = Path(args.data)
    checkpoint_path = Path(args.checkpoint)
    if not corpus_path.is_file():
        raise SystemExit(f"Corpus absent: {corpus_path}")
    if not checkpoint_path.is_file():
        raise SystemExit(f"Checkpoint absent: {checkpoint_path}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=True)
    vocab = checkpoint["vocab"]
    config = checkpoint["config"]
    text = corpus_path.read_text(encoding="utf-8")
    unknown = sorted(set(text) - set(vocab))
    if unknown:
        raise SystemExit(f"Corpus contains characters absent from checkpoint vocabulary: {unknown!r}")

    stoi = {char: index for index, char in enumerate(vocab)}
    encoded = torch.tensor([stoi[char] for char in text], dtype=torch.long)
    split = int(0.9 * len(encoded))
    train_data, val_data = encoded[:split], encoded[split:]
    block_size = int(config["block_size"])
    batch_size = 16
    if len(val_data) <= block_size + 1:
        raise SystemExit("Validation split is too short for this checkpoint.")

    model = TinyNexusLM(**config).to(device)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    torch.manual_seed(args.seed)

    @torch.no_grad()
    def average_loss(source: torch.Tensor) -> float:
        losses = []
        for _ in range(args.batches):
            starts = torch.randint(0, len(source) - block_size - 1, (batch_size,))
            x = torch.stack([source[i : i + block_size] for i in starts]).to(device)
            y = torch.stack([source[i + 1 : i + block_size + 1] for i in starts]).to(device)
            _, loss = model(x, y)
            losses.append(float(loss.item()))
        return sum(losses) / len(losses)

    result = {
        "device": str(device),
        "corpus_characters": len(text),
        "vocabulary_characters": len(vocab),
        "checkpoint_parameters": sum(parameter.numel() for parameter in model.parameters()),
        "evaluation_batches": args.batches,
        "train_cross_entropy": round(average_loss(train_data), 6),
        "validation_cross_entropy": round(average_loss(val_data), 6),
        "uniform_random_baseline_cross_entropy": round(math.log(len(vocab)), 6),
        "checkpoint_bytes": checkpoint_path.stat().st_size,
        "checkpoint_sha256": hashlib.sha256(checkpoint_path.read_bytes()).hexdigest(),
        "initialization": "random_weights",
        "pretrained_weights": False,
        "external_model_api": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
