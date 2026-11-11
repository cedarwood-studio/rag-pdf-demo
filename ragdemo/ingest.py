"""Read the PDFs, chunk them, embed the chunks and store them in pgvector.

    python -m ragdemo.ingest --strategy heading --collection heading
"""

from __future__ import annotations

import argparse
import time

from . import config
from .chunking import chunk_pages
from .corpus import PDF_DIR, fetch, load_sources
from .embed import Embedder, make_embedder
from .pdf import read_pdf
from .store import PgVectorStore


def ingest_file(store, embedder: Embedder, collection, path, document, title, strategy, max_chars=None, with_heading=True) -> int:
    chunks = chunk_pages(read_pdf(path), strategy, max_chars)
    vectors = embedder.embed_documents([c.embed_text(title, with_heading) for c in chunks])
    store.add(collection, [(document, title, c.page, c.heading, c.text, v) for c, v in zip(chunks, vectors, strict=True)])
    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", choices=["heading", "fixed"], default="heading")
    parser.add_argument("--collection", default=None, help="defaults to the strategy name")
    parser.add_argument("--max-chars", type=int, default=None)
    parser.add_argument("--no-heading-context", action="store_true", help="embed chunk text without its heading path")
    parser.add_argument("--if-empty", action="store_true", help="do nothing when the collection already has chunks")
    args = parser.parse_args()

    settings = config.load()
    collection = args.collection or args.strategy
    embedder = make_embedder(settings.embedding_provider, settings.embedding_model)
    store = PgVectorStore(settings.database_url, embedder.dim)
    store.wait_until_ready()
    store.init_schema()
    if args.if_empty and store.count(collection) > 0:
        print(f"collection '{collection}' already has {store.count(collection)} chunks, skipping ingest")
        return
    fetch()
    store.delete_collection(collection)
    start = time.time()
    total = 0
    for src in load_sources():
        n = ingest_file(
            store, embedder, collection, PDF_DIR / src["file"], src["file"], src["title"],
            args.strategy, args.max_chars, not args.no_heading_context,
        )
        total += n
        print(f"{src['file']}: {n} chunks", flush=True)
    print(f"ingested {total} chunks into '{collection}' in {time.time() - start:.0f}s")


if __name__ == "__main__":
    main()
