"""Read the PDFs, chunk them, embed the chunks and store them in pgvector.

python -m ragdemo.ingest --corpus core
python -m ragdemo.ingest --corpus full
python -m ragdemo.ingest --corpus core --strategy fixed    # the baseline chunker, stored as "core-fixed"
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from . import config
from .chunking import chunk_pages
from .corpus import DATA, PDF_DIR, ROOT, fetch, load_sources
from .embed import Embedder, make_embedder
from .pdf import read_pdf
from .store import PgVectorStore

RESULTS = ROOT / "eval" / "results"


def ingest_file(store, embedder: Embedder, collection: str, path: Path, document: str, title: str, strategy: str) -> tuple[int, int]:
    """Returns (pages, chunks)."""
    pages = read_pdf(path)
    chunks = chunk_pages(pages, strategy)
    vectors = embedder.embed_documents([c.embed_text(title) for c in chunks])
    store.add(collection, [(document, title, c.page, c.heading, c.text, v) for c, v in zip(chunks, vectors, strict=True)])
    return len(pages), len(chunks)


def main() -> None:
    settings = config.load()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--corpus", choices=["core", "full"], default=settings.corpus)
    parser.add_argument("--strategy", choices=["heading", "fixed"], default="heading")
    parser.add_argument("--collection", default=None, help="defaults to the corpus name, with -fixed added for the baseline chunker")
    parser.add_argument("--if-empty", action="store_true", help="do nothing when the collection already has chunks")
    args = parser.parse_args()

    collection = args.collection or (args.corpus if args.strategy == "heading" else f"{args.corpus}-{args.strategy}")
    embedder = make_embedder(settings.embedding_provider, settings.embedding_model, cache=DATA / "cache" / "embeddings.sqlite")
    store = PgVectorStore(settings.database_url, embedder.dim)
    store.wait_until_ready()
    store.init_schema()
    if args.if_empty and store.count(collection) > 0:
        print(f"collection '{collection}' already has {store.count(collection)} chunks, skipping ingest")
        return
    fetch(args.corpus)
    store.delete_collection(collection)
    start = time.perf_counter()
    pages = chunks = 0
    sources = load_sources(args.corpus)
    per_document = []
    for src in sources:
        began, embedded = time.perf_counter(), embedder.compute_seconds
        p, c = ingest_file(store, embedder, collection, PDF_DIR / src["file"], src["file"], src["title"], args.strategy)
        pages += p
        chunks += c
        seconds = round(time.perf_counter() - began, 1)
        per_document.append(
            {
                "file": src["file"],
                "set": src["set"],
                "pages": p,
                "chunks": c,
                "seconds": seconds,
                "embedding_seconds": round(embedder.compute_seconds - embedded, 1),
            }
        )
        print(f"{src['file']}: {p} pages, {c} chunks, {seconds}s", flush=True)
    total = time.perf_counter() - start
    report = {
        "collection": collection,
        "documents": len(sources),
        "pages": pages,
        "chunks": chunks,
        "total_seconds": round(total, 1),
        "embedded_now": embedder.computed,
        "embedding_seconds": round(embedder.compute_seconds, 1),
        "from_cache": chunks - embedder.computed,
        "parse_and_store_seconds": round(total - embedder.compute_seconds, 1),
        "per_document": per_document,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    # Keep the record of the cold run: a later run that only reads the cache must not overwrite its timings.
    record = RESULTS / f"ingest-{collection}.json"
    if embedder.computed == chunks or not record.exists():
        record.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "per_document"}))


if __name__ == "__main__":
    main()
