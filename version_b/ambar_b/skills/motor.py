"""Motor skill: executes commands and exposes motor actions as tools for the model."""
from __future__ import annotations

from ..core.bus import EventBus
from ..core.events import Command, CommandRequested
from ..core.ports import Actuator
from ..core.registry import DeviceRegistry, ToolRegistry


class MotorSkill:
    def __init__(self, bus: EventBus, actuator: Actuator, devices: DeviceRegistry,
                 tools: ToolRegistry, motor_id: str = "motor1"):
        self._actuator = actuator
        devices.register(motor_id, {"motor"})
        bus.subscribe(CommandRequested, self._on_command)
        for action, text in (("on", "Start the motor"), ("off", "Stop the motor")):
            tools.register(
                f"motor_{action}", text,
                lambda a=action: bus.publish(CommandRequested(Command(motor_id, a))),
            )

    def _on_command(self, event: CommandRequested) -> None:
        self._actuator.send(event.command)
