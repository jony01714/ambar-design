"""Minimal event bus. Sync mode for tests, threaded mode so handlers never block each other."""
from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any

log = logging.getLogger(__name__)


class EventBus:
    def __init__(self, threaded: bool = False, workers: int = 4):
        self._handlers: dict[type, list[Callable[[Any], None]]] = defaultdict(list)
        self._pool = ThreadPoolExecutor(max_workers=workers) if threaded else None

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: Any) -> None:
        for handler in list(self._handlers[type(event)]):
            if self._pool:
                self._pool.submit(self._safe, handler, event)
            else:
                self._safe(handler, event)

    @staticmethod
    def _safe(handler: Callable[[Any], None], event: Any) -> None:
        try:
            handler(event)
        except Exception:  # one failing skill must not take the assistant down
            log.exception("handler %s failed on %r", handler, event)

    def close(self) -> None:
        if self._pool:
            self._pool.shutdown(wait=True)
