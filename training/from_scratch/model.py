"""Small decoder-only Transformer. All parameters start from random initialization."""
from __future__ import annotations
import torch
from torch import nn
from torch.nn import functional as F

class CausalSelfAttention(nn.Module):
    def __init__(self, width: int, heads: int, block_size: int, dropout: float):
        super().__init__()
        if width % heads:
            raise ValueError("width must be divisible by heads")
        self.heads = heads
        self.head_dim = width // heads
        self.qkv = nn.Linear(width, 3 * width)
        self.proj = nn.Linear(width, width)
        self.attn_dropout = nn.Dropout(dropout)
        self.resid_dropout = nn.Dropout(dropout)
        self.register_buffer("mask", torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, length, width = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        shape = (batch, length, self.heads, self.head_dim)
        q = q.view(shape).transpose(1, 2)
        k = k.view(shape).transpose(1, 2)
        v = v.view(shape).transpose(1, 2)
        scores = (q @ k.transpose(-2, -1)) * (self.head_dim ** -0.5)
        scores = scores.masked_fill(self.mask[:, :, :length, :length] == 0, float("-inf"))
        weights = self.attn_dropout(F.softmax(scores, dim=-1))
        out = (weights @ v).transpose(1, 2).contiguous().view(batch, length, width)
        return self.resid_dropout(self.proj(out))

class TransformerBlock(nn.Module):
    def __init__(self, width: int, heads: int, block_size: int, dropout: float):
        super().__init__()
        self.norm1 = nn.LayerNorm(width)
        self.attn = CausalSelfAttention(width, heads, block_size, dropout)
        self.norm2 = nn.LayerNorm(width)
        self.mlp = nn.Sequential(nn.Linear(width, 4 * width), nn.GELU(), nn.Linear(4 * width, width), nn.Dropout(dropout))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.norm1(x))
        return x + self.mlp(self.norm2(x))

class TinyNexusLM(nn.Module):
    """Character-level language model; educational first baseline."""
    def __init__(self, vocab_size: int, block_size: int = 128, width: int = 128, heads: int = 4, layers: int = 2, dropout: float = 0.1):
        super().__init__()
        self.block_size = block_size
        self.token_embedding = nn.Embedding(vocab_size, width)
        self.position_embedding = nn.Embedding(block_size, width)
        self.blocks = nn.Sequential(*[TransformerBlock(width, heads, block_size, dropout) for _ in range(layers)])
        self.norm = nn.LayerNorm(width)
        self.lm_head = nn.Linear(width, vocab_size, bias=False)
        self.lm_head.weight = self.token_embedding.weight
        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, tokens: torch.Tensor, targets: torch.Tensor | None = None):
        batch, length = tokens.shape
        if length > self.block_size:
            raise ValueError(f"Sequence length {length} exceeds block_size={self.block_size}")
        positions = torch.arange(length, device=tokens.device)
        x = self.token_embedding(tokens) + self.position_embedding(positions)[None, :, :]
        logits = self.lm_head(self.norm(self.blocks(x)))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        return logits, loss
