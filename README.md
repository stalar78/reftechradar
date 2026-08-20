# RefTechRadar

RefTechRadar is a personal job-intelligence system that finds, normalizes, deduplicates, tracks and ranks vacancies against a **real working profile**, not merely a keyword stack.

The initial target profile is an AI-first builder / AI-assisted developer / product engineer who uses coding agents to take a business task from requirements through architecture, implementation review, testing, documentation and deployment.

## Product thesis

The system should answer one question well:

> Out of all newly discovered vacancies, which few are genuinely worth applying to?

The core product value is:

1. reliable ingestion;
2. persistent vacancy identity and freshness;
3. cross-source deduplication;
4. deterministic hard filtering;
5. explainable personal scoring;
6. concise reporting.

LLM-based semantic review is deliberately **not** part of the critical path of the first MVP.

## MVP pipeline

```text
collect
  -> raw observation
  -> normalize
  -> resolve identity / deduplicate
  -> persist state
  -> hard filter
  -> deterministic score
  -> classify
  -> report
```

## MVP output

The first useful interface is CLI + Markdown/JSON reports.

Example:

```text
RefTechRadar — Daily Report

Found: 137
Rejected automatically: 102
Low match: 24
Maybe: 7
Strong Match: 4
New Strong Match: 3
```

Each shortlisted vacancy must include:

- score;
- classification;
- positive evidence;
- penalties / gaps;
- state (`NEW`, `SEEN`, `UPDATED`, etc.);
- decision recommendation;
- source references.

## Source of truth

Project documentation lives in `docs/`.

Start with:

- `docs/PROJECT_BLUEPRINT.md`
- `docs/ARCHITECTURE.md`
- `docs/MVP_SCOPE.md`
- `docs/ROADMAP.md`
- `docs/CANDIDATE_PROFILE.md`
- `docs/SEARCH_POLICY.md`
- `docs/SCORING_MODEL.md`
- `docs/SOURCES.md`
- `docs/DOMAIN_MODEL.md`
- `docs/DECISIONS.md`

## Non-goals of the MVP

The MVP is not:

- a generic job aggregator;
- a multi-user SaaS;
- a dashboard-first product;
- an autonomous job application bot;
- an LLM wrapper;
- an aggressive scraping system;
- a learning-to-rank/ML project.

The first milestone is a reliable, inspectable pipeline whose decisions can be explained and tested.
