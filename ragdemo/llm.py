"""A minimal client for OpenAI-compatible chat completions, with token counting and a spend cap."""

from __future__ import annotations

import time
from dataclasses import dataclass

import httpx


class BudgetExceeded(RuntimeError):
    pass


class LLMError(RuntimeError):
    pass


MODEL_ERRORS: tuple[type[Exception], ...] = (LLMError,)  # what a failed model call raises; the API turns these into a 502


@dataclass
class Spend:
    """Counts tokens reported by the API and stops the run when the estimated cost passes the cap."""

    price_input_per_m: float
    price_output_per_m: float
    max_usd: float
    input_tokens: int = 0
    output_tokens: int = 0
    calls: int = 0

    @property
    def usd(self) -> float:
        return (self.input_tokens * self.price_input_per_m + self.output_tokens * self.price_output_per_m) / 1_000_000

    def add(self, input_tokens: int, output_tokens: int) -> None:
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.calls += 1

    def check(self) -> None:
        if self.usd >= self.max_usd:
            raise BudgetExceeded(f"estimated spend ${self.usd:.4f} reached the cap of ${self.max_usd:.2f}")

    def report(self) -> dict:
        return {
            "calls": self.calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "estimated_usd": round(self.usd, 4),
            "price_input_per_m": self.price_input_per_m,
            "price_output_per_m": self.price_output_per_m,
        }


class ChatClient:
    def __init__(self, api_key: str, base_url: str, model: str, spend: Spend, client: httpx.Client | None = None) -> None:
        self.model = model
        self.spend = spend
        self._url = base_url.rstrip("/") + "/chat/completions"
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self._client = client or httpx.Client(timeout=60)

    def _post(self, payload: dict) -> dict:
        """One request, retried on rate limits and server errors. Error messages never include the key."""
        attempts = 4
        for attempt in range(attempts):
            last = attempt == attempts - 1
            try:
                response = self._client.post(self._url, json=payload, headers=self._headers)
            except httpx.TransportError as error:  # timeouts and connection failures
                if last:
                    raise LLMError(f"chat request failed: {type(error).__name__}") from error
                time.sleep(2**attempt)
                continue
            if response.status_code == 200:
                return response.json()
            try:
                error = response.json().get("error", {})
            except ValueError:
                error = {}
            out_of_credit = error.get("type") == "insufficient_quota"
            if response.status_code in (429, 500, 502, 503) and not out_of_credit and not last:
                time.sleep(2**attempt)
                continue
            raise LLMError(f"chat request failed with status {response.status_code}: {error.get('message', 'no error message')}")
        raise LLMError("chat request failed")  # not reached: the last attempt returns or raises

    def complete(self, system: str, user: str, json_reply: bool = False, max_tokens: int = 400) -> str:
        self.spend.check()
        payload = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        }
        if json_reply:
            payload["response_format"] = {"type": "json_object"}
        data = self._post(payload)
        usage = data.get("usage", {})
        self.spend.add(usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))
        try:
            return (data["choices"][0]["message"]["content"] or "").strip()
        except (KeyError, IndexError, TypeError) as error:
            raise LLMError("chat reply had no message content") from error
