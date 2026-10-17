from ambar_b.core.bus import EventBus
from ambar_b.core.events import UserSaid


def test_publish_reaches_subscribers_and_isolates_failures():
    bus, seen = EventBus(), []

    def boom(_e):
        raise RuntimeError("bad skill")

    bus.subscribe(UserSaid, boom)
    bus.subscribe(UserSaid, lambda e: seen.append(e.text))
    bus.publish(UserSaid("hi"))
    assert seen == ["hi"]


def test_threaded_bus_delivers():
    bus, seen = EventBus(threaded=True), []
    bus.subscribe(UserSaid, lambda e: seen.append(e.text))
    bus.publish(UserSaid("hi"))
    bus.close()
    assert seen == ["hi"]
