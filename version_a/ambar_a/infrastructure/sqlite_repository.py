"""SQLite implementation of ReadingRepository."""
from __future__ import annotations

import sqlite3

from ..domain.models import Reading


class SqliteRepository:
    def __init__(self, path: str = ":memory:"):
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS readings (ts REAL, node TEXT, kind TEXT, value REAL)"
        )

    def add(self, reading: Reading) -> None:
        self._db.execute(
            "INSERT INTO readings VALUES (?, ?, ?, ?)",
            (reading.ts, reading.node, reading.kind, reading.value),
        )
        self._db.commit()

    def latest(self, kind: str) -> Reading | None:
        row = self._db.execute(
            "SELECT node, kind, value, ts FROM readings WHERE kind = ? ORDER BY ts DESC LIMIT 1",
            (kind,),
        ).fetchone()
        return Reading(*row) if row else None

    def recent(self, limit: int) -> list[Reading]:
        rows = self._db.execute(
            "SELECT node, kind, value, ts FROM readings ORDER BY ts DESC LIMIT ?", (limit,)
        ).fetchall()
        return [Reading(*r) for r in rows]
