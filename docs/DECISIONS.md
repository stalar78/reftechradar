# Architecture Decisions

This file is the lightweight decision log. Formal ADR files may be introduced if the log becomes large.

## D-001 — Modular monolith for MVP

**Status:** Accepted

**Decision:** Build the first system as a modular Python monolith.

**Reason:** domain correctness, identity and ranking matter more than horizontal scale. A service architecture would add operational complexity without MVP value.

## D-002 — SQLite first

**Status:** Accepted

**Decision:** Use SQLite initially behind repository/persistence boundaries.

**Reason:** simple local operation and testing. PostgreSQL remains a later migration path.

## D-003 — Persistence/state before broad source expansion

**Status:** Accepted

**Decision:** Establish vacancy identity, state and persistence before integrating many collectors.

**Reason:** `NEW`/`UPDATED` and deduplication are core product semantics.

## D-004 — Fixture-first vertical slice

**Status:** Accepted

**Decision:** The first technical slice uses controlled fixtures and two sequential runs before a real collector.

**Reason:** validates domain/state/policy contracts without mixing external-source instability into core debugging.

## D-005 — Deterministic core, semantic AI later

**Status:** Accepted

**Decision:** hard filtering, scoring, freshness and identity are deterministic first.

**Reason:** reliability, cost, repeatability and explainability.

## D-006 — Work-model fit outranks stack match

**Status:** Accepted

**Decision:** cap raw stack contribution below AI-first / experience-flexibility / ownership signals.

**Reason:** prevents regression into conventional job-board matching.

## D-007 — Separate observation state from user decision state

**Status:** Accepted

**Decision:** do not store `NEW/UPDATED` and `APPLIED/SKIPPED` as a single destructive enum internally.

**Reason:** a new source observation must not erase human application history.

## D-008 — Conservative cross-source deduplication

**Status:** Accepted

**Decision:** uncertain duplicates remain separate in early versions.

**Reason:** false merges destroy identity/history and are harder to repair than duplicates.

## D-009 — No dashboard in MVP

**Status:** Accepted

**Decision:** CLI + Markdown/JSON is the first interface.

**Reason:** core ranking quality must be proven before UI investment.

## D-010 — No automatic job application

**Status:** Accepted

**Decision:** RefTechRadar recommends and assists; application submission remains manual.

**Reason:** current product scope and safety/control.
