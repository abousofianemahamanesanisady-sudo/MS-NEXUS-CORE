"""Generate text from a checkpoint created by train.py."""
from __future__ import annotations
import argparse
import torch
from model import TinyNexusLM

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="artifacts/nexus-tiny.pt")
    parser.add_argument("--prompt", default="MS NEXUS")
    parser.add_argument("--tokens", type=int, default=300)
    args = parser.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(args.checkpoint, map_location=device, weights_only=False)
    vocab = checkpoint["vocab"]
    stoi = {ch: i for i, ch in enumerate(vocab)}
    unknown = sorted(set(args.prompt) - set(stoi))
    if unknown:
        raise SystemExit(f"Prompt contains characters absent from training corpus: {unknown!r}")
    config = checkpoint["config"]
    model = TinyNexusLM(**config).to(device)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()
    tokens = torch.tensor([[stoi[ch] for ch in args.prompt]], dtype=torch.long, device=device)
    generated = list(args.prompt)
    with torch.no_grad():
        for _ in range(args.tokens):
            context = tokens[:, -config["block_size"] :]
            logits, _ = model(context)
            probabilities = torch.softmax(logits[:, -1, :], dim=-1)
            next_token = torch.multinomial(probabilities, num_samples=1)
            tokens = torch.cat((tokens, next_token), dim=1)
            generated.append(vocab[next_token.item()])
    print("".join(generated))

if __name__ == "__main__":
    main()
