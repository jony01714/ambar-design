"""Console channel: publishes UserSaid, prints Reply and AlertRaised."""
from __future__ import annotations

from collections.abc import Callable

from ..core.bus import EventBus
from ..core.events import AlertRaised, Reply, UserSaid


class ConsoleAdapter:
    def __init__(self, bus: EventBus, read: Callable[[str], str] = input,
                 write: Callable[[str], None] = print):
        self._bus, self._read, self._write = bus, read, write
        bus.subscribe(Reply, lambda e: self._write(e.text))
        bus.subscribe(AlertRaised, lambda e: self._write(f"[ALERT] {e.message}"))

    def run(self) -> None:
        while True:
            try:
                text = self._read("> ")
            except EOFError:
                return
            if text.strip().lower() in {"exit", "quit"}:
                return
            self._bus.publish(UserSaid(text))
