# MVP Scope

## 1. MVP objective

Produce a trustworthy daily shortlist of **new or materially updated vacancies** that fit the candidate's AI-first builder profile.

## 2. In scope

### Acquisition

- source adapter abstraction;
- fixture collector for deterministic development;
- one sustainable real source after core contracts are stable;
- second source before MVP completion to prove cross-source deduplication.

### Domain

- canonical vacancy;
- source references;
- normalized observation;
- evaluation;
- user decision;
- ingestion run.

### State

- `first_seen_at`;
- `last_seen_at`;
- content hash;
- new/seen/updated detection;
- applied/skipped lifecycle preservation.

### Filtering

- deterministic hard rejects;
- configurable exceptions;
- explainable rule evidence.

### Scoring

- deterministic Opportunity Score;
- versioned weights;
- classification;
- positive evidence and gaps.

### Reporting

- CLI summary;
- Markdown daily digest;
- machine-readable JSON output.

### Feedback

- persist at least `APPLY/MAYBE/SKIP/APPLIED/INTERVIEW/REJECTED/OFFER` as user feedback/events;
- early MVP ranking does not need ML learning.

## 3. Explicitly out of scope

- dashboard;
- Telegram bot;
- automatic applications;
- resume autofill;
- multi-user accounts;
- SaaS billing;
- learning-to-rank;
- embeddings as core identity logic;
- LLM-only ranking;
- high-scale distributed ingestion;
- aggressive scraping;
- international-first sourcing.

## 4. MVP Definition of Done

The MVP is done when all statements below are true.

### Ingestion and identity

- at least two source adapters are supported, including one source pair capable of exposing duplicate jobs;
- one vacancy can hold multiple source references;
- rerunning ingestion does not create duplicate canonical vacancies for unchanged source records;
- conservative cross-source deduplication is implemented and tested.

### Freshness

- `first_seen_at` never changes after initial discovery;
- a publisher date change alone cannot turn an existing vacancy into `NEW`;
- material normalized-content changes produce `UPDATED`;
- unchanged observations become/remain `SEEN`.

### Filtering

- core hard rejects from `SEARCH_POLICY.md` are represented as explicit rules;
- every automatic rejection identifies the rule and evidence;
- ambiguous "middle / 3 years" cases are not blindly rejected if configured exception signals apply.

### Scoring

- scoring is deterministic for the same input/profile/policy version;
- score is bounded 0..100;
- every score has component-level explanations;
- thresholds map to at least `REJECTED`, `LOW_MATCH`, `MAYBE`, `STRONG_MATCH`;
- strong work-model signals weigh more than raw technology overlap.

### Reporting

- one command/use case produces a Markdown and JSON report;
- report includes found/rejected/low/maybe/strong/new-strong counts;
- top cards contain score, reasons, gaps, freshness state and source URLs.

### Feedback

- user decisions can be persisted without breaking observation freshness;
- previously applied/skipped vacancies remain distinguishable on later ingestion.

### Quality

- domain/state/policy/scoring/deduplication tests pass;
- one fixture-based end-to-end test covers two ingestion runs and verifies new/seen/updated behavior;
- architecture and scoring documentation match implementation.

## 5. MVP success metric

The system is useful when its daily top shortlist is small enough to review manually and the user can understand **why each vacancy is present or absent** without reading internal code.
