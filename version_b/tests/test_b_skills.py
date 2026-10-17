from ambar_b.adapters.console import ConsoleAdapter
from ambar_b.adapters.sqlite_store import SqliteEventStore
from ambar_b.core.bus import EventBus
from ambar_b.core.events import (
    AlertRaised,
    Command,
    CommandRequested,
    Reading,
    ReadingReceived,
    Reply,
    UserSaid,
)
from ambar_b.core.registry import DeviceRegistry, ToolRegistry
from ambar_b.skills.climate import ClimateSkill
from ambar_b.skills.conversation import ConversationSkill
from ambar_b.skills.motor import MotorSkill


class FakeLlm:
    def __init__(self, answer):
        self.answer, self.prompts = answer, []

    def generate(self, prompt):
        self.prompts.append(prompt)
        return self.answer


class FakeActuator:
    def __init__(self):
        self.sent = []

    def send(self, command):
        self.sent.append(command)


def collect(bus, event_type):
    out = []
    bus.subscribe(event_type, out.append)
    return out


def test_climate_skill_raises_alert():
    bus = EventBus()
    alerts = collect(bus, AlertRaised)
    ClimateSkill(bus, {"co2": 1000})
    bus.publish(ReadingReceived(Reading("n1", "co2", 1500, 1.0)))
    bus.publish(ReadingReceived(Reading("n1", "co2", 700, 2.0)))
    assert len(alerts) == 1 and alerts[0].kind == "co2"


def test_motor_skill_executes_requested_command():
    bus, act = EventBus(), FakeActuator()
    MotorSkill(bus, act, DeviceRegistry(), ToolRegistry())
    bus.publish(CommandRequested(Command("motor1", "on")))
    assert act.sent == [Command("motor1", "on")]


def test_spoken_order_moves_motor_while_replying():
    bus, act = EventBus(), FakeActuator()
    devices, tools = DeviceRegistry(), ToolRegistry()
    MotorSkill(bus, act, devices, tools)
    llm = FakeLlm("TOOL: motor_on\nDone, moving it.")
    ConversationSkill(bus, llm, tools)
    replies = collect(bus, Reply)
    bus.publish(UserSaid("move the motor"))
    assert act.sent == [Command("motor1", "on")]
    assert replies == [Reply("Done, moving it.")]
    assert "motor_on" in llm.prompts[0]
    assert devices.with_capability("motor") == ["motor1"]


def test_conversation_sees_latest_readings():
    bus, tools = EventBus(), ToolRegistry()
    llm = FakeLlm("ok")
    ConversationSkill(bus, llm, tools)
    bus.publish(ReadingReceived(Reading("n1", "temp", 24.0, 1.0)))
    bus.publish(UserSaid("how is it?"))
    assert "n1/temp=24.0" in llm.prompts[0]


def test_store_and_console_adapters():
    bus = EventBus()
    store = SqliteEventStore(bus)
    ClimateSkill(bus, {"co2": 1000})
    out, inputs = [], iter(["hello", "exit"])
    ConsoleAdapter(bus, read=lambda _p: next(inputs), write=out.append).run()
    bus.publish(ReadingReceived(Reading("n1", "co2", 1500, 1.0)))
    assert store.count() == 1
    assert out == ["[ALERT] co2 is 1500, above 1000"]
