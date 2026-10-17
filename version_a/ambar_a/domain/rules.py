"""Threshold rules. One place to change limits, no duplication."""
from __future__ import annotations

from .models import Alert, Reading


class RuleEngine:
    def __init__(self, limits: dict[str, float]):
        self._limits = dict(limits)

    def limit_for(self, kind: str) -> float | None:
        return self._limits.get(kind)

    def evaluate(self, reading: Reading) -> Alert | None:
        limit = self._limits.get(reading.kind)
        if limit is not None and reading.value > limit:
            return Alert(reading.kind, f"{reading.kind} is {reading.value}, above {limit}")
        return None
