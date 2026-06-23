# Hardline OpsAgent Core

![CI](https://github.com/hardlineitgroup/hardline-opsagent-core/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/docker-compose-blue)
![AI](https://img.shields.io/badge/AI-mock%20default-green)
![License](https://img.shields.io/badge/license-MIT-green)

**Hardline OpsAgent Core** is a Docker-deployable AI operations assistant that turns system and container state into health reports, runbooks, and proof-style Markdown output.

It is safe by default:

- no paid AI calls required
- no bundled API keys
- mock/offline provider by default
- optional OpenRouter BYOK support
- no automatic remediation
- no destructive actions

---

## Why this exists

Ops teams, homelab users, and small IT shops often have system state scattered across containers, logs, disk checks, and dashboards.

OpsAgent Core turns that raw state into a simple operational loop:

```text
collect state -> score health -> generate report -> save proof -> review next action
```

This is not AGI and it is not a monitoring replacement. It is a practical AI-assisted operations layer.

---

## Quick demo

```bash
cp .env.example .env
docker compose up --build
```

Open:

```text
http://localhost:8088
```

Click **Run analysis**.

You should see:

- service status
- active LLM provider
- health score
- findings
- generated Markdown reports

---

## Windows 11 reviewer path

For a normal Windows laptop:

1. Install Docker Desktop.
2. Download or clone this repo.
3. Open PowerShell in the repo folder.
4. Run:

```powershell
copy .env.example .env
docker compose up --build
```

Then open:

```text
http://localhost:8088
```

Use `curl.exe` instead of `curl` in older PowerShell:

```powershell
curl.exe http://localhost:8088/health
curl.exe http://localhost:8088/analyze
```

More details:

- [`docs/WINDOWS_11_QUICKSTART.md`](docs/WINDOWS_11_QUICKSTART.md)
- [`docs/HIRING_MANAGER_REVIEWER_TEST_PLAN.md`](docs/HIRING_MANAGER_REVIEWER_TEST_PLAN.md)
- [`docs/INSTALL_MATRIX.md`](docs/INSTALL_MATRIX.md)

---

## API

| Endpoint | Purpose |
|---|---|
| `GET /` | Browser dashboard |
| `GET /api` | API metadata |
| `GET /health` | Health check |
| `GET /state` | Collect current state |
| `GET /analyze` | Evaluate state and generate report |
| `GET /reports` | List generated Markdown reports |
| `GET /reports/{name}` | Read a generated Markdown report |

---

## AI access model

Default mode:

```env
OPSAGENT_LLM_PROVIDER=mock
```

This makes no external API calls and costs nothing.

Optional OpenRouter mode:

```env
OPSAGENT_LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key_here
```

This project does not include a maintainer API key. Users bring their own key.

See [`AI_ACCESS_POLICY.md`](AI_ACCESS_POLICY.md).

---

## Current v0.1.4 capabilities

- Docker Compose deployment
- FastAPI backend
- Browser dashboard
- system collector
- Docker socket collector
- rules-based health evaluator
- mock/offline LLM provider
- optional OpenRouter provider interface
- Markdown report generation
- report browser
- CI workflow
- Windows and Ubuntu quickstarts

---

## Screenshot/demo expectation

A successful local demo shows:

```text
Status: ok
LLM provider: mock
Run analysis -> status ok
Reports -> generated Markdown files
```

See [`examples/sample_health_report.md`](examples/sample_health_report.md).

---

## Roadmap

- v0.2: GitHub/Gitea issue connector
- v0.3: BookStack/Nextcloud publishing
- v0.4: scheduled daily reports and history
- v0.5: Ollama/local model provider
- v1.0: multi-host agent and production-ready auth model

See [`ROADMAP.md`](ROADMAP.md).

---

## Security

v0.1.4 is report-only. It does not restart services, mutate containers, delete files, edit configs, or run remediation.

See [`SECURITY.md`](SECURITY.md).

---

## License

MIT License. See [`LICENSE`](LICENSE).
