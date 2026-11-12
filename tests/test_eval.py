import httpx

from ragdemo.bench import percentiles
from ragdemo.corpus import load_sources
from ragdemo.eval_answers import CORRECTNESS_PROMPT, grade, summarize
from ragdemo.llm import ChatClient, Spend


def _grader(reply: str) -> ChatClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"choices": [{"message": {"content": reply}}], "usage": {"prompt_tokens": 50, "completion_tokens": 10}})

    return ChatClient("test-key", "https://llm.invalid/v1", "some-model", Spend(0.15, 0.60, 1.0), client=httpx.Client(transport=httpx.MockTransport(handler)))


def test_grader_verdict_is_parsed():
    result = grade(_grader('{"verdict": "Correct", "reason": "matches"}'), CORRECTNESS_PROMPT, "Question: ...", ("correct", "partial", "incorrect"))
    assert result == {"verdict": "correct", "reason": "matches"}


def test_grader_reply_outside_the_allowed_labels_is_ungraded():
    allowed = ("correct", "partial", "incorrect")
    assert grade(_grader('{"verdict": "maybe"}'), CORRECTNESS_PROMPT, "x", allowed)["verdict"] == "ungraded"
    assert grade(_grader("not json"), CORRECTNESS_PROMPT, "x", allowed)["verdict"] == "ungraded"


def test_summary_counts_each_outcome_once():
    rows = [
        {"in_corpus": True, "refused": False, "refused_by": None, "citation_correct": True,
         "correctness": {"verdict": "correct"}, "faithfulness": {"verdict": "supported"}},
        {"in_corpus": True, "refused": True, "refused_by": "model", "citation_correct": False},
        {"in_corpus": False, "refused": True, "refused_by": "retrieval checks"},
        {"in_corpus": False, "refused": False, "refused_by": None, "faithfulness": {"verdict": "unsupported"}},
    ]  # fmt: skip
    s = summarize(rows)
    assert (s["answer_correct"]["count"], s["answer_correct"]["of"]) == (1, 2)
    assert s["false_refusals_in_corpus"]["count"] == 1
    assert (s["faithful_of_answered"]["count"], s["faithful_of_answered"]["of"]) == (1, 2)
    assert s["unfaithful_of_answered"]["count"] == 1
    assert (s["refusals_out_of_corpus"]["count"], s["refused_by_model_out_of_corpus"]["count"]) == (1, 0)


def test_percentiles():
    assert percentiles([float(i) for i in range(1, 101)]) == {"p50_ms": 50.5, "p95_ms": 95.0}


def test_corpus_manifest_sets():
    core, full = load_sources("core"), load_sources("full")
    assert len(core) == 12
    assert len(full) >= 100
    assert len({s["file"] for s in full}) == len(full)
    assert all(len(s["sha256"]) == 64 and s["url"].startswith("https://nvlpubs.nist.gov/") for s in full)
