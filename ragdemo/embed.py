"""Embedding providers behind one small interface.

The default runs a small open model on CPU through fastembed (ONNX), so the
demo needs no API key. The hash embedder exists for tests: it is deterministic,
needs no download, and matches on shared words only.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Protocol


class Embedder(Protocol):
    dim: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


class FastEmbedEmbedder:
    def __init__(self, model: str = "BAAI/bge-small-en-v1.5") -> None:
        from fastembed import TextEmbedding

        self._model = TextEmbedding(model_name=model)
        self.dim = len(next(iter(self._model.embed(["dimension probe"]))))

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # Batches are padded to their longest text, so embedding in length order wastes less CPU.
        order = sorted(range(len(texts)), key=lambda i: len(texts[i]))
        vectors = self._model.embed([texts[i] for i in order], batch_size=16)
        out: list[list[float]] = [[] for _ in texts]
        for i, vector in zip(order, vectors, strict=True):
            out[i] = vector.tolist()
        return out

    def embed_query(self, text: str) -> list[float]:
        # query_embed adds the retrieval instruction the bge models were trained with.
        return next(iter(self._model.query_embed(text))).tolist()


class HashEmbedder:
    """Bag of words hashed into a fixed number of buckets, L2 normalised."""

    STOP = frozenset("a an and are as at be by do does for from how in is it of on or that the to what when which who why with".split())

    def __init__(self, dim: int = 384) -> None:
        self.dim = dim

    def _embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        for token in re.findall(r"[a-z0-9]+", text.lower()):
            if token in self.STOP:
                continue
            bucket = int.from_bytes(hashlib.sha1(token.encode()).digest()[:4], "big") % self.dim
            vec[bucket] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


def make_embedder(provider: str, model: str) -> Embedder:
    if provider == "fastembed":
        return FastEmbedEmbedder(model)
    if provider == "hash":
        return HashEmbedder()
    raise ValueError(f"unknown embedding provider: {provider}")
