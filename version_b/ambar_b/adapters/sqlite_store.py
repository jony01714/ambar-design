"""Persists every reading seen on the bus."""
from __future__ import annotations

import sqlite3

from ..core.bus import EventBus
from ..core.events import ReadingReceived


class SqliteEventStore:
    def __init__(self, bus: EventBus, path: str = ":memory:"):
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS readings (ts REAL, node TEXT, kind TEXT, value REAL)"
        )
        bus.subscribe(ReadingReceived, self._on_reading)

    def _on_reading(self, event: ReadingReceived) -> None:
        r = event.reading
        self._db.execute("INSERT INTO readings VALUES (?, ?, ?, ?)", (r.ts, r.node, r.kind, r.value))
        self._db.commit()

    def count(self) -> int:
        return self._db.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
