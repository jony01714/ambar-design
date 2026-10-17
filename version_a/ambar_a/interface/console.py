"""Console interface. I/O functions are injected so it can be tested."""
from __future__ import annotations

from collections.abc import Callable

from ..application.service import AssistantService


class ConsoleInterface:
    def __init__(self, service: AssistantService,
                 read: Callable[[str], str] = input, write: Callable[[str], None] = print):
        self._service, self._read, self._write = service, read, write

    def run(self) -> None:
        while True:
            try:
                text = self._read("> ")
            except EOFError:
                return
            if text.strip().lower() in {"exit", "quit"}:
                return
            self._write(self._service.handle_text(text))
