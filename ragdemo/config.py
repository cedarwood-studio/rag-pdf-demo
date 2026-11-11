"""Settings, all read from environment variables so the container needs no config file."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    embedding_provider: str  # "fastembed" or "hash" (tests only)
    embedding_model: str
    collection: str
    top_k: int
    max_citations: int
    score_threshold: float
    strict_threshold: float
    hybrid: bool
    keyword_weight: float
    openai_api_key: str
    openai_base_url: str
    openai_model: str


def load() -> Settings:
    env = os.environ.get
    return Settings(
        database_url=env("DATABASE_URL", "postgresql://rag:rag@localhost:5432/rag"),
        embedding_provider=env("EMBEDDING_PROVIDER", "fastembed"),
        embedding_model=env("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"),
        collection=env("COLLECTION", "heading"),
        top_k=int(env("TOP_K", "5")),
        max_citations=int(env("MAX_CITATIONS", "3")),
        score_threshold=float(env("SCORE_THRESHOLD", "0.62")),
        strict_threshold=float(env("STRICT_THRESHOLD", "0.75")),
        hybrid=env("HYBRID", "0").lower() in ("1", "true", "yes"),
        keyword_weight=float(env("KEYWORD_WEIGHT", "1.0")),
        openai_api_key=env("OPENAI_API_KEY", ""),
        openai_base_url=env("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        openai_model=env("OPENAI_MODEL", "gpt-4o-mini"),
    )
