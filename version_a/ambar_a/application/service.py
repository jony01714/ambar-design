"""Orchestrates one assistant turn. Depends only on ports and domain objects."""
from __future__ import annotations

from ..domain.models import Alert, Command, Reading
from ..domain.ports import ActuatorPort, LanguageModel, ReadingRepository
from ..domain.rules import RuleEngine
from .context import ContextBuilder
from .intents import Intent, IntentRouter


class AssistantService:
    def __init__(
        self,
        repository: ReadingRepository,
        language_model: LanguageModel,
        actuator: ActuatorPort,
        rules: RuleEngine,
        router: IntentRouter | None = None,
        context: ContextBuilder | None = None,
        motor_id: str = "motor1",
    ):
        self._repo = repository
        self._llm = language_model
        self._actuator = actuator
        self._rules = rules
        self._router = router or IntentRouter()
        self._context = context or ContextBuilder()
        self._motor_id = motor_id

    def on_reading(self, reading: Reading) -> Alert | None:
        self._repo.add(reading)
        return self._rules.evaluate(reading)

    def handle_text(self, text: str) -> str:
        intent = self._router.route(text)
        if intent is Intent.MOTOR_ON:
            self._actuator.send(Command(self._motor_id, "on"))
            return "Moving the motor."
        if intent is Intent.MOTOR_OFF:
            self._actuator.send(Command(self._motor_id, "off"))
            return "Motor stopped."
        if intent is Intent.AIR_STATUS:
            return self._air_status()
        return self._llm.generate(self._context.build(self._repo.recent(10), text))

    def _air_status(self) -> str:
        reading = self._repo.latest("co2")
        if reading is None:
            return "No CO2 readings yet."
        alert = self._rules.evaluate(reading)
        suffix = ", above the limit." if alert else "."
        return f"CO2 is {reading.value} ppm{suffix}"
