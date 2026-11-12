"""The refusal path: decide whether the retrieved passages are close enough to answer from.

Three checks, all made before any answer is written:

1. The best passage must reach the similarity threshold.
2. If the question uses a word that appears nowhere in the corpus, the best
   passage must reach a stricter threshold instead.
3. When the reranker is on, the best cross-encoder score must reach the rerank
   threshold. This is the check aimed at questions that are on the corpus
   topic but not answered by it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .store import Hit

REFUSAL = "I could not find this in the documents."

STOPWORDS = frozenset(
    """about after again also been before being between both cannot could does doing down during each from have having
    here into itself just many more most much must only other over same should some such than that their them then
    there these they this those through under until very were what when where which while will with would your
    often long soon ever make made take need want know tell find give mean means called kind kinds""".split()
)


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
class Decision:
    refused: bool
    top_score: float
    limit: float  # the threshold the top score was compared with
    unknown_terms: list[str]
    passages: list[Hit]  # passages that may be used for the answer, best first
    rerank_score: float | None = None  # best cross-encoder score, when the reranker ran
    refused_by: str = ""  # "similarity", "unknown word" or "rerank"


def decide(hits: list[Hit], unknown_terms: list[str], threshold: float, strict_threshold: float, max_passages: int) -> Decision:
    top = max((h.score for h in hits), default=0.0)
    limit = max(threshold, strict_threshold) if unknown_terms else threshold
    passages = [h for h in hits if h.score >= threshold][:max_passages]
    refused = top < limit or not passages
    reason = ("unknown word" if unknown_terms and top >= threshold else "similarity") if refused else ""
    return Decision(refused, top, limit, unknown_terms, [] if refused else passages, None, reason)


def decide_reranked(decision: Decision, reranked: list[Hit], rerank_threshold: float, threshold: float, max_passages: int) -> Decision:
    """The third check, applied to the passages in cross-encoder order."""
    best = max((h.rerank_score for h in reranked), default=float("-inf"))
    passages = [h for h in reranked if h.score >= threshold][:max_passages]
    refused = best < rerank_threshold or not passages
    return Decision(refused, decision.top_score, decision.limit, decision.unknown_terms, [] if refused else passages, best, "rerank" if refused else "")
