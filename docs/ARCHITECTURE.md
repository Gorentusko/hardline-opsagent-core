# Architecture

```text
Collectors
  â†“
State Snapshot
  â†“
Rules Evaluator
  â†“
Optional LLM Provider
  â†“
Markdown Report + JSON State
  â†“
Future Connectors
```

## Collectors

- System collector
- Docker collector

## Evaluator

Rules first. AI second.

That means OpsAgent Core remains useful even without paid AI.

## LLM providers

- mock/offline default
- OpenRouter BYOK optional
- Ollama planned

## Future connectors

- Gitea/GitHub issues
- BookStack pages
- Nextcloud archive uploads


