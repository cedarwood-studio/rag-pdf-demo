"""Download the public PDFs listed in corpus/sources.json and verify their checksums.

    python -m ragdemo.corpus --corpus core    # 12 PDFs
    python -m ragdemo.corpus --corpus full    # about 100 PDFs
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "corpus" / "sources.json"
DATA = ROOT / "data"
PDF_DIR = DATA / "pdfs"


def load_sources(corpus: str = "core") -> list[dict]:
    """The "core" set is the first 12 documents. "full" is every document in the manifest."""
    sources = json.loads(SOURCES.read_text())
    if corpus == "full":
        return sources
    if corpus == "core":
        return [s for s in sources if s["set"] == "core"]
    raise ValueError(f"unknown corpus: {corpus}")


def fetch(corpus: str = "core", pdf_dir: Path = PDF_DIR) -> None:
    pdf_dir.mkdir(parents=True, exist_ok=True)
    sources = load_sources(corpus)
    for src in sources:
        target = pdf_dir / src["file"]
        if not target.exists():
            print(f"downloading {src['url']}", flush=True)
            request = urllib.request.Request(src["url"], headers={"User-Agent": "Mozilla/5.0 rag-pdf-demo"})
            with urllib.request.urlopen(request, timeout=120) as response:
                target.write_bytes(response.read())
            time.sleep(0.5)  # the publisher's server throttles bursts
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != src["sha256"]:
            sys.exit(f"checksum mismatch for {src['file']}: got {digest}")
    print(f"{len(sources)} PDFs present and verified in {pdf_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", choices=["core", "full"], default="core")
    fetch(parser.parse_args().corpus)
