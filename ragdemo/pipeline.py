"""Retrieve, apply the refusal threshold, answer, attach citations."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from .answer import REFUSAL, Answerer
from .embed import Embedder
from .store import Hit, PgVectorStore

STOPWORDS = frozenset(
    """about after again also been before being between both cannot could does doing down during each from have having
    here into itself just many more most much must only other over same should some such than that their them then
    there these they this those through under until very were what when where which while will with would your
    often long soon ever make made take need want know tell find give mean means called kind kinds""".split()
)


def query_words(question: str) -> list[str]:
    """Words handed to full-text search. Postgres does its own stemming, so they are passed whole."""
    words = [w for w in re.findall(r"[a-z0-9]+", question.lower()) if w not in STOPWORDS and len(w) >= 3]
    return list(dict.fromkeys(words))


def content_terms(question: str) -> list[str]:
    """Words of the question worth checking against the corpus, with plural and verb endings trimmed."""
    terms = []
    for token in re.findall(r"[a-z0-9]+", question.lower()):
        if token in STOPWORDS or (len(token) < 4 and not token.isdigit()):
            continue
        if token.isdigit() and len(token) < 3:
            continue
        stem = re.sub(r"(ies|es|s|ing|ed)$", "", token) if token.isalpha() else token
        term = stem if len(stem) >= 4 else token
        if term not in terms:
            terms.append(term)
    return terms


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
    retrieved: list[Hit] = field(default_factory=list)

    def public(self) -> dict:
        data = asdict(self)
        data.pop("retrieved")
        return data


class Pipeline:
    def __init__(
        self,
        store: PgVectorStore,
        embedder: Embedder,
        answerer: Answerer,
        collection: str,
        top_k: int = 5,
        max_citations: int = 3,
        threshold: float = 0.62,
        strict_threshold: float = 0.0,
        hybrid: bool = False,
        keyword_weight: float = 1.0,
    ) -> None:
        self.store = store
        self.embedder = embedder
        self.answerer = answerer
        self.collection = collection
        self.top_k = top_k
        self.max_citations = max_citations
        self.threshold = threshold
        self.hybrid = hybrid
        self.keyword_weight = keyword_weight
        # Applied in place of the threshold when the question uses a word found nowhere in the corpus. 0 turns it off.
        self.strict_threshold = strict_threshold

    def retrieve(self, question: str, k: int | None = None) -> list[Hit]:
        vector = self.embedder.embed_query(question)
        if self.hybrid:
            return self.store.search_hybrid(self.collection, vector, query_words(question), k or self.top_k, keyword_weight=self.keyword_weight)
        return self.store.search(self.collection, vector, k or self.top_k)

    def chat(
        self,
        question: str,
        threshold: float | None = None,
        strict_threshold: float | None = None,
        hits: list[Hit] | None = None,
    ) -> ChatResult:
        threshold = self.threshold if threshold is None else threshold
        strict = self.strict_threshold if strict_threshold is None else strict_threshold
        hits = self.retrieve(question) if hits is None else hits
        top = max((h.score for h in hits), default=0.0)
        unknown = self.store.missing_terms(self.collection, content_terms(question)) if strict > threshold else []
        limit = strict if unknown else threshold
        passages = [h for h in hits if h.score >= threshold][: self.max_citations]
        if top < limit or not passages:
            return ChatResult(REFUSAL, True, self.answerer.mode, top, limit, [], unknown, hits)
        answer = self.answerer.answer(question, passages)
        citations = [
            Citation(p.document, p.title, p.page, p.heading, round(p.score, 4), p.text[:240]) for p in (passages[i] for i in answer.cited)
        ]
        return ChatResult(answer.text, answer.refused, self.answerer.mode, top, limit, citations, unknown, hits)
