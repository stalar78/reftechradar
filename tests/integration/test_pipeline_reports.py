import json
from pathlib import Path

from reftechradar.application import run_fixture_pipeline
from reftechradar.domain.models import ObservationState


def test_report_outputs_are_generated(tmp_path: Path) -> None:
    result = run_fixture_pipeline(tmp_path / "report.sqlite3", tmp_path / "reports", cycle=1)

    assert result.markdown_path.exists()
    assert result.json_path.exists()
    report = json.loads(result.json_path.read_text(encoding="utf-8"))
    assert report["summary"]["found"] == 6
    assert report["summary"]["rejected_automatically"] == 2
    assert {"title", "company", "score", "classification", "observation_state"} <= set(report["vacancies"][0])
    senior = next(item for item in report["vacancies"] if item["title"] == "Senior Python Backend Developer")
    assert senior["classification"] == "AUTO_REJECT"


def test_end_to_end_two_cycles_new_seen_updated(tmp_path: Path) -> None:
    db_path = tmp_path / "e2e.sqlite3"
    run_fixture_pipeline(db_path, tmp_path / "reports", cycle=1)
    result = run_fixture_pipeline(db_path, tmp_path / "reports", cycle=2)

    states = {item["id"]: item["observation_state"] for item in result.report["vacancies"]}
    assert ObservationState.SEEN.value in states.values()
    assert ObservationState.UPDATED.value in states.values()
    assert result.report["summary"]["found"] == 6
