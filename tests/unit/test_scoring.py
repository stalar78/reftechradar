from reftechradar.collectors import collect_fixture_observations
from reftechradar.domain.profile import DEFAULT_CANDIDATE_PROFILE
from reftechradar.domain.models import FeedbackDecision, ObservationState, Vacancy
from reftechradar.normalization import normalize_observation
from reftechradar.policy import evaluate_policy
from reftechradar.scoring import score_vacancy


def _vacancy_from_fixture(external_id: str) -> Vacancy:
    normalized = [
        normalize_observation(raw)
        for raw in collect_fixture_observations(1)
        if raw.external_id == external_id
    ][0]
    return Vacancy(
        id=1,
        title=normalized.title,
        company=normalized.company,
        description=normalized.description,
        location=normalized.location,
        remote=normalized.remote,
        salary=normalized.salary,
        first_seen_at=normalized.observed_at,
        last_seen_at=normalized.observed_at,
        content_hash=normalized.content_hash,
        observation_state=ObservationState.NEW,
        user_decision=FeedbackDecision.NONE,
    )


def test_strong_ai_first_fixture_scores_above_stack_only() -> None:
    strong = _vacancy_from_fixture("ai-builder-001")
    stack_only = _vacancy_from_fixture("stack-only-005")

    strong_score = score_vacancy(strong, DEFAULT_CANDIDATE_PROFILE, evaluate_policy(strong))
    stack_score = score_vacancy(stack_only, DEFAULT_CANDIDATE_PROFILE, evaluate_policy(stack_only))

    assert strong_score.total_score > stack_score.total_score
    assert strong_score.classification.value == "STRONG_MATCH"
    assert stack_score.total_score <= 35

