from __future__ import annotations

from reftechradar.domain.models import (
    CandidateProfile,
    Classification,
    PolicyResult,
    ScoreComponent,
    ScoreResult,
    Vacancy,
)

SCORING_VERSION = "v0.1"


def score_vacancy(vacancy: Vacancy, profile: CandidateProfile, policy: PolicyResult) -> ScoreResult:
    if policy.rejected:
        return ScoreResult(
            total_score=0,
            classification=Classification.AUTO_REJECT,
            scoring_version=SCORING_VERSION,
            positive_components=(),
            penalties=tuple(
                ScoreComponent(rule.rule_id, 0, rule.evidence, rule.reason)
                for rule in policy.rules
                if rule.outcome.value == "REJECT"
            ),
            summary="Rejected by deterministic hard filter.",
        )

    text = _text(vacancy)
    positives = tuple(
        component
        for component in (
            _component("ai_first_working_model", 30, text, ("coding agents", "ai-first", "ai-assisted", "codex", "copilot", "chatgpt")),
            _component("experience_flexibility_portfolio", 20, text, ("portfolio", "github", "real projects", "practical level", "more than formal years", "junior", "middle")),
            _component("builder_ownership_product_delivery", 20, text, ("end-to-end", "ownership", "mvp", "product builder", "independently", "full cycle")),
            _component("internal_tools_automation_integrations", 15, text, ("internal tools", "business automation", "workflow automation", "api integrations", "internal services")),
            _stack_component(profile, text),
            _component("logistics_tool_bonus", 5, text, ("remote russia", "remote", "codex", "copilot", "cursor")),
        )
        if component.points > 0
    )
    penalties = _penalties(policy)
    raw_score = sum(component.points for component in positives) - sum(component.points for component in penalties)
    total = max(0, min(100, raw_score))
    classification = _classify(total)
    gaps = _gaps(text)
    return ScoreResult(
        total_score=total,
        classification=classification,
        scoring_version=SCORING_VERSION,
        positive_components=positives,
        penalties=penalties,
        gaps=gaps,
        summary=f"{classification.value} - {total}/100",
    )


def _component(feature_id: str, maximum: int, text: str, terms: tuple[str, ...]) -> ScoreComponent:
    evidence = tuple(term for term in terms if term in text)
    if not evidence:
        return ScoreComponent(feature_id, 0, (), "No material signal found.")
    ratio = min(1.0, len(evidence) / 3)
    points = max(1, round(maximum * ratio))
    return ScoreComponent(feature_id, points, evidence, f"{feature_id.replace('_', ' ')} evidence found.")


def _stack_component(profile: CandidateProfile, text: str) -> ScoreComponent:
    stack_terms = profile.languages + profile.frontend + profile.backend + profile.data + profile.qa + profile.infrastructure
    evidence = tuple(dict.fromkeys(term for term in stack_terms if term in text))
    points = min(10, len(evidence) * 2)
    return ScoreComponent(
        "stack_compatibility",
        points,
        evidence,
        "Compatible stack overlap is capped so it cannot dominate ranking.",
    )


def _penalties(policy: PolicyResult) -> tuple[ScoreComponent, ...]:
    components: list[ScoreComponent] = []
    for rule in policy.rules:
        if rule.outcome.value == "PENALTY":
            components.append(ScoreComponent(rule.rule_id, 10, rule.evidence, rule.reason))
        if rule.outcome.value == "REVIEW_REQUIRED":
            components.append(ScoreComponent(rule.rule_id, 3, rule.evidence, rule.reason))
    return tuple(components)


def _classify(score: int) -> Classification:
    if score >= 80:
        return Classification.STRONG_MATCH
    if score >= 60:
        return Classification.MAYBE
    return Classification.LOW_MATCH


def _gaps(text: str) -> tuple[str, ...]:
    gaps: list[str] = []
    if "ai" not in text and "codex" not in text and "copilot" not in text:
        gaps.append("No clear AI-first workflow signal.")
    if "portfolio" not in text and "github" not in text and "real projects" not in text:
        gaps.append("No portfolio-first hiring signal.")
    return tuple(gaps)


def _text(vacancy: Vacancy) -> str:
    return f"{vacancy.title} {vacancy.company} {vacancy.description} {vacancy.location}".lower()
