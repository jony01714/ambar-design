import pytest
from ambar_a.application.intents import Intent, IntentRouter


@pytest.mark.parametrize("text,expected", [
    ("enciende el motor", Intent.MOTOR_ON),
    ("apaga el motor", Intent.MOTOR_OFF),
    ("how is the air?", Intent.AIR_STATUS),
    ("tell me a joke", Intent.CHAT),
])
def test_routes(text, expected):
    assert IntentRouter().route(text) is expected
