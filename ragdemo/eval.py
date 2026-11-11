"""Scripted evaluation over the fixed question set in eval/questions.json.

    python -m ragdemo.eval --collection heading --threshold 0.62 --label tuned

Each question names the document and the pages where its answer is stated, or
no document at all when the answer is not in the corpus. The script runs every
question through the same Pipeline object that serves /chat and reports:

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
from .answer import make_answerer
from .embed import make_embedder
from .pipeline import Pipeline
from .store import PgVectorStore

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "eval" / "questions.json"
RESULTS = ROOT / "eval" / "results"
KS = (1, 3, 5)


def _match(q: dict, document: str, page: int) -> bool:
    return document == q["document"] and page in q["pages"]


def evaluate(pipeline: Pipeline, questions: list[dict], threshold: float, strict: float = 0.0) -> dict:
    rows = []
    for q in questions:
        hits = pipeline.retrieve(q["question"], k=pipeline.top_k)
        result = pipeline.chat(q["question"], threshold=threshold, strict_threshold=strict, hits=hits)
        in_corpus = q["document"] is not None
        row = {
            "id": q["id"],
            "question": q["question"],
            "in_corpus": in_corpus,
            "expected": f"{q['document']} p.{','.join(map(str, q['pages']))}" if in_corpus else "not in corpus",
            "top_score": round(result.top_score, 4),
            "unknown_terms": result.unknown_terms,
            "refused": result.refused,
            "retrieved": [f"{h.document} p.{h.page} ({h.score:.3f})" for h in hits],
            "cited": [f"{c.document} p.{c.page}" for c in result.citations],
        }
        if in_corpus:
            for k in KS:
                row[f"hit@{k}"] = any(_match(q, h.document, h.page) for h in hits[:k])
            row["top_citation_correct"] = bool(result.citations) and _match(
                q, result.citations[0].document, result.citations[0].page
            )
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


def to_markdown(report: dict) -> str:
    s = report["summary"]
    lines = [
        f"# Evaluation run: {report['label']}",
        "",
        f"- Questions: `eval/{report['questions']}`",
        f"- Collection: `{report['collection']}`",
        f"- Answer mode: {report['answer_mode']}",
        f"- Retrieval: {report['retrieval']}",
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
    lines += ["", "| Id | Question | Expected | Top score | Unknown words | Outcome | Cited |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in report["rows"]:
        if r["in_corpus"]:
            outcome = "refused (wrong)" if r["refused"] else ("citation correct" if r["citation_correct"] else "citation wrong")
        else:
            outcome = "refused (right)" if r["refused"] else "answered (wrong)"
        lines.append(
            f"| {r['id']} | {r['question']} | {r['expected']} | {r['top_score']:.3f} | {', '.join(r['unknown_terms']) or '-'} | {outcome} | {'; '.join(r['cited']) or 'none'} |"
        )
    lines += ["", "## Threshold sweep", "", "| Threshold | False refusals (in corpus) | Refusals (out of corpus) |", "| --- | --- | --- |"]
    for row in report["sweep"]:
        lines.append(
            f"| {row['threshold']:.2f} | {row['false_refusals_in_corpus']}/{row['in_corpus']} | {row['refusals_out_of_corpus']}/{row['out_of_corpus']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    settings = config.load()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--collection", default=settings.collection)
    parser.add_argument("--threshold", type=float, default=settings.score_threshold)
    parser.add_argument("--strict-threshold", type=float, default=settings.strict_threshold)
    parser.add_argument("--hybrid", action=argparse.BooleanOptionalAction, default=settings.hybrid)
    parser.add_argument("--keyword-weight", type=float, default=settings.keyword_weight)
    parser.add_argument("--questions", type=Path, default=QUESTIONS, help="question file, defaults to eval/questions.json")
    parser.add_argument("--label", default=None)
    args = parser.parse_args()

    embedder = make_embedder(settings.embedding_provider, settings.embedding_model)
    store = PgVectorStore(settings.database_url, embedder.dim)
    answerer = make_answerer(settings.openai_api_key, settings.openai_base_url, settings.openai_model)
    pipeline = Pipeline(store, embedder, answerer, args.collection, settings.top_k, settings.max_citations, args.threshold, hybrid=args.hybrid)
    pipeline.keyword_weight = args.keyword_weight

    questions = json.loads(args.questions.read_text())
    report = evaluate(pipeline, questions, args.threshold, args.strict_threshold)
    label = args.label or args.collection
    report = {
        "label": label,
        "questions": args.questions.name,
        "collection": args.collection,
        "answer_mode": answerer.mode,
        "embedding_model": settings.embedding_model,
        "threshold": args.threshold,
        "strict_threshold": args.strict_threshold,
        "retrieval": f"hybrid (vector plus full-text, rank fusion, keyword weight {args.keyword_weight})" if args.hybrid else "vector only",
        "top_k": settings.top_k,
        "max_citations": settings.max_citations,
        "chunks": store.count(args.collection),
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        **report,
    }
    report["sweep"] = sweep(report["rows"], args.strict_threshold)
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{label}.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / f"{label}.md").write_text(to_markdown(report))

    print(f"label={label} collection={args.collection} mode={answerer.mode} threshold={args.threshold} strict={args.strict_threshold}")
    for key, value in report["summary"].items():
        print(f"  {key:28s} {value['count']}/{value['of']}  {value['rate']:.0%}")
    print(f"saved eval/results/{label}.json and eval/results/{label}.md")


if __name__ == "__main__":
    main()
