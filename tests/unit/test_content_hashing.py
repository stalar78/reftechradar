from dataclasses import replace
from datetime import datetime, timezone

from reftechradar.domain.models import RawObservation
from reftechradar.normalization import normalize_observation
from reftechradar.normalization.hashing import content_hash


def _raw(published_day: int, description: str = "Build internal tools") -> RawObservation:
    return RawObservation(
        source="fixture",
        external_id="hash-1",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        title="Builder",
        company="Co",
        description=description,
        location="Remote",
        remote=True,
        source_url="https://fixture.local/hash-1",
        published_at=datetime(2025, 12, published_day, tzinfo=timezone.utc),
    )


def test_published_at_is_not_material_content() -> None:
    first = normalize_observation(_raw(1))
    second = normalize_observation(_raw(2))

    assert first.content_hash == second.content_hash


def test_material_description_changes_hash() -> None:
    first = normalize_observation(_raw(1))
    changed = replace(first, description="Build internal tools with Codex")

    assert content_hash(first) != content_hash(changed)

