from __future__ import annotations

from datetime import datetime, timezone

from reftechradar.domain.models import RawObservation


def collect_fixture_observations(cycle: int = 1) -> list[RawObservation]:
    observed_at = datetime(2026, 1, cycle, 9, 0, tzinfo=timezone.utc)
    observations = [
        RawObservation(
            source="fixture",
            external_id="ai-builder-001",
            observed_at=observed_at,
            title="AI-first Product Builder",
            company="Practical Labs",
            description=(
                "Build internal tools and business automation with ChatGPT, Codex and coding agents "
                "as part of daily development. Own requirements, architecture, API integrations, tests "
                "and deployment end-to-end. Portfolio and real projects matter more than formal years. "
                "Stack: Python, FastAPI, React, TypeScript, PostgreSQL."
            ),
            location="Remote Russia",
            remote=True,
            source_url="https://fixture.local/jobs/ai-builder-001?utm=ref",
            published_at=datetime(2025, 12, 29, tzinfo=timezone.utc),
        ),
        RawObservation(
            source="fixture",
            external_id="senior-python-002",
            observed_at=observed_at,
            title="Senior Python Backend Developer",
            company="Backend Systems",
            description=(
                "Senior backend role requiring 5+ years professional Python development, distributed "
                "services and production support. Strong Python, REST and PostgreSQL required. "
                "The role is a conventional backend position in an established engineering team."
            ),
            location="Moscow hybrid",
            remote=False,
            source_url="https://fixture.local/jobs/senior-python-002",
            published_at=datetime(2025, 12, 28, tzinfo=timezone.utc),
        ),
        RawObservation(
            source="fixture",
            external_id="middle-ai-003",
            observed_at=observed_at,
            title="Middle AI Automation Developer",
            company="Workflow Forge",
            description=(
                "Middle role with nominal 3 years experience, but practical level is assessed by GitHub, "
                "portfolio and shipped projects. Use AI-assisted workflow, Copilot or Codex, build MVPs, "
                "internal services and API integrations with Python and React."
            ),
            location="Remote",
            remote=True,
            source_url="https://fixture.local/jobs/middle-ai-003",
            published_at=datetime(2025, 12, 27, tzinfo=timezone.utc),
        ),
        RawObservation(
            source="fixture",
            external_id="ml-heavy-004",
            observed_at=observed_at,
            title="ML Specialist / Data Scientist",
            company="ModelCore",
            description=(
                "Data Scientist role focused on model training, PyTorch and TensorFlow. Build and tune "
                "deep learning models, evaluate datasets and own ML research pipelines."
            ),
            location="Remote",
            remote=True,
            source_url="https://fixture.local/jobs/ml-heavy-004",
            published_at=datetime(2025, 12, 26, tzinfo=timezone.utc),
        ),
        RawObservation(
            source="fixture",
            external_id="stack-only-005",
            observed_at=observed_at,
            title="Python API Developer",
            company="Stack Match Co",
            description=(
                "Develop REST APIs with Python, FastAPI, SQL and Docker. Conventional backend feature "
                "delivery in an existing team. AI is mentioned only as an interest area."
            ),
            location="Remote",
            remote=True,
            source_url="https://fixture.local/jobs/stack-only-005",
            published_at=_published_for_stack_only(cycle),
        ),
    ]

    if cycle >= 2:
        observations.append(
            RawObservation(
                source="fixture",
                external_id="changed-006",
                observed_at=observed_at,
                title="Internal Automation Builder",
                company="OpsCraft",
                description=(
                    "Build internal tools, workflow automation and API integrations. Updated scope now "
                    "explicitly includes coding agents, Codex-assisted implementation, tests and "
                    "end-to-end ownership of small production tools."
                ),
                location="Remote Russia",
                remote=True,
                source_url="https://fixture.local/jobs/changed-006",
                published_at=datetime(2025, 12, 25, tzinfo=timezone.utc),
            )
        )
    else:
        observations.append(
            RawObservation(
                source="fixture",
                external_id="changed-006",
                observed_at=observed_at,
                title="Internal Automation Builder",
                company="OpsCraft",
                description="Build internal tools, workflow automation and API integrations with Python.",
                location="Remote Russia",
                remote=True,
                source_url="https://fixture.local/jobs/changed-006",
                published_at=datetime(2025, 12, 25, tzinfo=timezone.utc),
            )
        )
    return observations


def _published_for_stack_only(cycle: int) -> datetime:
    day = 24 if cycle <= 1 else 30
    return datetime(2025, 12, day, tzinfo=timezone.utc)
