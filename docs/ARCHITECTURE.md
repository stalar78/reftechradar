# Architecture

## 1. Architecture style

RefTechRadar starts as a **modular monolith** in Python.

Recommended package boundary:

```text
src/reftechradar/
  domain/
  collectors/
  normalization/
  identity/
  persistence/
  policy/
  scoring/
  reporting/
  application/
```

The package names describe responsibility rather than deployment units.

## 2. End-to-end flow

```text
Source Adapter
    |
    v
RawObservation
    |
    v
Normalizer
    |
    v
NormalizedVacancyObservation
    |
    v
Identity Resolver / Deduplicator
    |
    +----> SourceReference
    |
    v
Canonical Vacancy
    |
    v
Persistence + State Transition
    |
    v
Hard Filter Policy
    |
    v
Deterministic Opportunity Score
    |
    v
Classification
    |
    v
Markdown / JSON Report
```

Later:

```text
Shortlisted vacancies
    -> Semantic Review
    -> Application Assistant
```

## 3. Why persistence moves earlier than the original roadmap

Freshness and identity are core product features, not presentation concerns.

Therefore persistence/state should be established **before** real multi-source ingestion grows.

Without stable persistence contracts, the system cannot reliably answer:

- is this vacancy new?
- was it seen before?
- did the content materially change?
- is this another source reference to the same job?

## 4. Data boundaries

### RawObservation

Source-shaped record retained for traceability.

Expected metadata:

- source;
- external id if present;
- discovered URL;
- observed timestamp;
- raw title/company/location/salary/description;
- publisher timestamp if present;
- source-specific metadata.

### NormalizedVacancyObservation

Stable normalized contract used by the rest of the system.

### Vacancy

Canonical cross-source entity.

### SourceReference

A source-specific identity attached to a canonical vacancy.

### Evaluation

Policy/scoring result with structured evidence.

### UserDecision

Human feedback and application lifecycle event.

## 5. Identity strategy

Identity resolution should use layered confidence:

### Layer A — deterministic source identity

`source + external_id`

Highest confidence for recognizing the same source record across runs.

### Layer B — canonical URL identity

Useful when a stable canonical URL exists.

### Layer C — deterministic cross-source fingerprint

Normalized signals such as:

- company;
- title;
- location/remote;
- stable description features;
- salary when useful.

This must be conservative. False merges are more damaging than temporary duplicates.

### Layer D — semantic candidate merge

Not required in the initial MVP. Later used only for ambiguous pairs.

## 6. Freshness strategy

Keep two separate concepts:

- publisher-provided time (`published_at`);
- system-observed time (`first_seen_at`, `last_seen_at`).

`first_seen_at` is the authoritative basis for "new to RefTechRadar".

A material content fingerprint is used for `UPDATED`.

Publisher timestamp changes alone do not imply `NEW`.

## 7. Content hashing

Maintain at least:

- `identity_fingerprint` — conservative fields used in matching;
- `content_hash` — material normalized content for update detection.

Do not hash transient source UI fields.

## 8. State model

Lifecycle states:

- `NEW`
- `SEEN`
- `UPDATED`
- `APPLIED`
- `SKIPPED`
- `EXPIRED`

Important distinction:

`NEW`, `SEEN`, `UPDATED`, `EXPIRED` are primarily system observations.

`APPLIED`, `SKIPPED` are user decisions.

Implementation should avoid a design where a new observation accidentally erases a user decision. The database may therefore represent **observation state** and **user decision state** separately even if reports expose one composed status.

## 9. Policy architecture

Rules must be data-driven and testable.

A policy evaluation returns:

```text
rule_id
outcome
severity
evidence
reason
```

Outcomes can include:

- pass;
- reject;
- penalty;
- boost;
- review-required.

Semantic judgement is allowed only where deterministic evidence is insufficient, and only in a later stage.

## 10. Scoring architecture

Do not encode scoring as a single opaque function or prompt.

Recommended composition:

```text
base score
+ work-model signals
+ experience-flexibility signals
+ product/ownership signals
+ stack compatibility
+ location/remote signals
+ tool signals
- seniority penalties
- experience penalties
- ML specialization penalties
- infrastructure specialization penalties
- language constraints
= bounded score 0..100
```

Every component emits structured evidence.

## 11. Application services

The domain logic should remain independent from CLI and future API/UI layers.

Application services orchestrate use cases such as:

- ingest source observations;
- evaluate newly changed vacancies;
- generate daily digest;
- record user decision.

## 12. Persistence

Initial database: SQLite.

Recommended tables/concepts:

- vacancies;
- source_references;
- source_observations or observation metadata;
- evaluations;
- user_decisions;
- ingestion_runs.

A full historical snapshot table is optional for the earliest slice, but the schema must not prevent adding one.

## 13. Configuration

Separate configuration into:

### Runtime configuration

Database path, output path, log level, enabled sources.

### Candidate profile

Stable facts and preferred working model.

### Search policy

Hard rejects, exceptions, location/language constraints.

### Scoring weights

Versioned deterministic weights and classification thresholds.

Policy/scoring version should be recorded with each evaluation.

## 14. Testing

Minimum test layers:

- domain unit tests;
- normalization contract tests;
- state-transition tests;
- deduplication tests;
- policy rule tests;
- scoring snapshot/golden tests;
- end-to-end fixture pipeline test.

Real-source network tests should not be required for every local test run.

## 15. Observability

MVP logging should make every run auditable:

- source counts;
- normalize failures;
- new/seen/updated counts;
- dedupe merges;
- hard rejects by rule;
- classification counts;
- report output path.

## 16. Security and compliance

Do not store credentials in repository files.

For each source, document:

- acquisition method;
- authentication if any;
- rate constraints;
- ToS/robots considerations;
- failure behavior.

No bypassing anti-bot systems is an architectural requirement.
