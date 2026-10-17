"""MQTT adapters. paho is imported lazily to keep the core testable offline."""
from __future__ import annotations

import json
import time

from ..core.bus import EventBus
from ..core.events import Command, Reading, ReadingReceived


class MqttAdapter:
    def __init__(self, bus: EventBus, broker: str, topic: str = "ambar/+/+"):
        self._bus, self._broker, self._topic = bus, broker, topic

    def start(self) -> None:
        import paho.mqtt.client as mqtt

        client = mqtt.Client()
        client.on_message = lambda _c, _u, msg: self._bus.publish(
            ReadingReceived(Reading.from_mqtt(msg.topic, msg.payload, time.time()))
        )
        client.connect(self._broker, 1883)
        client.subscribe(self._topic)
        client.loop_start()


class MqttActuator:
    def __init__(self, broker: str):
        import paho.mqtt.client as mqtt

        self._client = mqtt.Client()
        self._client.connect(broker, 1883)
        self._client.loop_start()

    def send(self, command: Command) -> None:
        self._client.publish(f"ambar/{command.device}/cmd", json.dumps({"action": command.action}))
