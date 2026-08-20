# Stage 0 and Stage 1 Plan

## Stage 0 — Foundation and policy lock

### Objective

Make the intended product behavior unambiguous before implementation.

### Deliverables

- documentation set;
- agreed repository structure;
- naming/domain glossary;
- architecture decisions;
- initial scoring/policy model;
- first technical vertical slice;
- acceptance criteria.

### Acceptance criteria

- candidate is not modeled as a classic senior engineer;
- work-model matching is explicitly primary;
- MVP/non-MVP boundaries are documented;
- freshness semantics are explicit;
- state dimensions are separated;
- deterministic-first architecture is locked;
- no real-source implementation has started prematurely.

## Stage 1 — Core domain + persistence/state vertical slice

### Objective

Prove the product's hardest semantics independently of network sources.

### Slice

Use a small fixture collector with vacancy cases that include:

1. strong AI-first builder match;
2. ordinary senior Python false positive;
3. ambiguous middle + 3-year experience + portfolio-first case;
4. ML-heavy reject;
5. duplicate observation;
6. changed vacancy description on second run.

Flow:

```text
fixtures
-> normalize
-> resolve same-source identity
-> SQLite persist
-> NEW/SEEN/UPDATED
-> hard policy rules
-> deterministic score
-> Markdown + JSON digest
```

### Required tests

- first run creates `NEW`;
- second unchanged run creates `SEEN`;
- content change creates `UPDATED`;
- `first_seen_at` stays unchanged;
- source published-date-only change does not create `NEW`;
- known senior/ML cases reject;
- known strong match outranks stack-only vacancy;
- explanations include rule/component evidence;
- user decision state survives future ingestion.

### Stage 1 non-goals

- real collector;
- cross-source semantic dedupe;
- LLM review;
- Telegram;
- web UI.

## Proposed repository structure

```text
reftechradar/
  README.md
  pyproject.toml
  .gitignore
  .env.example

  docs/
    PROJECT_BLUEPRINT.md
    ARCHITECTURE.md
    MVP_SCOPE.md
    ROADMAP.md
    CANDIDATE_PROFILE.md
    SEARCH_POLICY.md
    SCORING_MODEL.md
    SOURCES.md
    DOMAIN_MODEL.md
    DECISIONS.md
    STAGE_0_STAGE_1.md

  src/
    reftechradar/
      __init__.py
      domain/
      collectors/
      normalization/
      identity/
      persistence/
      policy/
      scoring/
      reporting/
      application/

  tests/
    unit/
    integration/
    fixtures/

  data/
    .gitkeep

  reports/
    .gitkeep
```

`pyproject.toml`, package files and implementation code should be created in the coding step, not during the documentation-only bootstrap.

## Work allocation

### Architect / GPT

Own:

- product policy;
- architecture;
- docs/source of truth;
- acceptance criteria;
- scoring semantics;
- review of agent changes;
- stage transitions.

### SourceCraft / Copilot

Use for later narrow tasks:

- small config edits;
- simple tests;
- localized documentation updates;
- small adapters after contracts are stable;
- low-risk refactors.

### Codex

Use for Stage 1 implementation because it crosses:

- domain contracts;
- SQLite persistence;
- state transitions;
- deterministic policy/scoring;
- reporting;
- integration tests.

Codex should first inspect the repository and propose a plan before making broad changes.

## Codex task boundary

The first Codex implementation prompt should be issued **after Stage 0 is accepted**.

It should implement only the fixture-driven Stage 1 slice and must not add:

- real web collectors;
- FastAPI;
- frontend;
- LLM integration;
- Telegram;
- Docker unless required by an accepted decision;
- unrelated dependencies.

## Agent report required after implementation

- changed files;
- implementation summary;
- tests run and results;
- known limitations;
- deviations from plan;
- any architecture questions discovered.
