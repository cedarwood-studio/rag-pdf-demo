"""Query latency and storage size for one collection.

    python -m ragdemo.bench --collection full --label bench-full

Runs every question of eval/questions.json several times through the extractive
pipeline and reports the median and 95th percentile, split into the time spent
embedding the question, searching the database, reranking, and the whole /chat path.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

from . import config
from .eval import IMPLEMENTATION, QUESTIONS, RESULTS
from .pipeline import build_pipeline


def percentiles(values: list[float]) -> dict:
    ordered = sorted(values)
    p95 = ordered[min(len(ordered) - 1, round(0.95 * (len(ordered) - 1)))]
    return {"p50_ms": round(statistics.median(ordered), 1), "p95_ms": round(p95, 1)}


def run(pipeline, questions: list[str], passes: int) -> dict:
    for question in questions[:3]:  # warm up the model and the connection
        pipeline.chat(question)
    embed, search, rerank, total, top5 = [], [], [], [], {}
    for _ in range(passes):
        for question in questions:
            start = time.perf_counter()
            result = pipeline.chat(question)
            total.append((time.perf_counter() - start) * 1000)
            embed.append(pipeline.timings["embed_ms"])
            search.append(pipeline.timings["search_ms"])
            rerank.append(pipeline.timings["rerank_ms"])
            top5[question] = [(h.document, h.page, h.text[:40]) for h in result.retrieved]
    return {
        "embed": percentiles(embed),
        "search": percentiles(search),
        "rerank": percentiles(rerank),
        "total": percentiles(total),
        "samples": len(total),
        "top5": top5,
    }


def main() -> None:
    settings = config.load()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--collection", default=settings.collection)
    parser.add_argument("--passes", type=int, default=3)
    parser.add_argument("--with-index", action="store_true", help="also build an HNSW index and measure again")
    parser.add_argument("--label", default=None)
    args = parser.parse_args()
    questions = [q["question"] for q in json.loads(Path(QUESTIONS).read_text())]

    # The index comparison is about vector search, so the reranker is off there. It is timed as a third run.
    common = {"collection": args.collection, "answer_mode": "extractive"}
    exact = build_pipeline(settings, **common, rerank=False, use_index=False)
    store = exact.retriever.store
    store.drop_index()
    # First without the trigram index, to record what the refusal check's word lookup costs as a plain scan.
    store.drop_text_index()
    unindexed = run(exact, questions, 1)
    unindexed.pop("top5")
    store.create_text_index()
    report = {
        "label": args.label or f"bench-{args.collection}",
        "implementation": IMPLEMENTATION,
        "collection": args.collection,
        "answer_mode": "extractive",
        **exact.retriever.store.stats(args.collection),
    }
    measured = run(exact, questions, args.passes)
    exact_top5 = measured.pop("top5")
    report["exact"] = measured
    report["exact_without_text_index"] = {"total": unindexed["total"], "samples": unindexed["samples"]}
    if args.with_index:
        build_seconds = store.create_index()
        indexed = build_pipeline(settings, **common, rerank=False, use_index=True)
        measured = run(indexed, questions, args.passes)
        index_top5 = measured.pop("top5")
        same = sum(len(set(exact_top5[q]) & set(index_top5[q])) for q in questions)
        report["hnsw"] = {
            **measured,
            "build_seconds": round(build_seconds, 1),
            "top5_overlap_with_exact": round(same / sum(len(exact_top5[q]) for q in questions), 3),
            "table_with_indexes_bytes": indexed.retriever.store.stats(args.collection)["table_with_indexes_bytes"],
        }
    if not settings.use_index:
        store.drop_index()  # leave the database as the default configuration expects it: exact search
    if settings.rerank:
        measured = run(build_pipeline(settings, **common, rerank=True, use_index=False), questions, 1)
        measured.pop("top5")
        report["exact_with_rerank"] = measured
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{report['label']}.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
