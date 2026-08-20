from __future__ import annotations

import hashlib
import json

from reftechradar.domain.models import NormalizedVacancyObservation


def content_hash(observation: NormalizedVacancyObservation) -> str:
    material = {
        "title": observation.title,
        "company": observation.company,
        "description": observation.description,
        "location": observation.location,
        "remote": observation.remote,
        "salary": observation.salary,
    }
    payload = json.dumps(material, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
