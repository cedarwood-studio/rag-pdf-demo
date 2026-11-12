from dataclasses import replace

import httpx
import pytest

from ragdemo.answer import GeneratedAnswerer
from ragdemo.llm import BudgetExceeded, ChatClient, Spend
from ragdemo.refusal import REFUSAL
from ragdemo.store import Hit


def test_chat_returns_answer_with_document_and_page(client):
    response = client.post("/chat", json={"question": "How often should I descale the kettle?"})
    assert response.status_code == 200
    data = response.json()
    assert data["refused"] is False
    assert data["mode"] == "extractive"
    top = data["citations"][0]
    assert top["document"] == "kettle-guide.pdf"
    assert top["page"] == 2
    assert top["heading"] == "2. Descaling"
    assert "citric acid" in data["answer"]


def test_out_of_corpus_question_is_refused(client):
    response = client.post("/chat", json={"question": "Which airlines fly from Lisbon to Toronto?"})
    data = response.json()
    assert data["refused"] is True
    assert data["answer"] == REFUSAL
    assert data["citations"] == []


def test_empty_question_is_rejected(client):
    assert client.post("/chat", json={"question": ""}).status_code == 422


def test_health_reports_chunk_count(client):
    data = client.get("/health").json()
    assert data["status"] == "ok"
    assert data["chunks"] == 3


def test_chat_page_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "/chat" in response.text


PASSAGES = [
    Hit("kettle-guide.pdf", "Kettle Guide", 2, "2. Descaling", "Descale every two months.", 0.9),
    Hit("kettle-guide.pdf", "Kettle Guide", 3, "3. Warranty", "Three years.", 0.8),
]


def _answerer(reply: str, spend: Spend | None = None) -> GeneratedAnswerer:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer test-key"
        body = {"choices": [{"message": {"content": reply}}], "usage": {"prompt_tokens": 1000, "completion_tokens": 100}}
        return httpx.Response(200, json=body)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    spend = spend or Spend(0.15, 0.60, max_usd=1.0)
    return GeneratedAnswerer(ChatClient("test-key", "https://llm.invalid/v1", "some-model", spend, client=client))


def test_generated_answer_keeps_only_cited_passages():
    answer = _answerer("Every two months [1].").answer("How often?", PASSAGES)
    assert answer.cited == [0]
    assert answer.refused is False


def test_generated_answer_without_citation_becomes_refusal():
    answer = _answerer("Probably every month.").answer("How often?", PASSAGES)
    assert answer.refused is True
    assert answer.text == REFUSAL


def test_generated_refusal_is_passed_through():
    answer = _answerer(REFUSAL).answer("Who won the cup?", PASSAGES)
    assert answer.refused is True
    assert answer.cited == []


def test_spend_is_counted_and_capped():
    spend = Spend(0.15, 0.60, max_usd=0.0003)
    answerer = _answerer("Every two months [1].", spend)
    answerer.answer("How often?", PASSAGES)
    assert spend.input_tokens == 1000 and spend.output_tokens == 100
    assert abs(spend.usd - 0.00021) < 1e-9
    answerer.answer("How often?", PASSAGES)  # 0.00042 after this call, over the cap
    with pytest.raises(BudgetExceeded):
        answerer.answer("How often?", PASSAGES)


def test_question_with_a_word_absent_from_the_corpus_meets_the_strict_threshold(pipeline):
    question = "How often should I descale the kettle in Reykjavik?"
    assert pipeline.chat(question).refused is False
    pipeline.strict_threshold = 0.99
    try:
        guarded = pipeline.chat(question)
        assert guarded.refused is True
        assert guarded.unknown_terms == ["reykjavik"]
        # A question made only of words the corpus knows is not held to the strict threshold.
        assert pipeline.chat("How often should I descale the kettle?").refused is False
    finally:
        pipeline.strict_threshold = 0.0


class OverlapReranker:
    """Stands in for the cross-encoder: scores a passage by the question words it contains."""

    def rerank(self, question: str, hits: list[Hit], top_k: int) -> list[Hit]:
        words = set(question.lower().replace("?", "").split())
        scored = [replace(h, rerank_score=float(len(words & set(h.text.lower().split())))) for h in hits]
        return sorted(scored, key=lambda h: -h.rerank_score)[:top_k]


def test_reranker_reorders_and_can_refuse(pipeline):
    pipeline.reranker, pipeline.rerank_threshold = OverlapReranker(), 1.0
    try:
        result = pipeline.chat("How long is the warranty on the heating element of the kettle?")
        assert result.refused is False
        assert result.citations[0].page == 3
        assert result.rerank_score >= 1.0
        pipeline.rerank_threshold = 99.0
        refused = pipeline.chat("How long is the warranty on the heating element of the kettle?")
        assert refused.refused is True
        assert refused.refused_by == "rerank"
    finally:
        pipeline.reranker = None
