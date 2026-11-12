"""Settings, all read from environment variables so the container needs no config file."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    embedding_provider: str  # "fastembed" or "hash" (tests only)
    embedding_model: str
    corpus: str  # "core" (12 PDFs) or "full" (about 100 PDFs)
    collection: str
    top_k: int
    max_citations: int  # passages quoted by the extractive answer
    max_context: int  # passages handed to the language model
    score_threshold: float
    strict_threshold: float
    use_index: bool
    rerank: bool  # optional second-stage ranking, off by default
    rerank_model: str
    rerank_pool: int  # candidates fetched by vector search and handed to the cross-encoder
    rerank_threshold: float
    answer_mode: str  # "auto", "extractive" or "generated"
    openai_api_key: str
    openai_base_url: str
    answer_model: str
    price_input_per_m: float
    price_output_per_m: float
    max_spend_usd: float


def load() -> Settings:
    env = os.environ.get
    corpus = env("CORPUS", "core")
    return Settings(
        database_url=env("DATABASE_URL", "postgresql://rag:rag@localhost:54329/rag"),
        embedding_provider=env("EMBEDDING_PROVIDER", "fastembed"),
        embedding_model=env("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"),
        corpus=corpus,
        collection=env("COLLECTION", corpus),
        top_k=int(env("TOP_K", "5")),
        max_citations=int(env("MAX_CITATIONS", "3")),
        max_context=int(env("MAX_CONTEXT", "5")),
        score_threshold=float(env("SCORE_THRESHOLD", "0.62")),
        strict_threshold=float(env("STRICT_THRESHOLD", "0.75")),
        use_index=env("USE_INDEX", "0").lower() in ("1", "true", "yes"),
        rerank=env("RERANK", "0").lower() in ("1", "true", "yes"),
        rerank_model=env("RERANK_MODEL", "Xenova/ms-marco-MiniLM-L-6-v2"),
        rerank_pool=int(env("RERANK_POOL", "10")),
        rerank_threshold=float(env("RERANK_THRESHOLD", "-1.5")),
        answer_mode=env("ANSWER_MODE", "auto"),
        # The key is read from the environment only. It is never written to disk or logged.
        openai_api_key=env("OPENAI_API_KEY", ""),
        openai_base_url=env("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        # Any OpenAI-compatible endpoint works: set OPENAI_BASE_URL, ANSWER_MODEL and that endpoint's key in OPENAI_API_KEY.
        answer_model=env("ANSWER_MODEL", "gpt-4o-mini"),
        price_input_per_m=float(env("PRICE_INPUT_PER_M", "0.15")),
        price_output_per_m=float(env("PRICE_OUTPUT_PER_M", "0.60")),
        max_spend_usd=float(env("MAX_SPEND_USD", "0.40")),
    )
