"""Intent detection driven by a table instead of if/elif chains."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class Intent(Enum):
    MOTOR_ON = auto()
    MOTOR_OFF = auto()
    AIR_STATUS = auto()
    CHAT = auto()


@dataclass(frozen=True)
class IntentRule:
    intent: Intent
    all_of: tuple[str, ...] = ()
    any_of: tuple[str, ...] = ()

    def matches(self, text: str) -> bool:
        return all(w in text for w in self.all_of) and (
            not self.any_of or any(w in text for w in self.any_of)
        )


DEFAULT_RULES = (
    IntentRule(Intent.MOTOR_ON, all_of=("motor",), any_of=("enciende", "mueve", "start")),
    IntentRule(Intent.MOTOR_OFF, all_of=("motor",), any_of=("apaga", "detén", "stop")),
    IntentRule(Intent.AIR_STATUS, any_of=("co2", "aire", "air")),
)


class IntentRouter:
    def __init__(self, rules: tuple[IntentRule, ...] = DEFAULT_RULES):
        self._rules = rules

    def route(self, text: str) -> Intent:
        lowered = text.lower()
        for rule in self._rules:
            if rule.matches(lowered):
                return rule.intent
        return Intent.CHAT
