# Reviewer Demo

## Goal

Show that this is a practical DevOps/SRE-style project, not just a toy chatbot wrapper.

## Run

```bash
cp .env.example .env
docker compose up --build
```

## Test

```bash
curl -s http://localhost:8088/analyze | jq .
```

## What this demonstrates

- Dockerized Python service
- FastAPI API design
- system/container state collection
- rules-based evaluation
- model-agnostic AI provider abstraction
- safe default offline/mock mode
- Markdown report generation
- cost/security awareness

## What is intentionally not included

- no automatic remediation
- no bundled API key
- no secret collection
- no paid AI requirement



