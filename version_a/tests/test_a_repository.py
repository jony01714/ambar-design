from ambar_a.domain.models import Reading
from ambar_a.infrastructure.sqlite_repository import SqliteRepository


def test_latest_and_recent_order():
    repo = SqliteRepository(":memory:")
    repo.add(Reading("n", "co2", 800, 1.0))
    repo.add(Reading("n", "co2", 900, 2.0))
    repo.add(Reading("n", "temp", 22, 3.0))
    assert repo.latest("co2").value == 900
    assert [r.kind for r in repo.recent(2)] == ["temp", "co2"]
    assert repo.latest("light") is None
