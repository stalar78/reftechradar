from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from reftechradar.domain.models import Classification, ObservationState, PolicyResult, ScoreResult, Vacancy


@dataclass(frozen=True)
class ReportItem:
    vacancy: Vacancy
    policy: PolicyResult
    score: ScoreResult


def build_report(items: list[ReportItem]) -> dict[str, Any]:
    summary = {
        "found": len(items),
        "rejected_automatically": sum(1 for item in items if item.score.classification == Classification.AUTO_REJECT),
        "low_match": sum(1 for item in items if item.score.classification == Classification.LOW_MATCH),
        "maybe": sum(1 for item in items if item.score.classification == Classification.MAYBE),
        "strong_match": sum(1 for item in items if item.score.classification == Classification.STRONG_MATCH),
        "new_strong_match": sum(
            1
            for item in items
            if item.score.classification == Classification.STRONG_MATCH
            and item.vacancy.observation_state == ObservationState.NEW
        ),
    }
    return {"summary": summary, "vacancies": [_item_to_dict(item) for item in items]}


def write_json_report(report: dict[str, Any], path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def write_markdown_report(report: dict[str, Any], path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    lines = ["# RefTechRadar Daily Report", ""]
    summary = report["summary"]
    lines.extend(
        [
            f"Found: {summary['found']}",
            f"Rejected automatically: {summary['rejected_automatically']}",
            f"Low match: {summary['low_match']}",
            f"Maybe: {summary['maybe']}",
            f"Strong Match: {summary['strong_match']}",
            f"New Strong Match: {summary['new_strong_match']}",
            "",
        ]
    )
    for vacancy in report["vacancies"]:
        if vacancy["classification"] == Classification.AUTO_REJECT.value:
            continue
        lines.extend(
            [
                f"## {vacancy['title']} - {vacancy['company']}",
                "",
                f"- Score: {vacancy['score']}",
                f"- Classification: {vacancy['classification']}",
                f"- Observation state: {vacancy['observation_state']}",
                f"- User decision: {vacancy['user_decision']}",
                f"- Source: {vacancy['source_url']}",
                "- Positive reasons:",
            ]
        )
        lines.extend(f"  - {reason}" for reason in vacancy["positive_reasons"])
        lines.append("- Penalties/gaps:")
        if vacancy["penalties_or_gaps"]:
            lines.extend(f"  - {gap}" for gap in vacancy["penalties_or_gaps"])
        else:
            lines.append("  - none material")
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def _item_to_dict(item: ReportItem) -> dict[str, Any]:
    vacancy = item.vacancy
    source = vacancy.source_references[0] if vacancy.source_references else None
    return {
        "id": vacancy.id,
        "title": vacancy.title,
        "company": vacancy.company,
        "score": item.score.total_score,
        "classification": item.score.classification.value,
        "observation_state": vacancy.observation_state.value,
        "user_decision": vacancy.user_decision.value,
        "positive_reasons": [component.reason for component in item.score.positive_components],
        "positive_evidence": [
            {"feature_id": component.feature_id, "points": component.points, "evidence": component.evidence}
            for component in item.score.positive_components
        ],
        "penalties_or_gaps": [component.reason for component in item.score.penalties] + list(item.score.gaps),
        "policy_rules": [
            {
                "rule_id": rule.rule_id,
                "outcome": rule.outcome.value,
                "evidence": rule.evidence,
                "reason": rule.reason,
            }
            for rule in item.policy.rules
        ],
        "source_url": source.source_url if source else None,
    }
