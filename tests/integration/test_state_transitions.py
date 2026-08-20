from pathlib import Path

from reftechradar.collectors import collect_fixture_observations
from reftechradar.domain.models import FeedbackDecision, ObservationState
from reftechradar.normalization import normalize_observation
from reftechradar.persistence import SQLiteVacancyRepository


def _ingest_one(repo: SQLiteVacancyRepository, external_id: str, cycle: int):
    raw = [item for item in collect_fixture_observations(cycle) if item.external_id == external_id][0]
    return repo.upsert_observation(normalize_observation(raw))


def test_first_and_second_unchanged_ingestion_states(tmp_path: Path) -> None:
    repo = SQLiteVacancyRepository(tmp_path / "state.sqlite3")
    try:
        first = _ingest_one(repo, "ai-builder-001", 1)
        second = _ingest_one(repo, "ai-builder-001", 2)
    finally:
        repo.close()

    assert first.observation_state == ObservationState.NEW
    assert second.observation_state == ObservationState.SEEN
    assert second.first_seen_at == first.first_seen_at
    assert second.last_seen_at > first.last_seen_at


def test_material_content_change_becomes_updated(tmp_path: Path) -> None:
    repo = SQLiteVacancyRepository(tmp_path / "updated.sqlite3")
    try:
        _ingest_one(repo, "changed-006", 1)
        changed = _ingest_one(repo, "changed-006", 2)
    finally:
        repo.close()

    assert changed.observation_state == ObservationState.UPDATED


def test_published_at_only_change_stays_seen(tmp_path: Path) -> None:
    repo = SQLiteVacancyRepository(tmp_path / "published.sqlite3")
    try:
        _ingest_one(repo, "stack-only-005", 1)
        second = _ingest_one(repo, "stack-only-005", 2)
    finally:
        repo.close()

    assert second.observation_state == ObservationState.SEEN


def test_user_decision_survives_reingestion(tmp_path: Path) -> None:
    repo = SQLiteVacancyRepository(tmp_path / "decision.sqlite3")
    try:
        vacancy = _ingest_one(repo, "ai-builder-001", 1)
        assert vacancy.id is not None
        repo.set_user_decision(vacancy.id, FeedbackDecision.APPLIED)
        second = _ingest_one(repo, "ai-builder-001", 2)
    finally:
        repo.close()

    assert second.user_decision == FeedbackDecision.APPLIED

