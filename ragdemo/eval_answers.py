"""Answer-quality evaluation for the generated answer mode. Needs OPENAI_API_KEY in the environment.

    OPENAI_API_KEY=... python -m ragdemo.eval_answers --collection core --label answers-core

Any OpenAI-compatible endpoint can be used by setting OPENAI_BASE_URL and ANSWER_MODEL.

Every question is answered by the language model from the retrieved passages.
A second call to the same model then grades each answer twice:

- correctness: does the answer agree with the short reference answer in the question file?
- faithfulness: is every claim in the answer supported by the passages it cites?

The script also reports citation correctness, false refusals, and how many
out-of-corpus questions were refused (by the retrieval checks or by the model).
Token counts come from the API's usage field and the run stops at MAX_SPEND_USD.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from . import config
from .answer import format_passages
from .eval import IMPLEMENTATION, QUESTIONS, RESULTS, _match
from .llm import ChatClient, LLMError, Spend
from .pipeline import Pipeline, build_pipeline

CORRECTNESS_PROMPT = (
    "You grade answers from a document question answering system. Compare the answer with the reference answer. "
    'Reply with JSON: {"verdict": "correct" | "partial" | "incorrect", "reason": "<one sentence>"}. '
    '"correct" means the answer states the key facts of the reference and nothing that contradicts it. Extra detail is fine. '
    '"partial" means some key facts of the reference are missing or vague. '
    '"incorrect" means the answer contradicts the reference or misses its main point.'
)
FAITHFULNESS_PROMPT = (
    "You check whether an answer is supported by source passages. Ignore the bracketed citation numbers. "
    'Reply with JSON: {"verdict": "supported" | "partial" | "unsupported", "reason": "<one sentence>"}. '
    '"supported" means every factual claim in the answer is stated in or directly follows from the passages. '
    '"partial" means at least one claim is not in the passages. '
    '"unsupported" means the main claim of the answer is not in the passages.'
)


def grade(chat: ChatClient, system: str, user: str, allowed: tuple[str, ...]) -> dict:
    reply = chat.complete(system, user, json_reply=True, max_tokens=150)
    try:
        data = json.loads(reply)
    except json.JSONDecodeError:
        return {"verdict": "ungraded", "reason": "the grader did not return JSON"}
    verdict = str(data.get("verdict", "")).lower()
    return {"verdict": verdict if verdict in allowed else "ungraded", "reason": str(data.get("reason", ""))[:300]}


def evaluate(pipeline: Pipeline, grader: ChatClient, questions: list[dict]) -> dict:
    rows = []
    for q in questions:
        result = pipeline.chat(q["question"])
        in_corpus = q["document"] is not None
        row = {
            "id": q["id"],
            "question": q["question"],
            "in_corpus": in_corpus,
            "answer": result.answer,
            "refused": result.refused,
            "refused_by": result.refused_by or None,
            "cited": [f"{c.document} p.{c.page}" for c in result.citations],
        }
        if in_corpus:
            row["reference"] = q["reference"]
            row["citation_correct"] = any(_match(q, c.document, c.page) for c in result.citations)
        if not result.refused:
            passages = format_passages(result.passages)
            row["faithfulness"] = grade(
                grader, FAITHFULNESS_PROMPT, f"Passages:\n\n{passages}\n\nAnswer: {result.answer}", ("supported", "partial", "unsupported")
            )
            if in_corpus:
                row["correctness"] = grade(
                    grader,
                    CORRECTNESS_PROMPT,
                    f"Question: {q['question']}\nReference answer: {q['reference']}\nAnswer: {result.answer}",
                    ("correct", "partial", "incorrect"),
                )
        rows.append(row)
    return {"summary": summarize(rows), "rows": rows}


def summarize(rows: list[dict]) -> dict:
    inside = [r for r in rows if r["in_corpus"]]
    outside = [r for r in rows if not r["in_corpus"]]
    answered = [r for r in rows if not r["refused"]]

    def count(items: list[dict], test) -> dict:
        n = sum(1 for r in items if test(r))
        return {"count": n, "of": len(items), "rate": round(n / len(items), 3) if items else None}

    def verdict(r: dict, key: str) -> str:
        return r.get(key, {}).get("verdict", "")

    return {
        "answer_correct": count(inside, lambda r: verdict(r, "correctness") == "correct"),
        "answer_partial": count(inside, lambda r: verdict(r, "correctness") == "partial"),
        "answer_incorrect": count(inside, lambda r: verdict(r, "correctness") == "incorrect"),
        "false_refusals_in_corpus": count(inside, lambda r: r["refused"]),
        "citation_correct": count(inside, lambda r: r["citation_correct"]),
        "faithful_of_answered": count(answered, lambda r: verdict(r, "faithfulness") == "supported"),
        "partly_faithful_of_answered": count(answered, lambda r: verdict(r, "faithfulness") == "partial"),
        "unfaithful_of_answered": count(answered, lambda r: verdict(r, "faithfulness") == "unsupported"),
        "refusals_out_of_corpus": count(outside, lambda r: r["refused"]),
        "refused_by_model_out_of_corpus": count(outside, lambda r: r["refused_by"] == "model"),
    }


def to_markdown(report: dict) -> str:
    lines = [
        f"# Answer-quality run: {report['label']}",
        "",
        f"- Implementation: {report['implementation']}",
        f"- Questions: `eval/{report['questions']}`",
        f"- Collection: `{report['collection']}`",
        "- Answer mode: generated",
        f"- Answer and grading model: {report['model']} at {report['endpoint']}",
        f"- Embedding model: {report['embedding_model']}",
        f"- Reranker: {report['rerank']}",
        f"- Estimated spend: ${report['spend']['estimated_usd']:.4f} "
        f"({report['spend']['input_tokens']} input and {report['spend']['output_tokens']} output tokens, {report['spend']['calls']} calls)",
        f"- Run at: {report['run_at']}",
        "",
        "| Metric | Result |",
        "| --- | --- |",
    ]
    for key, value in report["summary"].items():
        rate = f" ({value['rate']:.0%})" if value["rate"] is not None else ""
        lines.append(f"| {key} | {value['count']}/{value['of']}{rate} |")
    lines += ["", "| Id | Question | Outcome | Correctness | Faithfulness | Cited | Answer |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in report["rows"]:
        outcome = f"refused by {r['refused_by']}" + ("" if r["refused_by"] == "model" else " check") if r["refused"] else "answered"
        answer = r["answer"].replace("\n", " ").replace("|", "/")[:300]
        lines.append(
            f"| {r['id']} | {r['question']} | {outcome} | {r.get('correctness', {}).get('verdict', '-')} | "
            f"{r.get('faithfulness', {}).get('verdict', '-')} | {'; '.join(r['cited']) or 'none'} | {answer} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    settings = config.load()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--collection", default=settings.collection)
    parser.add_argument("--questions", type=Path, default=QUESTIONS)
    parser.add_argument("--use-index", action=argparse.BooleanOptionalAction, default=settings.use_index)
    parser.add_argument("--rerank", action=argparse.BooleanOptionalAction, default=settings.rerank)
    parser.add_argument("--label", default=None)
    args = parser.parse_args()
    if not settings.openai_api_key:
        sys.exit("OPENAI_API_KEY is not set. This evaluation needs a language model; ragdemo.eval runs without one.")

    spend = Spend(settings.price_input_per_m, settings.price_output_per_m, settings.max_spend_usd)
    pipeline = build_pipeline(settings, spend=spend, collection=args.collection, use_index=args.use_index, rerank=args.rerank, answer_mode="generated")
    grader = ChatClient(settings.openai_api_key, settings.openai_base_url, settings.answer_model, spend)
    questions = json.loads(args.questions.read_text())
    try:
        report = evaluate(pipeline, grader, questions)
    except LLMError as error:
        sys.exit(f"stopped: {error}")
    label = args.label or f"answers-{args.collection}"
    report = {
        "label": label,
        "implementation": IMPLEMENTATION,
        "questions": args.questions.name,
        "collection": args.collection,
        "answer_mode": "generated",
        "model": settings.answer_model,
        "endpoint": settings.openai_base_url,
        "embedding_model": settings.embedding_model,
        "threshold": settings.score_threshold,
        "strict_threshold": settings.strict_threshold,
        "rerank": f"{settings.rerank_model}, pool {settings.rerank_pool}, threshold {settings.rerank_threshold}" if args.rerank else "off",
        "chunks": pipeline.count(),
        "spend": spend.report(),
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        **report,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{label}.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / f"{label}.md").write_text(to_markdown(report))
    print(f"label={label} collection={args.collection} mode=generated model={settings.answer_model}")
    for key, value in report["summary"].items():
        rate = f"  {value['rate']:.0%}" if value["rate"] is not None else ""
        print(f"  {key:32s} {value['count']}/{value['of']}{rate}")
    print(f"  estimated spend ${spend.usd:.4f} ({spend.input_tokens} input, {spend.output_tokens} output tokens, {spend.calls} calls)")
    print(f"saved eval/results/{label}.json and eval/results/{label}.md")


if __name__ == "__main__":
    main()
