"""Two chunkers that both keep the page number on every chunk.

"fixed" is the baseline: fixed-size windows cut inside each page, blind to
structure. "heading" is the tuned one: it drops running headers and footers,
finds section headings from font weight and numbering, starts a new chunk at
each heading, never crosses a page, and stores the heading path with the chunk
so it can be embedded alongside the text.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from .pdf import Line, Page, body_font_size

NUMBERED = re.compile(r"^(?:(\d{1,2}(?:\.\d{1,2}){0,4})\.?|Appendix\s+([A-Z]))(?:\s|[\u2014:.-])+\S")
CAPTION = re.compile(r"^(Figure|Table|Fig\.)\s", re.I)


@dataclass
class Chunk:
    page: int
    heading: str
    text: str

    def embed_text(self, title: str, with_heading: bool = True) -> str:
        if with_heading and self.heading:
            return f"{title}\n{self.heading}\n{self.text}"
        return self.text


def _norm(text: str) -> str:
    return re.sub(r"\d+", "#", text.strip().lower())


def strip_running_lines(pages: list[Page]) -> list[Page]:
    """Remove headers, footers and bare page numbers.

    A line counts as a running header or footer when the same text (digits
    ignored) sits in the first or last two lines of more than 30% of pages.
    """
    edge: Counter = Counter()
    for page in pages:
        seen = {_norm(line.text) for line in page.lines[:2] + page.lines[-2:]}
        edge.update(seen)
    limit = max(3, int(len(pages) * 0.3))
    repeated = {text for text, count in edge.items() if count >= limit}
    cleaned = []
    for page in pages:
        lines = []
        for i, line in enumerate(page.lines):
            at_edge = i < 2 or i >= len(page.lines) - 2
            if at_edge and (_norm(line.text) in repeated or re.fullmatch(r"[\divxlc\-\u2013 ]{1,8}", line.text.lower())):
                continue
            lines.append(line)
        cleaned.append(Page(number=page.number, lines=lines))
    return cleaned


def is_heading(line: Line, body: float) -> bool:
    text = line.text
    if len(text) > 110 or len(text) < 3 or CAPTION.match(text):
        return False
    if re.search(r"\.{2,}|(\. ){2,}|\b[A-Z]-\d+$", text):  # table of contents entries
        return False
    if len(text.split()) > 14 or ";" in text:  # bold list items read as sentences
        return False
    larger = line.size >= body * 1.12
    if NUMBERED.match(text):
        # Numbered list items set in bold read as sentences; headings do not.
        if text.endswith((".", ",", ";", ":")) or re.search(r"[a-z]\. [A-Z]", text):
            return False
        return line.bold or larger
    return larger and line.bold and not text.endswith((".", ",", ";"))


UNNUMBERED = 99


def _chapter(text: str) -> str:
    m = NUMBERED.match(text)
    if not m:
        return ""
    return m.group(1).split(".")[0] if m.group(1) else "Appendix " + m.group(2)


def _level(text: str) -> int:
    """Depth of a heading. Unnumbered headings sit below any numbered one, so the next numbered heading replaces them."""
    m = NUMBERED.match(text)
    if m and m.group(1):
        return m.group(1).count(".") + 1
    return 1 if m else UNNUMBERED


def _split(lines: list[str], max_chars: int, overlap_lines: int) -> list[str]:
    out: list[str] = []
    cur: list[str] = []
    size = 0
    for text in lines:
        if cur and size + len(text) + 1 > max_chars:
            out.append(" ".join(cur))
            cur = cur[-overlap_lines:] if overlap_lines else []
            size = sum(len(t) + 1 for t in cur)
        cur.append(text)
        size += len(text) + 1
    if cur:
        out.append(" ".join(cur))
    return out


def chunk_heading(pages: list[Page], max_chars: int = 1200, min_chars: int = 250, overlap_lines: int = 1) -> list[Chunk]:
    pages = strip_running_lines(pages)
    body = body_font_size(pages)
    chunks: list[Chunk] = []
    stack: list[tuple[int, str]] = []

    def path() -> str:
        return " > ".join(text for _, text in stack)

    for page in pages:
        # A page opens under whatever section was active when the last page ended.
        blocks: list[tuple[str, list[str]]] = [(path(), [])]
        for line in page.lines:
            if is_heading(line, body):
                level = _level(line.text)
                while stack and stack[-1][0] >= level:
                    stack.pop()
                # "3.5 ..." cannot sit under "2. ..." or under an appendix: a section from another chapter starts afresh.
                if stack and level != UNNUMBERED and _chapter(stack[0][1]) != _chapter(line.text):
                    stack.clear()
                stack.append((level, line.text))
                # Start a new block unless the current one is still too small to stand alone.
                if sum(len(t) for t in blocks[-1][1]) >= min_chars:
                    blocks.append((path(), []))
                elif not blocks[-1][1]:
                    blocks[-1] = (path(), [])
            blocks[-1][1].append(line.text)
        for heading, lines in blocks:
            for text in _split(lines, max_chars, overlap_lines):
                if len(text) >= 40:
                    chunks.append(Chunk(page=page.number, heading=heading, text=text))
    return chunks


def chunk_fixed(pages: list[Page], max_chars: int = 1000, overlap: int = 150) -> list[Chunk]:
    chunks: list[Chunk] = []
    for page in pages:
        text = re.sub(r"\s+", " ", page.text).strip()
        start = 0
        while start < len(text):
            piece = text[start : start + max_chars]
            if len(piece) >= 40:
                chunks.append(Chunk(page=page.number, heading="", text=piece))
            if start + max_chars >= len(text):
                break
            start += max_chars - overlap
    return chunks


def chunk_pages(pages: list[Page], strategy: str = "heading", max_chars: int | None = None) -> list[Chunk]:
    if strategy == "heading":
        return chunk_heading(pages, max_chars=max_chars or 1200)
    if strategy == "fixed":
        return chunk_fixed(pages, max_chars=max_chars or 1000)
    raise ValueError(f"unknown chunking strategy: {strategy}")
