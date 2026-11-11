"""The answer step, behind one interface with two providers.

ExtractiveAnswerer needs no key: it returns the best passages word for word,
each with its document and page. OpenAICompatAnswerer sends the passages to any
OpenAI-compatible chat completions endpoint and asks for an answer that cites
passages by number.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

import httpx

from .store import Hit

REFUSAL = "I could not find this in the documents."


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
    "Cite the passages you used with their numbers in square brackets, for example [1]. "
    "Do not use any knowledge that is not in the passages. "
    f'If the passages do not contain the answer, reply with exactly: "{REFUSAL}"'
)


class OpenAICompatAnswerer:
    mode = "generated"

    def __init__(self, api_key: str, base_url: str, model: str, client: httpx.Client | None = None) -> None:
        self.model = model
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.client = client or httpx.Client(timeout=60)
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def answer(self, question: str, passages: list[Hit]) -> Answer:
        context = "\n\n".join(
            f"[{i}] {hit.title}, page {hit.page}\n{hit.text}" for i, hit in enumerate(passages, start=1)
        )
        payload = {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Passages:\n\n{context}\n\nQuestion: {question}"},
            ],
        }
        response = self.client.post(self.url, json=payload, headers=self.headers)
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if REFUSAL.lower().rstrip(".") in text.lower():
            return Answer(text=REFUSAL, cited=[], refused=True)
        cited = sorted({int(n) - 1 for n in re.findall(r"\[(\d+)\]", text) if 0 < int(n) <= len(passages)})
        # An answer that cites nothing cannot be checked, so it is not passed on.
        if not cited:
            return Answer(text=REFUSAL, cited=[], refused=True)
        return Answer(text=text, cited=cited)


def make_answerer(api_key: str, base_url: str, model: str) -> Answerer:
    if api_key:
        return OpenAICompatAnswerer(api_key, base_url, model)
    return ExtractiveAnswerer()
