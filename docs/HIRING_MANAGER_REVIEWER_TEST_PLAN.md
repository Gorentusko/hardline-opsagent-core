# Hiring Manager Reviewer Test Plan

## Goal

Verify that OpsAgent Core is a real Dockerized DevOps/SRE-style project and not just a prompt wrapper.

## 5-minute review

1. Clone or download the repo.
2. Run Docker Compose.
3. Call `/health`.
4. Call `/analyze`.
5. Inspect generated Markdown report in `data/reports`.

## Expected result

`/analyze` should return JSON like:

```json
{
  "status": "ok",
  "health": "healthy",
  "score": 90,
  "findings": [],
  "report_paths": {
    "report": "/app/data/reports/...",
    "state": "/app/data/state/latest_state.json"
  },
  "llm_provider": "mock"
}
```

## What this demonstrates

- Docker deployment
- Python/FastAPI service design
- state collection
- rules-based evaluation
- safe AI provider abstraction
- Markdown report generation
- no paid AI dependency
- BYOK provider design

## What to inspect in the repo

- `app/collectors/`
- `app/evaluators/`
- `app/llm/providers.py`
- `app/reports/markdown.py`
- `docker-compose.yml`
- `.env.example`
- `AI_ACCESS_POLICY.md`
- `SECURITY.md`
- `.github/workflows/ci.yml`

## Security/cost expectation

Default provider:

```env
OPSAGENT_LLM_PROVIDER=mock
```

This makes no paid calls and requires no API key.
