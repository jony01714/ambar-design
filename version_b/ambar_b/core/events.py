"""Event and value types shared by the whole system."""
from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Reading:
    node: str
    kind: str
    value: float
    ts: float

    @classmethod
    def from_mqtt(cls, topic: str, payload: bytes, ts: float) -> Reading:
        _, node, kind = topic.split("/")
        return cls(node, kind, float(json.loads(payload)["value"]), ts)


@dataclass(frozen=True)
class Command:
    device: str
    action: str


@dataclass(frozen=True)
class ReadingReceived:
    reading: Reading


@dataclass(frozen=True)
class UserSaid:
    text: str


@dataclass(frozen=True)
class CommandRequested:
    command: Command


@dataclass(frozen=True)
class AlertRaised:
    kind: str
    message: str


@dataclass(frozen=True)
class Reply:
    text: str
