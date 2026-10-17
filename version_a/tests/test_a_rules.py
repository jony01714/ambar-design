from ambar_a.domain.models import Reading
from ambar_a.domain.rules import RuleEngine


def test_alert_when_above_limit():
    alert = RuleEngine({"co2": 1000}).evaluate(Reading("n1", "co2", 1200, 0))
    assert alert is not None and alert.kind == "co2"


def test_no_alert_within_limit_or_unknown_kind():
    engine = RuleEngine({"co2": 1000})
    assert engine.evaluate(Reading("n1", "co2", 900, 0)) is None
    assert engine.evaluate(Reading("n1", "temp", 99, 0)) is None


def test_reading_from_mqtt():
    r = Reading.from_mqtt("ambar/node1/co2", b'{"value": 812.5}', 10.0)
    assert (r.node, r.kind, r.value, r.ts) == ("node1", "co2", 812.5, 10.0)
