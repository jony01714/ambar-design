"""Environment skill. CO2 and temperature are only the first test case."""
from __future__ import annotations

from ..core.bus import EventBus
from ..core.events import AlertRaised, ReadingReceived


class ClimateSkill:
    def __init__(self, bus: EventBus, limits: dict[str, float]):
        self._bus, self._limits = bus, dict(limits)
        bus.subscribe(ReadingReceived, self._on_reading)

    def _on_reading(self, event: ReadingReceived) -> None:
        r = event.reading
        limit = self._limits.get(r.kind)
        if limit is not None and r.value > limit:
            self._bus.publish(AlertRaised(r.kind, f"{r.kind} is {r.value}, above {limit}"))
