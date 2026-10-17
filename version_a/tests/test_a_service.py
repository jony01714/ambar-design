from ambar_a.application.service import AssistantService
from ambar_a.domain.models import Command, Reading
from ambar_a.domain.rules import RuleEngine
from ambar_a.infrastructure.sqlite_repository import SqliteRepository
from ambar_a.interface.console import ConsoleInterface


class FakeLlm:
    def __init__(self):
        self.prompts = []

    def generate(self, prompt):
        self.prompts.append(prompt)
        return "llm reply"


class FakeActuator:
    def __init__(self):
        self.sent = []

    def send(self, command: Command):
        self.sent.append(command)


def make():
    llm, act = FakeLlm(), FakeActuator()
    service = AssistantService(SqliteRepository(":memory:"), llm, act, RuleEngine({"co2": 1000}))
    return service, llm, act


def test_motor_command_goes_through_port():
    service, _, act = make()
    assert service.handle_text("enciende el motor") == "Moving the motor."
    assert act.sent == [Command("motor1", "on")]


def test_air_status_uses_latest_reading_and_rule():
    service, _, _ = make()
    assert service.handle_text("co2?") == "No CO2 readings yet."
    alert = service.on_reading(Reading("n1", "co2", 1500, 1.0))
    assert alert is not None
    assert service.handle_text("co2?") == "CO2 is 1500.0 ppm, above the limit."


def test_chat_includes_readings_in_prompt():
    service, llm, _ = make()
    service.on_reading(Reading("n1", "temp", 24.0, 1.0))
    assert service.handle_text("hello") == "llm reply"
    assert "n1/temp=24.0" in llm.prompts[0]


def test_console_runs_until_exit():
    service, _, act = make()
    inputs = iter(["enciende el motor", "exit"])
    out = []
    ConsoleInterface(service, read=lambda _p: next(inputs), write=out.append).run()
    assert out == ["Moving the motor."] and len(act.sent) == 1
