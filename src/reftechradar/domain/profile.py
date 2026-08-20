from reftechradar.domain.models import CandidateProfile


DEFAULT_CANDIDATE_PROFILE = CandidateProfile(
    languages=("python", "typescript", "javascript", "sql", "html", "css"),
    frontend=("react", "next.js", "vite", "tailwind"),
    backend=("fastapi", "node.js", "rest api", "pydantic"),
    data=("postgresql", "sqlite", "json", "csv"),
    qa=("pytest", "vitest", "testing library", "playwright"),
    infrastructure=("docker", "docker compose", "nginx", "linux", "vps", "github actions", "ci/cd"),
    primary_ai_tools=("chatgpt", "codex", "github copilot", "copilot", "sourcecraft"),
    positive_work_model_terms=(
        "ai-first",
        "ai-assisted",
        "coding agents",
        "internal tools",
        "automation",
        "api integrations",
        "end-to-end",
        "ownership",
        "portfolio",
        "github",
        "real projects",
        "mvp",
    ),
)
