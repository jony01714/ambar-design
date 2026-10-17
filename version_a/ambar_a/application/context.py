"""Builds the prompt the language model receives."""
from __future__ import annotations

from ..domain.models import Reading


class ContextBuilder:
    def __init__(self, persona: str = "You are Ambar, a local assistant."):
        self._persona = persona

    def build(self, readings: list[Reading], user_text: str) -> str:
        state = ", ".join(f"{r.node}/{r.kind}={r.value}" for r in readings) or "no readings"
        return f"{self._persona}\nReadings: {state}\nUser: {user_text}"
