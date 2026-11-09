"""Train TinyNexusLM from random weights using an authorized plain-text corpus."""
from __future__ import annotations
import argparse
import json
import random
from pathlib import Path
import torch
from model import TinyNexusLM

def get_batch(data: torch.Tensor, batch_size: int, block_size: int, device: torch.device):
    if len(data) <= block_size + 1:
        raise ValueError("Corpus is too small for the selected block_size.")
    starts = torch.randint(0, len(data) - block_size - 1, (batch_size,))
    x = torch.stack([data[i : i + block_size] for i in starts])
    y = torch.stack([data[i + 1 : i + block_size + 1] for i in starts])
    return x.to(device), y.to(device)

@torch.no_grad()
def estimate_loss(model, train_data, val_data, args, device):
    model.eval()
    result = {}
    for name, data in (("train", train_data), ("validation", val_data)):
        losses = []
        for _ in range(args.eval_batches):
            x, y = get_batch(data, args.batch_size, args.block_size, device)
            _, loss = model(x, y)
            losses.append(loss.item())
        result[name] = sum(losses) / len(losses)
    model.train()
    return result

def main():
    parser = argparse.ArgumentParser(description="Train a tiny NEXUS language model from scratch.")
    parser.add_argument("--data", default="training/from_scratch/corpus.txt")
    parser.add_argument("--output", default="artifacts/nexus-tiny.pt")
    parser.add_argument("--steps", type=int, default=2000)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--block-size", type=int, default=128)
    parser.add_argument("--width", type=int, default=128)
    parser.add_argument("--heads", type=int, default=4)
    parser.add_argument("--layers", type=int, default=2)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--eval-every", type=int, default=200)
    parser.add_argument("--eval-batches", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    corpus_path = Path(args.data)
    if not corpus_path.exists():
        raise SystemExit(f"Corpus absent: {corpus_path}. Create it from texts you own or are licensed to use.")
    text = corpus_path.read_text(encoding="utf-8")
    if len(text) < 1000:
        raise SystemExit("Corpus trop court : ajoute au moins 1 000 caractères pour ce prototype.")
    chars = sorted(set(text))
    stoi = {ch: i for i, ch in enumerate(chars)}
    encoded = torch.tensor([stoi[ch] for ch in text], dtype=torch.long)
    split = int(0.9 * len(encoded))
    train_data, val_data = encoded[:split], encoded[split:]
    if len(val_data) <= args.block_size + 1:
        raise SystemExit("Partie validation trop courte : ajoute davantage de texte.")
    model = TinyNexusLM(vocab_size=len(chars), block_size=args.block_size, width=args.width, heads=args.heads, layers=args.layers, dropout=args.dropout).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    print(f"Device: {device}; vocab: {len(chars)}; parameters: {sum(p.numel() for p in model.parameters()):,}")
    print("Initialization: random weights; no pretrained checkpoint and no external model API.")
    for step in range(1, args.steps + 1):
        x, y = get_batch(train_data, args.batch_size, args.block_size, device)
        _, loss = model(x, y)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        if step == 1 or step % args.eval_every == 0 or step == args.steps:
            print(json.dumps({"step": step, **estimate_loss(model, train_data, val_data, args, device)}, ensure_ascii=False))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state": model.state_dict(), "vocab": chars, "config": {"vocab_size": len(chars), "block_size": args.block_size, "width": args.width, "heads": args.heads, "layers": args.layers, "dropout": args.dropout}, "training": {"steps": args.steps, "seed": args.seed, "corpus": str(corpus_path)}}, output)
    print(f"Checkpoint saved: {output}")

if __name__ == "__main__":
    main()
