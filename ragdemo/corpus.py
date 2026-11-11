"""Download the public PDFs listed in corpus/sources.json and verify their checksums."""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "corpus" / "sources.json"
PDF_DIR = ROOT / "data" / "pdfs"


def load_sources() -> list[dict]:
    return json.loads(SOURCES.read_text())


def fetch(pdf_dir: Path = PDF_DIR) -> None:
    pdf_dir.mkdir(parents=True, exist_ok=True)
    for src in load_sources():
        target = pdf_dir / src["file"]
        if not target.exists():
            print(f"downloading {src['url']}", flush=True)
            request = urllib.request.Request(src["url"], headers={"User-Agent": "rag-pdf-demo/0.1"})
            with urllib.request.urlopen(request, timeout=120) as response:
                target.write_bytes(response.read())
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != src["sha256"]:
            sys.exit(f"checksum mismatch for {src['file']}: got {digest}")
    print(f"{len(load_sources())} PDFs present and verified in {pdf_dir}")


if __name__ == "__main__":
    fetch()
