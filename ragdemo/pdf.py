"""PDF text extraction that keeps the page number and the font of every line.

pypdf is used because its licence (BSD) puts no conditions on the code that
calls it. Font size and weight are what the chunker uses to find headings.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass
class Line:
    text: str
    size: float
    bold: bool


@dataclass
class Page:
    number: int  # 1-based position in the PDF file, the number a PDF viewer shows
    lines: list[Line]

    @property
    def text(self) -> str:
        return "\n".join(line.text for line in self.lines)


def _extract_lines(page) -> list[Line]:
    lines: list[Line] = []
    parts: list[str] = []
    weights: Counter = Counter()

    def flush() -> None:
        text = re.sub(r"\s+", " ", "".join(parts)).strip()
        if text:
            (size, bold), _ = weights.most_common(1)[0] if weights else ((0.0, False), 0)
            lines.append(Line(text=text, size=size, bold=bold))
        parts.clear()
        weights.clear()

    def visit(text, cm, tm, font_dict, font_size) -> None:
        if not text:
            return
        scale = abs(tm[3]) or abs(tm[0]) or 1.0
        cscale = abs(cm[3]) or abs(cm[0]) or 1.0
        size = round(float(font_size) * scale * cscale, 1)
        name = str(font_dict.get("/BaseFont", "")) if font_dict else ""
        bold = bool(re.search(r"bold|black|heavy|demi", name, re.I))
        pieces = text.split("\n")
        for i, piece in enumerate(pieces):
            if i > 0:
                flush()
            if piece.strip():
                weights[(size, bold)] += len(piece.strip())
            parts.append(piece)

    page.extract_text(visitor_text=visit)
    flush()
    return lines


def read_pdf(path: str | Path) -> list[Page]:
    reader = PdfReader(str(path))
    return [Page(number=i, lines=_extract_lines(p)) for i, p in enumerate(reader.pages, start=1)]


def body_font_size(pages: list[Page]) -> float:
    """The font size that carries the most characters is taken as body text."""
    sizes: Counter = Counter()
    for page in pages:
        for line in page.lines:
            sizes[line.size] += len(line.text)
    return sizes.most_common(1)[0][0] if sizes else 0.0
