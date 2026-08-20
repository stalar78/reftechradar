from __future__ import annotations

from dataclasses import replace
from urllib.parse import urlsplit, urlunsplit

from reftechradar.domain.models import NormalizedVacancyObservation, RawObservation
from reftechradar.normalization.hashing import content_hash


def normalize_observation(raw: RawObservation) -> NormalizedVacancyObservation:
    normalized = NormalizedVacancyObservation(
        source=_clean_text(raw.source).lower(),
        external_id=_clean_text(raw.external_id),
        observed_at=raw.observed_at,
        title=_clean_text(raw.title),
        company=_clean_text(raw.company),
        description=_clean_text(raw.description),
        location=_clean_text(raw.location),
        remote=_normalize_remote(raw.remote, raw.location, raw.description),
        source_url=_normalize_url(raw.source_url),
        published_at=raw.published_at,
        salary=_clean_text(raw.salary) if raw.salary else None,
        metadata=dict(raw.metadata),
    )
    return replace(normalized, content_hash=content_hash(normalized))


def _clean_text(value: str) -> str:
    return " ".join(value.strip().split())


def _normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    scheme = parts.scheme.lower() or "https"
    netloc = parts.netloc.lower()
    path = parts.path.rstrip("/")
    return urlunsplit((scheme, netloc, path, parts.query, ""))


def _normalize_remote(value: str | bool | None, location: str, description: str) -> bool:
    if isinstance(value, bool):
        return value
    haystack = f"{value or ''} {location} {description}".lower()
    return any(term in haystack for term in ("remote", "удален", "удалён", "remotely"))
