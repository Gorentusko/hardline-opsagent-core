# Product Spec: Hardline OpsAgent Core v0.1

## Product statement

Hardline OpsAgent Core is a model-agnostic AI operations assistant that turns system state into actionable reports, runbooks, and future tickets/docs.

## Primary goal

Make a hiring-manager-testable DevOps/SRE portfolio project that can be deployed with Docker Compose and demonstrate useful AI-assisted operations workflows without requiring paid AI access.

## Target users

- Homelab operators
- Junior-to-mid DevOps/SRE learners
- Small MSP operators
- Platform engineering reviewers
- technical reviewers looking for practical infrastructure automation work

## MVP promise

A user can clone the repo, run Docker Compose, call `/analyze`, and receive a clear Markdown operations report.

## v0.1 requirements

### Must have

- Docker Compose deployment
- FastAPI backend
- `/health`, `/state`, `/analyze`
- system collector
- Docker collector
- rules-based evaluator
- Markdown report generation
- JSON state snapshot
- mock/offline provider
- OpenRouter provider interface
- BYOK configuration
- docs for safe usage

### Must not have

- no bundled API key
- no paid AI by default
- no automatic remediation
- no destructive actions
- no hidden telemetry
- no secret leakage into reports

## Future roadmap

### v0.2 connectors

- GitHub/Gitea issue creation
- BookStack doc publishing
- Nextcloud archive upload

### v0.3 retention

- report index
- trend history
- weekly health score
- incident timeline

### v0.4 local AI

- Ollama provider
- local GPU mode
- no direct remediation authority

### v1.0 production-minded release

- authentication
- multi-host agents
- plugin system
- signed releases
- polished UI



