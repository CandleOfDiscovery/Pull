from datetime import datetime, timedelta, timezone

from app.services.freshness import freshness_label


def test_freshness_boundaries() -> None:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert freshness_label(now - timedelta(minutes=59), now) == "Very Fresh"
    assert freshness_label(now - timedelta(hours=2), now) == "Fresh"
    assert freshness_label(now - timedelta(days=4), now) == "Old"
