# AI Access Policy

OpsAgent Core is safe and cost-free by default.

## Default mode

```env
OPSAGENT_LLM_PROVIDER=mock
```

Mock mode:

- does not call external APIs
- costs $0
- requires no key
- still produces runbook-style report text

## BYOK model

Users bring their own API key for external providers.

```env
OPSAGENT_LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=...
```

The project does not include, proxy, lend, or share Alec's OpenRouter key or any maintainer-owned key.

## Cost guardrails

```env
OPSAGENT_MAX_LLM_CALLS_PER_RUN=1
OPSAGENT_MAX_INPUT_CHARS=12000
OPSAGENT_LLM_TIMEOUT_SECONDS=45
```

## Provider design

Providers are swappable:

- `mock` now
- `openrouter` optional
- `ollama` planned
- other providers later

## Development rule

No paid AI calls are needed for development, tests, CI, or the default demo.
