"""Domain entities. No I/O and no third-party imports."""
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
        """Parse topic ``ambar/<node>/<kind>`` and a JSON payload ``{"value": x}``."""
        _, node, kind = topic.split("/")
        return cls(node=node, kind=kind, value=float(json.loads(payload)["value"]), ts=ts)


@dataclass(frozen=True)
class Command:
    device: str
    action: str


@dataclass(frozen=True)
class Alert:
    kind: str
    message: str
