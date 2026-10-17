"""MQTT adapters. paho is imported lazily so the rest stays testable offline."""
from __future__ import annotations

import json
import time
from collections.abc import Callable

from ..domain.models import Command, Reading


class MqttSensorFeed:
    def __init__(self, broker: str, topic: str = "ambar/+/+"):
        self._broker, self._topic = broker, topic

    def subscribe(self, callback: Callable[[Reading], None]) -> None:
        import paho.mqtt.client as mqtt

        client = mqtt.Client()
        client.on_message = lambda _c, _u, msg: callback(
            Reading.from_mqtt(msg.topic, msg.payload, time.time())
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
