# Quickstart: Choose Your Test Path

Hardline OpsAgent Core is designed to be testable from a Windows laptop, a Linux/Mac development machine, or a remote Ubuntu server.

You do **not** need an AI API key for the default demo.

## Pick a path

| Reviewer setup | Recommended path |
|---|---|
| Windows 11 laptop | Docker Desktop + PowerShell |
| Mac laptop | Docker Desktop + Terminal |
| Linux laptop | Docker Engine + Terminal |
| Remote Ubuntu server/VPS | SSH + Docker Engine |
| Already have Docker | Clone/copy repo and run Compose |

## Default AI mode

The default `.env` uses:

```env
OPSAGENT_LLM_PROVIDER=mock
```

That means:

- no external API calls
- no paid AI usage
- no API key required
- reports still generate with rules + mock runbook text

Optional OpenRouter mode is BYOK only: bring your own key.

```env
OPSAGENT_LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key_here
```

The project does not ship with a maintainer API key.



