# Domain Model

## 1. Core entities and value objects

## Vacancy

Canonical cross-source job entity.

Representative fields:

- internal id;
- title;
- company;
- location;
- remote;
- salary;
- normalized description;
- first_seen_at;
- last_seen_at;
- content_hash;
- observation state;
- expiry state.

The exact schema belongs to implementation, but the semantics above are stable.

## SourceReference

Links one external source record to a canonical Vacancy.

Representative fields:

- source;
- external_id;
- source_url;
- canonical_url if known;
- published_at;
- first_seen_at for this source reference;
- last_seen_at;
- latest source content hash;
- source metadata.

Unique deterministic key where possible:

```text
(source, external_id)
```

## RawObservation

One result observed during one collector run.

It is source-facing and preserves traceability.

## NormalizedVacancyObservation

Source-independent normalized representation consumed by identity and persistence layers.

## CandidateProfile

Structured candidate facts and work-model preferences.

Must not be embedded in collector code.

## SearchPolicy

Deterministic constraints and exception policy.

## ScoreResult

Explainable ranking result.

## Decision / FeedbackEvent

Human outcome such as:

- APPLY
- MAYBE
- SKIP
- APPLIED
- INTERVIEW
- REJECTED
- OFFER

## IngestionRun

Tracks one collection/evaluation execution.

Representative metadata:

- started/finished;
- enabled sources;
- source counts;
- failures;
- new/seen/updated counts;
- scoring/policy versions.

## 2. State separation

Avoid conflating system-observed state with user decision state.

### Observation state

- NEW
- SEEN
- UPDATED
- EXPIRED

### User decision/application state

- NONE
- APPLY
- MAYBE
- SKIP
- APPLIED
- INTERVIEW
- REJECTED
- OFFER

Reports may render a composed label, but storage should preserve both dimensions.

## 3. State transitions

### First observation

```text
absent -> NEW
first_seen_at = now
last_seen_at = now
```

### Re-observation without material change

```text
NEW/SEEN/UPDATED -> SEEN
first_seen_at unchanged
last_seen_at = now
```

### Re-observation with material content change

```text
NEW/SEEN -> UPDATED
first_seen_at unchanged
last_seen_at = now
content_hash changed
```

### Expiry

Source-specific expiry evidence can mark a source reference inactive.

Canonical vacancy expiry should be conservative if multiple references still exist.

## 4. Deduplication rule

Deduplication resolves **observations/references to Vacancy**, never the reverse.

One Vacancy may have many SourceReferences.

False negatives (temporary duplicate entities) are preferable to false-positive merges.

## 5. Evaluation versioning

Each evaluation should store:

- policy version;
- scoring version;
- evaluated timestamp.

This makes later tuning auditable.

## 6. Candidate profile portability

Although the MVP is personal, CandidateProfile and SearchPolicy should be domain objects/configuration so another profile can eventually be substituted without rewriting ingestion or persistence.
