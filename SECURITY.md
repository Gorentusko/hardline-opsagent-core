# Security Policy

## Supported security posture

v0.1 is report-only.

OpsAgent Core does not intentionally:

- restart services
- mutate containers
- delete files
- edit configs
- run remediation
- collect secrets
- send data externally unless an LLM provider is explicitly configured

## Docker socket warning

The optional Docker collector uses:

```yaml
/var/run/docker.sock:/var/run/docker.sock:ro
```

Docker socket access is powerful even when mounted read-only. Use it only on trusted systems.

## Secrets

Do not commit `.env`.

Use `.env.example` as a template.

## AI providers

Default provider is mock/offline. External providers require explicit user configuration.

## Reporting vulnerabilities

Open an issue or contact the maintainer through the GitHub profile.

