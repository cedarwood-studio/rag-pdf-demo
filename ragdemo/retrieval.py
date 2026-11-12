"""Retrieval: embed the question, search the vector store, return scored passages."""

from __future__ import annotations

import time

from .embed import Embedder
from .store import Hit, PgVectorStore


class Retriever:
    def __init__(self, store: PgVectorStore, embedder: Embedder, collection: str, top_k: int = 5) -> None:
        self.store = store
        self.embedder = embedder
        self.collection = collection
        self.top_k = top_k  # how many passages to fetch; the pipeline asks for a larger pool when it reranks
        self.timings: dict[str, float] = {}  # milliseconds spent in the last call, for the benchmark

    def retrieve(self, question: str, k: int | None = None) -> list[Hit]:
        start = time.perf_counter()
        vector = self.embedder.embed_query(question)
        embedded = time.perf_counter()
        hits = self.store.search(self.collection, vector, k or self.top_k)
        self.timings = {"embed_ms": (embedded - start) * 1000, "search_ms": (time.perf_counter() - embedded) * 1000}
        return hits
