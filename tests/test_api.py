import httpx

from ragdemo.answer import REFUSAL, OpenAICompatAnswerer
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


def _answerer(reply: str) -> OpenAICompatAnswerer:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer test-key"
        return httpx.Response(200, json={"choices": [{"message": {"content": reply}}]})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    return OpenAICompatAnswerer("test-key", "https://llm.invalid/v1", "some-model", client=client)


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


def test_question_with_a_word_absent_from_the_corpus_meets_the_strict_threshold(pipeline):
    question = "How often should I descale the kettle in Reykjavik?"
    assert pipeline.chat(question).refused is False
    guarded = pipeline.chat(question, strict_threshold=0.99)
    assert guarded.refused is True
    assert guarded.unknown_terms == ["reykjavik"]
    # A question made only of words the corpus knows is not held to the strict threshold.
    assert pipeline.chat("How often should I descale the kettle?", strict_threshold=0.99).refused is False


def test_hybrid_search_finds_exact_words_and_keeps_cosine_scores(pipeline):
    vector = pipeline.embedder.embed_query("limescale")
    hits = pipeline.store.search_hybrid("test", vector, ["limescale"], k=3)
    assert hits[0].page == 3
    assert 0.0 < hits[0].score <= 1.0
