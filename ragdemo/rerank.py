"""Second-stage ranking with a cross-encoder.

Vector search compares the question with each passage separately. A
cross-encoder reads the question and one passage together and scores how well
the passage answers the question. It is slower (it runs once per candidate
passage) and more accurate, so it is applied only to the candidates that
vector search returns.

The best cross-encoder score is also used as a refusal check: a passage can be
about the same subject as the question without answering it, and this score
separates those cases better than cosine similarity does.
"""

from __future__ import annotations

from dataclasses import replace

from .store import Hit


class Reranker:
    def __init__(self, model: str = "Xenova/ms-marco-MiniLM-L-6-v2") -> None:
        from fastembed.rerank.cross_encoder import TextCrossEncoder

        self._model = TextCrossEncoder(model_name=model)

    def rerank(self, question: str, hits: list[Hit], top_k: int) -> list[Hit]:
        """The top_k hits by cross-encoder score, best first, each carrying its rerank_score."""
        if not hits:
            return []
        scores = list(self._model.rerank(question, [h.text for h in hits]))
        ranked = sorted(zip(hits, scores, strict=True), key=lambda pair: -pair[1])
        return [replace(hit, rerank_score=float(score)) for hit, score in ranked[:top_k]]
