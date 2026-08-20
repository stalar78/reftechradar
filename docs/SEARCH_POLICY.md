# Search Policy

## 1. Purpose

This policy controls which vacancies enter the candidate's attention set.

The system must match by **way of working first**, technologies second.

## 2. Strong positive signals

High-value semantic/keyword families:

- vibe coder / vibecoder;
- AI-first;
- AI-assisted;
- AI developer;
- AI product;
- AI automation;
- product builder;
- product engineer;
- Claude Code;
- Codex;
- Cursor;
- Copilot;
- coding agents;
- AI agents;
- internal tools;
- automation;
- business automation;
- MVP;
- prototype;
- rapid development;
- API integrations;
- internal services;
- full cycle;
- end-to-end;
- ownership;
- builder mindset;
- portfolio;
- GitHub;
- real projects;
- projects over formal experience;
- any experience;
- no commercial experience required;
- junior;
- junior+;
- flexible middle.

A positive signal must be weighted more strongly when it describes actual responsibilities rather than a tools/benefits list.

## 3. Hard-reject families

By default, reject or heavily penalize:

- Senior;
- Lead;
- Principal;
- Staff Engineer;
- mandatory 4–6+ years professional development;
- hard requirement for 3+ years in a narrow language specialty when clearly non-negotiable;
- deep ML / Data Science;
- model training;
- PyTorch/TensorFlow as core specialty;
- CUDA;
- Computer Vision specialist;
- Data Scientist;
- MLOps specialist;
- Kubernetes-heavy platform engineering;
- Kafka-heavy distributed backend;
- professional Go/Java/C++ as mandatory primary language;
- algorithmic/LeetCode-heavy hiring;
- mandatory English B2/C1 when genuinely required for everyday work;
- AI mentioned only as marketing/bonus;
- pure frontend/backend roles without meaningful AI/product/automation/ownership evidence.

## 4. Explicit non-hard-rejects

Do not reject automatically solely because of:

- the word `Middle`;
- a nominal 3-year requirement;
- one unfamiliar tool;
- Claude Code being requested;
- imperfect stack overlap.

## 5. Exception policy

A nominal experience requirement may be downgraded from reject to penalty/review when the vacancy contains strong counter-signals such as:

- portfolio-first hiring;
- demonstrable-project emphasis;
- AI-first workflow;
- output-over-tenure language;
- explicit willingness to assess practical level;
- broad builder role rather than narrow specialist role.

The system must preserve both pieces of evidence in its explanation.

## 6. AI relevance test

AI is considered **core** when it appears in responsibilities, delivery workflow, engineering process or required working method.

AI is considered **weak/marketing** when it appears only in:

- company positioning;
- product description unrelated to the role;
- optional benefit;
- generic "interest in AI".

## 7. Geography

Preference signal:

- remote Russia.

International sourcing is not a priority while English constraints materially reduce viability.

Location and language details should be configurable rather than hard-coded into source adapters.

## 8. Decision classes

Recommended classification layer:

- `AUTO_REJECT`
- `LOW_MATCH`
- `MAYBE`
- `STRONG_MATCH`

A later semantic reviewer may add:

- `APPLY_NOW`
- `REVIEW_MANUALLY`

but should not erase the deterministic explanation.

## 9. Policy test corpus

Maintain curated examples of:

- known strong matches;
- stack-only false positives;
- senior specialist false positives;
- ambiguous middle/3-year cases;
- AI-marketing false positives;
- internal-tool/product-builder positives.

Every material policy change should be evaluated against this corpus.
