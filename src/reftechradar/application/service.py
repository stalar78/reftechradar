from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from reftechradar.collectors import collect_fixture_observations
from reftechradar.domain.profile import DEFAULT_CANDIDATE_PROFILE
from reftechradar.normalization import normalize_observation
from reftechradar.persistence import SQLiteVacancyRepository
from reftechradar.policy import evaluate_policy
from reftechradar.reporting import ReportItem, build_report, write_json_report, write_markdown_report
from reftechradar.scoring import score_vacancy


@dataclass(frozen=True)
class PipelineResult:
    report: dict
    markdown_path: Path
    json_path: Path


def run_fixture_pipeline(
    db_path: str | Path = "data/reftechradar.sqlite3",
    output_dir: str | Path = "reports",
    cycle: int = 1,
) -> PipelineResult:
    repository = SQLiteVacancyRepository(db_path)
    try:
        observations = collect_fixture_observations(cycle)
        run = repository.start_run(datetime.now(timezone.utc), ("fixture",))
        items: list[ReportItem] = []
        for raw in observations:
            normalized = normalize_observation(raw)
            vacancy = repository.upsert_observation(normalized)
            policy = evaluate_policy(vacancy)
            score = score_vacancy(vacancy, DEFAULT_CANDIDATE_PROFILE, policy)
            items.append(ReportItem(vacancy=vacancy, policy=policy, score=score))
        repository.finish_run(run, [item.vacancy for item in items])
    finally:
        repository.close()

    report = build_report(items)
    output_path = Path(output_dir)
    markdown_path = output_path / f"fixture-cycle-{cycle}.md"
    json_path = output_path / f"fixture-cycle-{cycle}.json"
    write_markdown_report(report, markdown_path)
    write_json_report(report, json_path)
    return PipelineResult(report=report, markdown_path=markdown_path, json_path=json_path)

