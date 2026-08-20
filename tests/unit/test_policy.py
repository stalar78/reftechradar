from datetime import datetime, timezone

from reftechradar.domain.models import FeedbackDecision, ObservationState, Vacancy
from reftechradar.policy import evaluate_policy


def _vacancy(title: str, description: str) -> Vacancy:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return Vacancy(
        id=1,
        title=title,
        company="Co",
        description=description,
        location="Remote",
        remote=True,
        salary=None,
        first_seen_at=now,
        last_seen_at=now,
        content_hash="hash",
        observation_state=ObservationState.NEW,
        user_decision=FeedbackDecision.NONE,
    )


def test_senior_python_false_positive_is_rejected() -> None:
    result = evaluate_policy(
        _vacancy("Senior Python Developer", "5+ years professional Python backend development required.")
    )

    assert result.rejected
    assert any(rule.rule_id == "seniority.clear_mismatch" for rule in result.rules)


def test_ml_heavy_vacancy_is_rejected() -> None:
    result = evaluate_policy(
        _vacancy("ML Specialist Data Scientist", "Model training with PyTorch and TensorFlow.")
    )

    assert result.rejected
    assert any(rule.rule_id == "specialization.ml_core" for rule in result.rules)


def test_middle_three_year_ai_first_case_survives_filtering() -> None:
    result = evaluate_policy(
        _vacancy(
            "Middle AI Automation Developer",
            "Nominal 3 years, practical level by GitHub portfolio, AI-assisted workflow and real projects.",
        )
    )

    assert not result.rejected

