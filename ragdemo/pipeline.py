"""The whole question-to-answer path: retrieve, apply the refusal checks, answer, attach citations."""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field

from . import config
from .answer import Answerer, ExtractiveAnswerer, GeneratedAnswerer
from .embed import make_embedder
from .llm import ChatClient, Spend
from .refusal import REFUSAL, content_terms, decide, decide_reranked
from .rerank import Reranker
from .retrieval import Retriever
from .store import Hit, PgVectorStore


@dataclass
class Citation:
    document: str
    title: str
    page: int
    heading: str
    score: float
    snippet: str


@dataclass
class ChatResult:
    answer: str
    refused: bool
    mode: str
    top_score: float
    threshold: float
    citations: list[Citation] = field(default_factory=list)
    unknown_terms: list[str] = field(default_factory=list)
    rerank_score: float | None = None
    refused_by: str = ""
    retrieved: list[Hit] = field(default_factory=list)
    passages: list[Hit] = field(default_factory=list)

    def public(self) -> dict:
        data = asdict(self)
        data.pop("retrieved")
        data.pop("passages")
        return data


class Pipeline:
    def __init__(
        self,
        retriever: Retriever,
        answerer: Answerer,
        threshold: float = 0.62,
        strict_threshold: float = 0.0,
        max_citations: int = 3,
        max_context: int = 5,
        reranker: Reranker | None = None,
        rerank_threshold: float = 0.0,
        top_k: int = 5,
    ) -> None:
        self.retriever = retriever  # fetches top_k passages, or the larger rerank pool when a reranker is set
        self.answerer = answerer
        self.threshold = threshold
        # Applied in place of the threshold when the question uses a word found nowhere in the corpus. 0 turns it off.
        self.strict_threshold = strict_threshold
        self.max_citations = max_citations
        self.max_context = max_context
        self.reranker = reranker
        self.rerank_threshold = rerank_threshold
        self.top_k = top_k  # passages kept after reranking
        self.timings: dict[str, float] = {}

    @property
    def mode(self) -> str:
        return self.answerer.mode  # "extractive" or "generated"

    @property
    def collection(self) -> str:
        return self.retriever.collection

    def count(self) -> int:
        return self.retriever.store.count(self.collection)

    def chat(self, question: str) -> ChatResult:
        hits = self.retriever.retrieve(question)
        self.timings = {**self.retriever.timings, "rerank_ms": 0.0}
        unknown = []
        if self.strict_threshold > self.threshold:
            unknown = self.retriever.store.missing_terms(self.collection, content_terms(question))
        max_passages = self.max_context if self.mode == "generated" else self.max_citations
        decision = decide(hits, unknown, self.threshold, self.strict_threshold, max_passages)
        if self.reranker and not decision.refused:
            # Only questions that pass the cheap checks pay for the cross-encoder.
            start = time.perf_counter()
            hits = self.reranker.rerank(question, hits, self.top_k)
            self.timings["rerank_ms"] = (time.perf_counter() - start) * 1000
            decision = decide_reranked(decision, hits, self.rerank_threshold, self.threshold, max_passages)
        hits = hits[: self.top_k]
        d = decision
        if d.refused:
            return ChatResult(REFUSAL, True, self.mode, d.top_score, d.limit, [], unknown, d.rerank_score, d.refused_by, hits, [])
        answer = self.answerer.answer(question, d.passages)
        cited = [d.passages[i] for i in answer.cited]
        citations = [Citation(p.document, p.title, p.page, p.heading, round(p.score, 4), p.text[:240]) for p in cited]
        refused_by = "model" if answer.refused else ""
        return ChatResult(answer.text, answer.refused, self.mode, d.top_score, d.limit, citations, unknown, d.rerank_score, refused_by, hits, cited)


def build_pipeline(settings: config.Settings, spend: Spend | None = None, **overrides) -> Pipeline:
    """Wire the parts together from settings. Keyword overrides replace single settings, for the eval scripts."""
    opt = {**asdict(settings), **overrides}
    embedder = make_embedder(opt["embedding_provider"], opt["embedding_model"])
    store = PgVectorStore(opt["database_url"], embedder.dim, use_index=opt["use_index"])
    reranker = Reranker(opt["rerank_model"]) if opt["rerank"] else None
    retriever = Retriever(store, embedder, opt["collection"], opt["rerank_pool"] if reranker else opt["top_k"])
    mode = opt["answer_mode"]
    if mode == "auto":
        mode = "generated" if opt["openai_api_key"] else "extractive"
    if mode == "generated":
        spend = spend or Spend(opt["price_input_per_m"], opt["price_output_per_m"], opt["max_spend_usd"])
        answerer: Answerer = GeneratedAnswerer(ChatClient(opt["openai_api_key"], opt["openai_base_url"], opt["openai_model"], spend))
    else:
        answerer = ExtractiveAnswerer()
    return Pipeline(
        retriever,
        answerer,
        opt["score_threshold"],
        opt["strict_threshold"],
        opt["max_citations"],
        opt["max_context"],
        reranker,
        opt["rerank_threshold"],
        opt["top_k"],
    )
