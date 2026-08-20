from reftechradar.domain.models import NormalizedVacancyObservation


def same_source_key(observation: NormalizedVacancyObservation) -> tuple[str, str]:
    return observation.source, observation.external_id
