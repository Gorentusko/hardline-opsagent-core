# Contributing

Thanks for checking out Hardline OpsAgent Core.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

## Run locally

```bash
cp .env.example .env
python -m app.main
```

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

## Rules

- Keep default mode free/offline.
- Do not add automatic remediation without a separate design.
- Do not commit secrets.
- Keep reports factual and grounded in collected state.

