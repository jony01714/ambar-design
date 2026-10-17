"""Composition root. Adding a skill or adapter means adding one line here."""
from __future__ import annotations

import os

from .adapters.console import ConsoleAdapter
from .adapters.mqtt import MqttActuator, MqttAdapter
from .adapters.ollama import LocalLlmAdapter
from .adapters.sqlite_store import SqliteEventStore
from .core.bus import EventBus
from .core.registry import DeviceRegistry, ToolRegistry
from .skills.climate import ClimateSkill
from .skills.conversation import ConversationSkill
from .skills.motor import MotorSkill


def main() -> None:
    broker = os.getenv("AMBAR_BROKER", "localhost")
    bus, devices, tools = EventBus(threaded=True), DeviceRegistry(), ToolRegistry()
    SqliteEventStore(bus, os.getenv("AMBAR_DB", "ambar.db"))
    ClimateSkill(bus, {"co2": float(os.getenv("AMBAR_CO2_LIMIT", "1000"))})
    MotorSkill(bus, MqttActuator(broker), devices, tools)
    ConversationSkill(bus, LocalLlmAdapter(), tools)
    MqttAdapter(bus, broker).start()
    try:
        ConsoleAdapter(bus).run()
    finally:
        bus.close()


if __name__ == "__main__":
    main()
