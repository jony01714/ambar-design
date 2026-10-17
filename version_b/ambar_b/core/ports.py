"""Ports used by skills."""
from __future__ import annotations

from typing import Protocol

from .events import Command


class LanguageModel(Protocol):
    def generate(self, prompt: str) -> str: ...


class Actuator(Protocol):
    def send(self, command: Command) -> None: ...
