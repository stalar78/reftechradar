# Roadmap

## Stage 0 — Foundation and policy lock

**Goal:** establish source-of-truth documentation and prevent product drift.

Deliverables:

- README;
- project blueprint;
- architecture;
- MVP scope;
- candidate profile;
- search policy;
- scoring model v0;
- source strategy;
- architecture decision log;
- repository/package structure;
- configuration conventions.

Exit criteria:

- scope is explicit;
- domain vocabulary is stable enough for coding;
- hard product invariants are documented;
- first vertical slice is defined.

## Stage 1 — Core domain + state contracts

**Goal:** implement the smallest source-independent core.

Deliverables:

- domain models/contracts;
- status and decision model;
- normalized observation contract;
- canonical vacancy/source reference model;
- score/evidence contracts;
- SQLite repository contracts and minimal implementation;
- deterministic content hashing;
- fixture collector;
- tests.

Primary vertical slice:

```text
fixture observations
-> normalize
-> persist
-> identify NEW/SEEN/UPDATED
-> hard filter
-> score
-> Markdown/JSON report
```

Exit criteria:

- two sequential fixture runs prove freshness/state behavior;
- no external source is required to validate the core.

## Stage 2 — First sustainable real collector

**Goal:** prove the source adapter boundary against a real source.

Work:

- source feasibility check;
- adapter;
- rate/error behavior;
- source-specific normalization tests;
- ingestion telemetry.

Exit criteria:

- real vacancies flow through unchanged core contracts.

## Stage 3 — Identity and cross-source deduplication

**Goal:** attach multiple source references to one canonical vacancy conservatively.

Work:

- deterministic fingerprinting;
- matching confidence;
- duplicate-review diagnostics;
- second source integration.

Exit criteria:

- known duplicate fixtures and selected real cases resolve correctly;
- uncertain cases remain separate rather than false-merged.

## Stage 4 — Hard Filter Engine v1

**Goal:** reliably remove obvious mismatches.

Work:

- rule registry;
- seniority;
- strict experience;
- ML specialization;
- enterprise platform specialization;
- mandatory language constraints;
- exception rules.

Exit criteria:

- every reject is explainable;
- golden policy cases pass.

## Stage 5 — Opportunity Score v1

**Goal:** rank survivors by real work-model fit.

Work:

- deterministic feature extraction;
- weight configuration;
- score explanations;
- thresholds;
- scoring golden set.

Exit criteria:

- curated good examples rank above ordinary stack-only matches.

## Stage 6 — Persistence hardening + feedback

**Goal:** make repeated daily operation safe.

Work:

- user decision/event persistence;
- ingestion run records;
- policy/scoring versioning;
- expiration handling;
- migrations.

## Stage 7 — Daily reporting

**Goal:** optimize the actual daily review workflow.

Work:

- daily delta;
- New Strong Match;
- concise cards;
- JSON export;
- CLI ergonomics.

At this point the deterministic MVP can be considered production-usable if its quality gate is met.

## Stage 8 — Semantic AI Review

Only survivors enter semantic review.

Possible outputs:

- nuanced fit;
- acceptable gaps;
- AI-as-marketing vs AI-as-workflow;
- portfolio relevance;
- apply recommendation.

The semantic layer must not replace deterministic state/identity/filtering.

## Stage 9 — Telegram delivery

Digest delivery only after reporting is trusted.

## Stage 10 — Web dashboard

Read-oriented dashboard first; no need to redesign core logic.

## Stage 11 — Application Assistant

Per shortlisted vacancy:

- why it fits;
- risks/gaps;
- portfolio projects to show;
- tailored cover letter;
- probable interview questions.

## Stage 12 — Personal ranking refinement

Use persisted feedback for rule/weight adjustments.

Learning-to-rank is optional and should be justified by enough data.
