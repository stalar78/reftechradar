from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class ObservationState(StrEnum):
    NEW = "NEW"
    SEEN = "SEEN"
    UPDATED = "UPDATED"
    EXPIRED = "EXPIRED"


class FeedbackDecision(StrEnum):
    NONE = "NONE"
    APPLY = "APPLY"
    MAYBE = "MAYBE"
    SKIP = "SKIP"
    APPLIED = "APPLIED"
    INTERVIEW = "INTERVIEW"
    REJECTED = "REJECTED"
    OFFER = "OFFER"


class PolicyOutcome(StrEnum):
    PASS = "PASS"
    REJECT = "REJECT"
    PENALTY = "PENALTY"
    BOOST = "BOOST"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class Classification(StrEnum):
    AUTO_REJECT = "AUTO_REJECT"
    LOW_MATCH = "LOW_MATCH"
    MAYBE = "MAYBE"
    STRONG_MATCH = "STRONG_MATCH"


@dataclass(frozen=True)
class RawObservation:
    source: str
    external_id: str
    observed_at: datetime
    title: str
    company: str
    description: str
    location: str
    remote: str | bool | None
    source_url: str
    published_at: datetime | None = None
    salary: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NormalizedVacancyObservation:
    source: str
    external_id: str
    observed_at: datetime
    title: str
    company: str
    description: str
    location: str
    remote: bool
    source_url: str
    published_at: datetime | None = None
    salary: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    content_hash: str = ""


@dataclass(frozen=True)
class SourceReference:
    id: int | None
    vacancy_id: int
    source: str
    external_id: str
    source_url: str
    canonical_url: str | None
    published_at: datetime | None
    first_seen_at: datetime
    last_seen_at: datetime
    content_hash: str


@dataclass(frozen=True)
class Vacancy:
    id: int | None
    title: str
    company: str
    description: str
    location: str
    remote: bool
    salary: str | None
    first_seen_at: datetime
    last_seen_at: datetime
    content_hash: str
    observation_state: ObservationState
    user_decision: FeedbackDecision = FeedbackDecision.NONE
    source_references: tuple[SourceReference, ...] = ()


@dataclass(frozen=True)
class CandidateProfile:
    languages: tuple[str, ...]
    frontend: tuple[str, ...]
    backend: tuple[str, ...]
    data: tuple[str, ...]
    qa: tuple[str, ...]
    infrastructure: tuple[str, ...]
    primary_ai_tools: tuple[str, ...]
    positive_work_model_terms: tuple[str, ...]


@dataclass(frozen=True)
class RuleEvidence:
    rule_id: str
    outcome: PolicyOutcome
    evidence: tuple[str, ...]
    reason: str
    severity: str = "info"


@dataclass(frozen=True)
class PolicyResult:
    classification: Classification
    rules: tuple[RuleEvidence, ...]

    @property
    def rejected(self) -> bool:
        return self.classification == Classification.AUTO_REJECT


@dataclass(frozen=True)
class ScoreComponent:
    feature_id: str
    points: int
    evidence: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class ScoreResult:
    total_score: int
    classification: Classification
    scoring_version: str
    positive_components: tuple[ScoreComponent, ...]
    penalties: tuple[ScoreComponent, ...] = ()
    gaps: tuple[str, ...] = ()
    summary: str = ""


@dataclass(frozen=True)
class IngestionRun:
    id: int | None
    started_at: datetime
    finished_at: datetime | None
    sources: tuple[str, ...]
    found_count: int = 0
    new_count: int = 0
    seen_count: int = 0
    updated_count: int = 0
