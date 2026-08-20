from __future__ import annotations

import re

from reftechradar.domain.models import (
    Classification,
    PolicyOutcome,
    PolicyResult,
    RuleEvidence,
    Vacancy,
)

POLICY_VERSION = "v0.1"


def evaluate_policy(vacancy: Vacancy) -> PolicyResult:
    text = _text(vacancy)
    rules = [
        _seniority_rule(vacancy, text),
        _ml_specialist_rule(vacancy, text),
        _experience_rule(vacancy, text),
    ]
    active = tuple(rule for rule in rules if rule is not None)
    rejected = any(rule.outcome == PolicyOutcome.REJECT for rule in active)
    return PolicyResult(
        classification=Classification.AUTO_REJECT if rejected else Classification.LOW_MATCH,
        rules=active,
    )


def _seniority_rule(vacancy: Vacancy, text: str) -> RuleEvidence | None:
    title = vacancy.title.lower()
    patterns = {
        "Senior": r"\bsenior\b",
        "Lead": r"\blead\b",
        "Principal": r"\bprincipal\b",
        "Staff Engineer": r"\bstaff\s+engineer\b",
    }
    evidence = tuple(label for label, pattern in patterns.items() if re.search(pattern, title))
    if not evidence:
        return None
    return RuleEvidence(
        rule_id="seniority.clear_mismatch",
        outcome=PolicyOutcome.REJECT,
        evidence=evidence,
        reason="Clear Senior/Lead/Principal/Staff mismatch for the target profile.",
        severity="high",
    )


def _ml_specialist_rule(vacancy: Vacancy, text: str) -> RuleEvidence | None:
    terms = ("data scientist", "ml specialist", "model training", "pytorch", "tensorflow")
    evidence = tuple(term for term in terms if term in text)
    if len(evidence) >= 2 or "data scientist" in evidence or "ml specialist" in evidence:
        return RuleEvidence(
            rule_id="specialization.ml_core",
            outcome=PolicyOutcome.REJECT,
            evidence=evidence,
            reason="Core ML/Data Science specialization is outside the target profile.",
            severity="high",
        )
    return None


def _experience_rule(vacancy: Vacancy, text: str) -> RuleEvidence | None:
    strict_years = _years_required(text)
    if strict_years < 4:
        if strict_years == 3 and _has_exception_signals(text):
            return RuleEvidence(
                rule_id="experience.nominal_three_years_exception",
                outcome=PolicyOutcome.REVIEW_REQUIRED,
                evidence=(f"{strict_years}+ years",) + _exception_evidence(text),
                reason="Nominal 3 years is preserved for review because strong practical/AI-first signals exist.",
            )
        return None
    return RuleEvidence(
        rule_id="experience.strict_mismatch",
        outcome=PolicyOutcome.REJECT,
        evidence=(f"{strict_years}+ years",),
        reason="Strict 4+ years professional experience requirement is a hard mismatch.",
        severity="high",
    )


def _years_required(text: str) -> int:
    patterns = (
        r"(\d+)\s*\+?\s+years?\s+(?:of\s+)?(?:professional\s+)?(?:development|developer|engineering|backend|frontend|commercial)\b",
        r"(?:require(?:d|s)?|must\s+have|need(?:s|ed)?)\s+(\d+)\s*\+?\s+years?",
    )
    matches: list[str] = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, text))
    return max((int(match) for match in matches), default=0)


def _has_exception_signals(text: str) -> bool:
    return bool(_exception_evidence(text))


def _exception_evidence(text: str) -> tuple[str, ...]:
    terms = (
        "portfolio",
        "github",
        "real projects",
        "practical level",
        "ai-first",
        "ai-assisted",
        "coding agents",
        "projects over formal experience",
        "more than formal years",
    )
    return tuple(term for term in terms if term in text)


def _text(vacancy: Vacancy) -> str:
    return f"{vacancy.title} {vacancy.company} {vacancy.description} {vacancy.location}".lower()
