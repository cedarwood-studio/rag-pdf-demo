"""FastAPI app: POST /chat, GET /health, and the chat page at /."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from . import config
from .answer import make_answerer
from .embed import make_embedder
from .pipeline import Pipeline
from .store import PgVectorStore

app = FastAPI(title="PDF question answering demo")
STATIC = Path(__file__).parent / "static"


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class CitationOut(BaseModel):
    document: str
    title: str
    page: int
    heading: str
    score: float
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    refused: bool
    mode: str
    top_score: float
    threshold: float
    unknown_terms: list[str]
    citations: list[CitationOut]


@lru_cache(maxsize=1)
def get_pipeline() -> Pipeline:
    s = config.load()
    embedder = make_embedder(s.embedding_provider, s.embedding_model)
    store = PgVectorStore(s.database_url, embedder.dim)
    answerer = make_answerer(s.openai_api_key, s.openai_base_url, s.openai_model)
    return Pipeline(store, embedder, answerer, s.collection, s.top_k, s.max_citations, s.score_threshold, s.strict_threshold, s.hybrid, s.keyword_weight)


@app.get("/health")
def health(pipeline: Pipeline = Depends(get_pipeline)) -> dict:
    return {
        "status": "ok",
        "collection": pipeline.collection,
        "chunks": pipeline.store.count(pipeline.collection),
        "answer_mode": pipeline.answerer.mode,
        "threshold": pipeline.threshold,
        "strict_threshold": pipeline.strict_threshold,
        "hybrid": pipeline.hybrid,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, pipeline: Pipeline = Depends(get_pipeline)) -> dict:
    return pipeline.chat(request.question.strip()).public()


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")
