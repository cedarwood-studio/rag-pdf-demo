"""The answer step, behind one interface with two providers.

ExtractiveAnswerer needs no key: it returns the best passages word for word,
each with its document and page. GeneratedAnswerer sends the passages to an
OpenAI-compatible chat model and asks for an answer that cites passages by
number. A generated answer that cites nothing is turned into a refusal.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

from .llm import ChatClient
from .refusal import REFUSAL
from .store import Hit


@dataclass
class Answer:
    text: str
    cited: list[int]  # indexes into the passages given to the answerer
    refused: bool = False


class Answerer(Protocol):
    mode: str

    def answer(self, question: str, passages: list[Hit]) -> Answer: ...


class ExtractiveAnswerer:
    mode = "extractive"

    def answer(self, question: str, passages: list[Hit]) -> Answer:
        parts = ["The closest passages in the documents, quoted as written:"]
        for i, hit in enumerate(passages, start=1):
            parts.append(f"[{i}] {hit.title}, page {hit.page}:\n{hit.text}")
        return Answer(text="\n\n".join(parts), cited=list(range(len(passages))))


SYSTEM_PROMPT = (
    "You answer questions for a support team using only the numbered passages provided. "
    "Answer in one to three sentences. "
    "Cite every passage you used with its number in square brackets, for example [1]. "
    "Do not use any knowledge that is not in the passages. "
    "If the passages do not state the answer, even if they are on the same subject, "
    f'reply with exactly: "{REFUSAL}"'
)


def format_passages(passages: list[Hit]) -> str:
    return "\n\n".join(f"[{i}] {hit.title}, page {hit.page}\n{hit.text}" for i, hit in enumerate(passages, start=1))


def parse_reply(text: str, n_passages: int) -> Answer:
    if REFUSAL.lower().rstrip(".") in text.lower():
        return Answer(text=REFUSAL, cited=[], refused=True)
    cited = sorted({int(n) - 1 for n in re.findall(r"\[(\d+)\]", text) if 0 < int(n) <= n_passages})
    # An answer that cites nothing cannot be checked, so it is not passed on.
    if not cited:
        return Answer(text=REFUSAL, cited=[], refused=True)
    return Answer(text=text, cited=cited)


class GeneratedAnswerer:
    mode = "generated"

    def __init__(self, chat: ChatClient) -> None:
        self.chat = chat

    def answer(self, question: str, passages: list[Hit]) -> Answer:
        reply = self.chat.complete(SYSTEM_PROMPT, f"Passages:\n\n{format_passages(passages)}\n\nQuestion: {question}")
        return parse_reply(reply, len(passages))
