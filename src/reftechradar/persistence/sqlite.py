from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from reftechradar.domain.models import (
    FeedbackDecision,
    IngestionRun,
    NormalizedVacancyObservation,
    ObservationState,
    SourceReference,
    Vacancy,
)


class SQLiteVacancyRepository:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.initialize_schema()

    def close(self) -> None:
        self.connection.close()

    def initialize_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                remote INTEGER NOT NULL,
                salary TEXT,
                first_seen_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                observation_state TEXT NOT NULL,
                user_decision TEXT NOT NULL DEFAULT 'NONE'
            );

            CREATE TABLE IF NOT EXISTS source_references (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vacancy_id INTEGER NOT NULL REFERENCES vacancies(id),
                source TEXT NOT NULL,
                external_id TEXT NOT NULL,
                source_url TEXT NOT NULL,
                canonical_url TEXT,
                published_at TEXT,
                first_seen_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                UNIQUE(source, external_id)
            );

            CREATE TABLE IF NOT EXISTS ingestion_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                sources TEXT NOT NULL,
                found_count INTEGER NOT NULL DEFAULT 0,
                new_count INTEGER NOT NULL DEFAULT 0,
                seen_count INTEGER NOT NULL DEFAULT 0,
                updated_count INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        self.connection.commit()

    def start_run(self, started_at: datetime, sources: tuple[str, ...]) -> IngestionRun:
        cursor = self.connection.execute(
            "INSERT INTO ingestion_runs (started_at, sources) VALUES (?, ?)",
            (_dt(started_at), ",".join(sources)),
        )
        self.connection.commit()
        return IngestionRun(id=cursor.lastrowid, started_at=started_at, finished_at=None, sources=sources)

    def finish_run(self, run: IngestionRun, vacancies: list[Vacancy]) -> IngestionRun:
        finished_at = datetime.now(timezone.utc)
        counts = {
            ObservationState.NEW: 0,
            ObservationState.SEEN: 0,
            ObservationState.UPDATED: 0,
        }
        for vacancy in vacancies:
            if vacancy.observation_state in counts:
                counts[vacancy.observation_state] += 1
        self.connection.execute(
            """
            UPDATE ingestion_runs
            SET finished_at = ?, found_count = ?, new_count = ?, seen_count = ?, updated_count = ?
            WHERE id = ?
            """,
            (
                _dt(finished_at),
                len(vacancies),
                counts[ObservationState.NEW],
                counts[ObservationState.SEEN],
                counts[ObservationState.UPDATED],
                run.id,
            ),
        )
        self.connection.commit()
        return IngestionRun(
            id=run.id,
            started_at=run.started_at,
            finished_at=finished_at,
            sources=run.sources,
            found_count=len(vacancies),
            new_count=counts[ObservationState.NEW],
            seen_count=counts[ObservationState.SEEN],
            updated_count=counts[ObservationState.UPDATED],
        )

    def upsert_observation(self, observation: NormalizedVacancyObservation) -> Vacancy:
        ref_row = self.connection.execute(
            """
            SELECT sr.*, v.user_decision, v.first_seen_at AS vacancy_first_seen_at
            FROM source_references sr
            JOIN vacancies v ON v.id = sr.vacancy_id
            WHERE sr.source = ? AND sr.external_id = ?
            """,
            (observation.source, observation.external_id),
        ).fetchone()
        if ref_row is None:
            return self._insert_new(observation)
        return self._update_existing(observation, ref_row)

    def set_user_decision(self, vacancy_id: int, decision: FeedbackDecision) -> None:
        self.connection.execute(
            "UPDATE vacancies SET user_decision = ? WHERE id = ?",
            (decision.value, vacancy_id),
        )
        self.connection.commit()

    def get_by_source(self, source: str, external_id: str) -> Vacancy | None:
        row = self.connection.execute(
            """
            SELECT v.*
            FROM vacancies v
            JOIN source_references sr ON sr.vacancy_id = v.id
            WHERE sr.source = ? AND sr.external_id = ?
            """,
            (source, external_id),
        ).fetchone()
        if row is None:
            return None
        return self._vacancy_from_row(row)

    def _insert_new(self, observation: NormalizedVacancyObservation) -> Vacancy:
        cursor = self.connection.execute(
            """
            INSERT INTO vacancies (
                title, company, description, location, remote, salary, first_seen_at, last_seen_at,
                content_hash, observation_state, user_decision
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                observation.title,
                observation.company,
                observation.description,
                observation.location,
                int(observation.remote),
                observation.salary,
                _dt(observation.observed_at),
                _dt(observation.observed_at),
                observation.content_hash,
                ObservationState.NEW.value,
                FeedbackDecision.NONE.value,
            ),
        )
        vacancy_id = cursor.lastrowid
        self.connection.execute(
            """
            INSERT INTO source_references (
                vacancy_id, source, external_id, source_url, canonical_url, published_at,
                first_seen_at, last_seen_at, content_hash
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                vacancy_id,
                observation.source,
                observation.external_id,
                observation.source_url,
                None,
                _dt_or_none(observation.published_at),
                _dt(observation.observed_at),
                _dt(observation.observed_at),
                observation.content_hash,
            ),
        )
        self.connection.commit()
        return self.get_by_source(observation.source, observation.external_id)  # type: ignore[return-value]

    def _update_existing(self, observation: NormalizedVacancyObservation, ref_row: sqlite3.Row) -> Vacancy:
        state = (
            ObservationState.UPDATED
            if observation.content_hash != ref_row["content_hash"]
            else ObservationState.SEEN
        )
        vacancy_id = int(ref_row["vacancy_id"])
        self.connection.execute(
            """
            UPDATE vacancies
            SET title = ?, company = ?, description = ?, location = ?, remote = ?, salary = ?,
                last_seen_at = ?, content_hash = ?, observation_state = ?
            WHERE id = ?
            """,
            (
                observation.title,
                observation.company,
                observation.description,
                observation.location,
                int(observation.remote),
                observation.salary,
                _dt(observation.observed_at),
                observation.content_hash,
                state.value,
                vacancy_id,
            ),
        )
        self.connection.execute(
            """
            UPDATE source_references
            SET source_url = ?, published_at = ?, last_seen_at = ?, content_hash = ?
            WHERE id = ?
            """,
            (
                observation.source_url,
                _dt_or_none(observation.published_at),
                _dt(observation.observed_at),
                observation.content_hash,
                int(ref_row["id"]),
            ),
        )
        self.connection.commit()
        return self.get_by_source(observation.source, observation.external_id)  # type: ignore[return-value]

    def _vacancy_from_row(self, row: sqlite3.Row) -> Vacancy:
        refs = tuple(
            self._source_ref_from_row(ref)
            for ref in self.connection.execute(
                "SELECT * FROM source_references WHERE vacancy_id = ? ORDER BY id",
                (row["id"],),
            ).fetchall()
        )
        return Vacancy(
            id=int(row["id"]),
            title=row["title"],
            company=row["company"],
            description=row["description"],
            location=row["location"],
            remote=bool(row["remote"]),
            salary=row["salary"],
            first_seen_at=_parse_dt(row["first_seen_at"]),
            last_seen_at=_parse_dt(row["last_seen_at"]),
            content_hash=row["content_hash"],
            observation_state=ObservationState(row["observation_state"]),
            user_decision=FeedbackDecision(row["user_decision"]),
            source_references=refs,
        )

    def _source_ref_from_row(self, row: sqlite3.Row) -> SourceReference:
        return SourceReference(
            id=int(row["id"]),
            vacancy_id=int(row["vacancy_id"]),
            source=row["source"],
            external_id=row["external_id"],
            source_url=row["source_url"],
            canonical_url=row["canonical_url"],
            published_at=_parse_dt_or_none(row["published_at"]),
            first_seen_at=_parse_dt(row["first_seen_at"]),
            last_seen_at=_parse_dt(row["last_seen_at"]),
            content_hash=row["content_hash"],
        )


def _dt(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _dt_or_none(value: datetime | None) -> str | None:
    return _dt(value) if value else None


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _parse_dt_or_none(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None
