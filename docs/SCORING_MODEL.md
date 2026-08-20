# Scoring Model v0

## 1. Goal

Opportunity Score ranks vacancies that survive hard filtering.

It is not a substitute for hard filtering and not an LLM judgement.

## 2. Design rules

1. Deterministic.
2. Versioned.
3. Explainable.
4. Bounded to `0..100`.
5. Work-model fit outweighs raw technology overlap.
6. Every component produces evidence.
7. The same input + profile + policy/scoring version gives the same score.

## 3. Initial component proposal

This is an architectural baseline, not a frozen numeric model.

### A. AI-first working model — up to 30

Examples:

- coding agents are explicitly part of daily engineering;
- AI-assisted implementation/review workflow;
- employer expects use of Codex/Cursor/Claude Code/Copilot;
- AI is part of responsibilities, not marketing.

### B. Experience flexibility / portfolio-first — up to 20

Examples:

- real projects over years of experience;
- GitHub/portfolio requested;
- any/no commercial experience accepted;
- junior/junior+;
- flexible middle;
- explicit practical assessment.

### C. Builder / ownership / product delivery — up to 20

Examples:

- end-to-end;
- full cycle;
- ownership;
- product builder mindset;
- rapid prototypes/MVP;
- independently deliver result.

### D. Internal tools / automation / integrations — up to 15

Examples:

- internal services;
- business automation;
- API integrations;
- workflow automation.

### E. Stack compatibility — up to 10

Relevant technologies include:

- Python/FastAPI;
- TypeScript/JavaScript;
- React/Next.js;
- PostgreSQL/SQLite;
- REST;
- Docker;
- testing/CI.

Stack compatibility is intentionally capped below work-model fit.

### F. Logistics/tool bonus — up to 5

Examples:

- remote Russia;
- Codex/Cursor/Copilot/Claude Code exposure;
- salary fit once configured.

## 4. Penalties

Penalties operate after positive components and before bounding.

Examples:

- seniority mismatch;
- strict years-of-experience requirement;
- hard English requirement;
- ML specialization;
- platform/Kubernetes specialization;
- Kafka/distributed-systems specialization;
- mandatory primary language outside profile;
- AI only weakly related to actual work.

Certain rules belong in hard filtering and therefore never reach scoring.

## 5. Suggested provisional thresholds

These are starting values to calibrate against a curated corpus:

- `0–34`: LOW_MATCH or rejected by policy;
- `35–59`: LOW_MATCH;
- `60–79`: MAYBE;
- `80–100`: STRONG_MATCH.

Do not optimize thresholds before a representative test set exists.

## 6. ScoreResult contract

A score result should conceptually contain:

```text
total_score
classification
scoring_version
positive_components[]
penalties[]
gaps[]
summary
```

Each component contains:

```text
feature_id
points
evidence
reason
```

## 7. Explainability example

```text
STRONG MATCH — 92/100

Positive:
+ 28 AI coding agents are part of daily development
+ 19 portfolio/projects outweigh formal tenure
+ 18 end-to-end product ownership
+ 12 internal automation and API integration
+ 10 Python/API/React stack match
+ 5 remote/tool fit

Penalties:
- none material

Gap:
- Claude Code appears in daily workflow and is not currently a primary tool

Recommendation:
APPLY NOW
```

## 8. Calibration strategy

Create a manually labeled "golden vacancies" corpus.

At minimum:

- strong positive examples;
- normal senior stack matches that must rank low/reject;
- ML specialist vacancies;
- pure frontend/backend vacancies;
- ambiguous 3-year AI-first vacancies;
- portfolio-first junior/middle builder roles.

Weight changes are accepted only when they improve the corpus without violating anti-drift invariants.

## 9. Semantic layer boundary

Later LLM review may explain nuance or recommend an application decision.

It should not silently mutate deterministic evidence or retroactively change freshness/identity.
