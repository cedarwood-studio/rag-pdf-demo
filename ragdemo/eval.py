"""Scripted evaluation over the fixed question set in eval/questions.json.

    python -m ragdemo.eval --collection core --label core

Each question names the document and the pages where its answer is stated, or
no document at all when the answer is not in the corpus. The script runs every
question through the same Pipeline object that serves /chat, with the extractive answer step, and reports:

- retrieval hit rate at k: an accepted page of the expected document is among the top k chunks
- citation correctness: the answer was given and a cited passage is on an accepted page
- false refusals: in-corpus questions the system declined to answer
- refusal rate: out-of-corpus questions the system declined to answer
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from . import config
from .pipeline import Pipeline, build_pipeline

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "eval" / "questions.json"
RESULTS = ROOT / "eval" / "results"
KS = (1, 3, 5)
IMPLEMENTATION = "plain Python"


def _match(q: dict, document: str, page: int) -> bool:
    return document == q["document"] and page in q["pages"]


def evaluate(pipeline: Pipeline, questions: list[dict]) -> dict:
    rows = []
    for q in questions:
        result = pipeline.chat(q["question"])
        hits = result.retrieved
        in_corpus = q["document"] is not None
        row = {
            "id": q["id"],
            "question": q["question"],
            "in_corpus": in_corpus,
            "expected": f"{q['document']} p.{','.join(map(str, q['pages']))}" if in_corpus else "not in corpus",
            "top_score": round(result.top_score, 4),
            "unknown_terms": result.unknown_terms,
            "rerank_score": None if result.rerank_score is None else round(result.rerank_score, 2),
            "refused": result.refused,
            "refused_by": result.refused_by,
            "retrieved": [f"{h.document} p.{h.page} ({h.score:.3f})" for h in hits],
            "cited": [f"{c.document} p.{c.page}" for c in result.citations],
        }
        if in_corpus:
            for k in KS:
                row[f"hit@{k}"] = any(_match(q, h.document, h.page) for h in hits[:k])
            row["top_citation_correct"] = bool(result.citations) and _match(q, result.citations[0].document, result.citations[0].page)
            row["citation_correct"] = any(_match(q, c.document, c.page) for c in result.citations)
        rows.append(row)

    inside = [r for r in rows if r["in_corpus"]]
    outside = [r for r in rows if not r["in_corpus"]]

    def rate(items: list[dict], key: str) -> dict:
        n = sum(1 for r in items if r[key])
        return {"count": n, "of": len(items), "rate": round(n / len(items), 3) if items else None}

    summary = {f"retrieval_hit@{k}": rate(inside, f"hit@{k}") for k in KS}
    summary["citation_correct"] = rate(inside, "citation_correct")
    summary["top_citation_correct"] = rate(inside, "top_citation_correct")
    summary["false_refusals_in_corpus"] = rate(inside, "refused")
    summary["refusals_out_of_corpus"] = rate(outside, "refused")
    return {"summary": summary, "rows": rows}


def sweep(rows: list[dict], strict: float = 0.0) -> list[dict]:
    """Refusal depends only on the top score and the unknown terms, so every threshold can be scored from one run."""

    def refused(r: dict, t: float) -> bool:
        return r["top_score"] < (max(t, strict) if r["unknown_terms"] else t)

    out = []
    for step in range(50, 81, 2):
        t = step / 100
        inside = [r for r in rows if r["in_corpus"]]
        outside = [r for r in rows if not r["in_corpus"]]
        out.append(
            {
                "threshold": t,
                "false_refusals_in_corpus": sum(refused(r, t) for r in inside),
                "in_corpus": len(inside),
                "refusals_out_of_corpus": sum(refused(r, t) for r in outside),
                "out_of_corpus": len(outside),
            }
        )
    return out


def rerank_sweep(rows: list[dict]) -> list[dict]:
    """For questions that passed the similarity checks: how many each rerank threshold would refuse."""
    passed = [r for r in rows if r["rerank_score"] is not None]
    inside = [r for r in passed if r["in_corpus"]]
    outside = [r for r in passed if not r["in_corpus"]]
    out = []
    for step in range(-8, 9):
        t = step / 2
        out.append(
            {
                "rerank_threshold": t,
                "false_refusals_in_corpus": sum(r["rerank_score"] < t for r in inside),
                "in_corpus": len(inside),
                "refusals_out_of_corpus": sum(r["rerank_score"] < t for r in outside),
                "out_of_corpus": len(outside),
            }
        )
    return out


def to_markdown(report: dict) -> str:
    s = report["summary"]
    lines = [
        f"# Evaluation run: {report['label']}",
        "",
        f"- Questions: `eval/{report['questions']}`",
        f"- Collection: `{report['collection']}`",
        f"- Answer mode: {report['answer_mode']}",
        f"- Implementation: {report['implementation']}",
        f"- Search: {report['search']}",
        f"- Reranker: {report['rerank']}",
        f"- Embedding model: {report['embedding_model']}",
        f"- Refusal threshold: {report['threshold']}",
        f"- Strict threshold for questions with a word found nowhere in the corpus: {report['strict_threshold'] or 'off'}",
        f"- Chunks in collection: {report['chunks']}",
        f"- Run at: {report['run_at']}",
        "",
        "| Metric | Result |",
        "| --- | --- |",
    ]
    for key, value in s.items():
        lines.append(f"| {key} | {value['count']}/{value['of']} ({value['rate']:.0%}) |")
    lines += ["", "| Id | Question | Expected | Top score | Rerank score | Unknown words | Outcome | Cited |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in report["rows"]:
        if r["in_corpus"]:
            outcome = f"refused by {r['refused_by']} check (wrong)" if r["refused"] else ("citation correct" if r["citation_correct"] else "citation wrong")
        else:
            outcome = f"refused by {r['refused_by']} check (right)" if r["refused"] else "answered (wrong)"
        lines.append(
            f"| {r['id']} | {r['question']} | {r['expected']} | {r['top_score']:.3f} | {'-' if r['rerank_score'] is None else r['rerank_score']} | {', '.join(r['unknown_terms']) or '-'} | {outcome} | {'; '.join(r['cited']) or 'none'} |"
        )
    lines += ["", "## Threshold sweep", "", "| Threshold | False refusals (in corpus) | Refusals (out of corpus) |", "| --- | --- | --- |"]
    for row in report["sweep"]:
        lines.append(
            f"| {row['threshold']:.2f} | {row['false_refusals_in_corpus']}/{row['in_corpus']} | {row['refusals_out_of_corpus']}/{row['out_of_corpus']} |"
        )
    if report.get("rerank_sweep"):
        lines += [
            "",
            "## Rerank threshold sweep",
            "",
            "Only questions that passed the similarity checks reach the reranker, so only those are counted here.",
            "",
            "| Rerank threshold | False refusals (in corpus) | Refusals (out of corpus) |",
            "| --- | --- | --- |",
        ]
        for row in report["rerank_sweep"]:
            lines.append(
                f"| {row['rerank_threshold']:.1f} | {row['false_refusals_in_corpus']}/{row['in_corpus']} | {row['refusals_out_of_corpus']}/{row['out_of_corpus']} |"
            )
    return "\n".join(lines) + "\n"


def main() -> None:
    settings = config.load()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--collection", default=settings.collection)
    parser.add_argument("--threshold", type=float, default=settings.score_threshold)
    parser.add_argument("--strict-threshold", type=float, default=settings.strict_threshold)
    parser.add_argument("--rerank", action=argparse.BooleanOptionalAction, default=settings.rerank)
    parser.add_argument("--rerank-threshold", type=float, default=settings.rerank_threshold)
    parser.add_argument("--use-index", action=argparse.BooleanOptionalAction, default=settings.use_index)
    parser.add_argument("--questions", type=Path, default=QUESTIONS, help="question file, defaults to eval/questions.json")
    parser.add_argument("--label", default=None)
    args = parser.parse_args()

    # This script scores retrieval, citations and refusals. It always runs the extractive answer step,
    # so a key in the environment cannot change its numbers. Generated answers are scored by ragdemo.eval_answers.
    pipeline = build_pipeline(
        settings,
        collection=args.collection,
        score_threshold=args.threshold,
        strict_threshold=args.strict_threshold,
        use_index=args.use_index,
        rerank=args.rerank,
        rerank_threshold=args.rerank_threshold,
        answer_mode="extractive",
    )
    questions = json.loads(args.questions.read_text())
    report = evaluate(pipeline, questions)
    label = args.label or args.collection
    report = {
        "label": label,
        "implementation": IMPLEMENTATION,
        "questions": args.questions.name,
        "collection": args.collection,
        "answer_mode": pipeline.mode,
        "embedding_model": settings.embedding_model,
        "threshold": args.threshold,
        "strict_threshold": args.strict_threshold,
        "search": "HNSW index" if args.use_index else "exact",
        "rerank": f"{settings.rerank_model}, pool {settings.rerank_pool}, threshold {args.rerank_threshold}" if args.rerank else "off",
        "top_k": settings.top_k,
        "max_citations": settings.max_citations,
        "chunks": pipeline.count(),
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        **report,
    }
    report["sweep"] = sweep(report["rows"], args.strict_threshold)
    report["rerank_sweep"] = rerank_sweep(report["rows"]) if args.rerank else []
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{label}.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / f"{label}.md").write_text(to_markdown(report))

    print(f"label={label} collection={args.collection} mode={pipeline.mode} threshold={args.threshold} strict={args.strict_threshold}")
    for key, value in report["summary"].items():
        print(f"  {key:28s} {value['count']}/{value['of']}  {value['rate']:.0%}")
    print(f"saved eval/results/{label}.json and eval/results/{label}.md")


if __name__ == "__main__":
    main()
