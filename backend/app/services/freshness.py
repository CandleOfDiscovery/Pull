from datetime import datetime, timezone


def freshness_label(seen_at: datetime, now: datetime | None = None) -> str:
    """Return the deterministic discovery freshness label shown in the UI."""
    now = now or datetime.now(timezone.utc)
    seconds = (now - seen_at).total_seconds()
    if seconds < 3600:
        return "Very Fresh"
    if seconds < 6 * 3600:
        return "Fresh"
    if seconds < 24 * 3600:
        return "Recent"
    if seconds < 3 * 86400:
        return "Older"
    return "Old"
