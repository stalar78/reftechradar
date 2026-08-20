# Project Blueprint

## 1. Mission

RefTechRadar is a personal job-intelligence system for discovering **new** vacancies that match the candidate's real way of working.

The system prioritizes roles where the employer values an AI-assisted builder who can independently turn a business need into a working result using coding agents and modern application-development tooling.

The project must resist drift toward conventional keyword-based matching such as:

```text
Python in profile -> Senior Python Developer
```

The primary match is the **working model**, not the title.

## 2. Primary user outcome

A successful daily run reduces a large raw set of vacancies to a small, ranked shortlist:

```text
hundreds discovered
-> deterministic rejection
-> deduplicated relevant set
-> ranked shortlist
-> a few vacancies worth human attention
```

## 3. Core product invariants

1. `first_seen_at` is an immutable product fact.
2. A changed publisher date must not make an old vacancy `NEW`.
3. The same job exposed by several sources should resolve to one vacancy entity whenever confidence is sufficient.
4. Hard filters and deterministic scores must be inspectable.
5. Every score must contain evidence, not only a number.
6. AI semantic review is optional enrichment, never the only source of truth.
7. Source acquisition must prefer APIs, RSS, public endpoints, alerts and sustainable adapters over aggressive scraping.
8. Candidate policy must be configuration/domain data, not scattered constants.
9. The system must preserve enough source data to explain and debug decisions.
10. No automatic application submission is part of the current product.

## 4. Product layers

### Acquisition layer

Collects source observations without interpreting candidate fit.

### Normalization layer

Maps heterogeneous source fields into stable domain contracts.

### Identity layer

Resolves source observations into canonical vacancy entities and source references.

### State layer

Tracks freshness and lifecycle: `NEW`, `SEEN`, `UPDATED`, `APPLIED`, `SKIPPED`, `EXPIRED`.

### Policy layer

Evaluates deterministic rejects, positive evidence and penalties.

### Ranking layer

Calculates an explainable Opportunity Score and classification.

### Reporting layer

Produces compact CLI/Markdown/JSON digests.

### Intelligence layer

Later semantic review of survivors: nuance, risks, gap interpretation and application assistance.

## 5. Architectural stance

Use a modular Python monolith for the MVP.

Reasons:

- the problem is domain-heavy, not scale-heavy;
- SQLite is sufficient initially;
- one process is easier to debug and test;
- premature service decomposition would reduce speed without improving product value.

Internal boundaries should still be explicit so collectors, persistence and scoring can evolve independently.

## 6. Initial release strategy

Do not start with ten real sources.

First prove a vertical slice using controlled fixtures. Then connect one sustainable real source. Add the second source specifically to validate cross-source identity and deduplication.

## 7. Success criteria

The first production-usable milestone is reached when the system can repeatedly ingest observations, preserve vacancy identity across runs, detect new/updated vacancies, reject obvious mismatches, score survivors explainably and generate a trustworthy daily report.
