"""Ports: what the application needs from the outside world."""
from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from .models import Command, Reading


class SensorFeed(Protocol):
    def subscribe(self, callback: Callable[[Reading], None]) -> None: ...


class ReadingRepository(Protocol):
    def add(self, reading: Reading) -> None: ...
    def latest(self, kind: str) -> Reading | None: ...
    def recent(self, limit: int) -> list[Reading]: ...


class LanguageModel(Protocol):
    def generate(self, prompt: str) -> str: ...


class ActuatorPort(Protocol):
    def send(self, command: Command) -> None: ...
