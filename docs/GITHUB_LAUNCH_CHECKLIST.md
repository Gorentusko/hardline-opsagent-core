# GitHub Launch Checklist

## Before publishing

- [ ] Choose license: MIT or Apache-2.0 recommended for review.
- [ ] Replace placeholder GitHub URL if needed.
- [ ] Confirm `.env` is not committed.
- [ ] Confirm default provider is `mock`.
- [ ] Confirm `OPENROUTER_API_KEY` is blank in `.env.example`.
- [ ] Run local Docker test.
- [ ] Run `/health`.
- [ ] Run `/analyze`.
- [ ] Confirm Markdown report appears in `data/reports`.
- [ ] Confirm dashboard loads at `http://localhost:8088`.
- [ ] Commit to GitHub.
- [ ] Add README screenshots later.

## Suggested repo description

Docker-deployable AI operations assistant that turns system/container state into health reports and runbooks. Mock/offline by default, OpenRouter BYOK optional.

## Suggested topics

```text
devops
sre
observability
docker
fastapi
ai
openrouter
homelab
runbooks
platform-engineering
```


