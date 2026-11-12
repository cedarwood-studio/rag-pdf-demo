"""FastAPI app: POST /chat, GET /health, and the chat page at /."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from . import config
from .pipeline import Pipeline, build_pipeline

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
    rerank_score: float | None
    refused_by: str
    citations: list[CitationOut]


@lru_cache(maxsize=1)
def get_pipeline() -> Pipeline:
    return build_pipeline(config.load())


@app.get("/health")
def health(pipeline: Pipeline = Depends(get_pipeline)) -> dict:
    return {
        "status": "ok",
        "collection": pipeline.collection,
        "chunks": pipeline.count(),
        "answer_mode": pipeline.mode,
        "threshold": pipeline.threshold,
        "strict_threshold": pipeline.strict_threshold,
        "rerank": pipeline.reranker is not None,
        "rerank_threshold": pipeline.rerank_threshold,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, pipeline: Pipeline = Depends(get_pipeline)) -> dict:
    return pipeline.chat(request.question.strip()).public()


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")
