"""FastAPI app: POST /chat, GET /health, and the chat page at /."""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, StringConstraints

from . import config
from .llm import MODEL_ERRORS, BudgetExceeded
from .pipeline import Pipeline, build_pipeline

app = FastAPI(title="PDF question answering demo")
STATIC = Path(__file__).parent / "static"
log = logging.getLogger("uvicorn.error")


class ChatRequest(BaseModel):
    question: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]


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
    return pipeline.chat(request.question).public()


@app.exception_handler(BudgetExceeded)
def spend_cap_reached(request: Request, error: BudgetExceeded) -> JSONResponse:
    """The cap counts every model call since the server started. Past it, generated answers stop until a restart."""
    return JSONResponse(status_code=503, content={"detail": f"Generated answers are switched off: {error}. Raise MAX_SPEND_USD and restart."})


def model_call_failed(request: Request, error: Exception) -> JSONResponse:
    # Only the error type is logged: the provider's message is not trusted to leave the key out.
    log.error("language model call failed: %s", type(error).__name__)
    return JSONResponse(status_code=502, content={"detail": "The language model call failed. See the server log."})


for error_type in MODEL_ERRORS:
    app.add_exception_handler(error_type, model_call_failed)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")
