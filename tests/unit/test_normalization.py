from datetime import datetime, timezone

from reftechradar.domain.models import RawObservation
from reftechradar.normalization import normalize_observation


def test_normalization_cleans_text_remote_and_url() -> None:
    raw = RawObservation(
        source="Fixture",
        external_id=" x ",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        title="  Python   Developer ",
        company=" Test  Co ",
        description="Build remotely",
        location=" Remote ",
        remote=None,
        source_url="HTTPS://EXAMPLE.COM/jobs/1?utm=x",
    )

    normalized = normalize_observation(raw)

    assert normalized.source == "fixture"
    assert normalized.title == "Python Developer"
    assert normalized.company == "Test Co"
    assert normalized.remote is True
    assert normalized.source_url == "https://example.com/jobs/1"
    assert normalized.content_hash

