"""Composition root: the only place that knows every concrete class."""
from __future__ import annotations

from .application.service import AssistantService
from .domain.rules import RuleEngine
from .infrastructure.mqtt import MqttActuator, MqttSensorFeed
from .infrastructure.ollama_llm import OllamaLlm
from .infrastructure.settings import Settings
from .infrastructure.sqlite_repository import SqliteRepository
from .interface.console import ConsoleInterface


def build() -> tuple[AssistantService, MqttSensorFeed]:
    cfg = Settings.from_env()
    service = AssistantService(
        repository=SqliteRepository(cfg.db_path),
        language_model=OllamaLlm(cfg.llm_url, cfg.llm_model),
        actuator=MqttActuator(cfg.broker),
        rules=RuleEngine({"co2": cfg.co2_limit}),
    )
    return service, MqttSensorFeed(cfg.broker)


def main() -> None:
    service, feed = build()
    feed.subscribe(lambda r: (alert := service.on_reading(r)) and print(f"[ALERT] {alert.message}"))
    ConsoleInterface(service).run()


if __name__ == "__main__":
    main()
