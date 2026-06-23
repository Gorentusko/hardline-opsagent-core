# v0.2 GitHub Issue Connector

Hardline OpsAgent Core v0.2 adds a safe GitHub issue connector.

The connector turns the latest generated Markdown report into an optional GitHub issue.

## Flow

```text
Run analysis -> generate Markdown report -> preview issue payload -> optionally create GitHub issue
```

## Safety defaults

The connector is safe by default:

```env
OPSAGENT_GITHUB_ENABLED=false
OPSAGENT_GITHUB_DRY_RUN=true
```

With those defaults, issue creation is blocked.

## Endpoints

```text
GET  /issues/status
POST /issues/dry-run
POST /issues/create
```

## Status endpoint

```text
GET /issues/status
```

Returns whether the connector is enabled, in dry-run mode, and configured.

## Dry-run endpoint

```text
POST /issues/dry-run
```

Builds a GitHub issue preview from the latest report without creating anything.

## Create endpoint

```text
POST /issues/create
```

Creates an issue only when all gates are satisfied:

```env
OPSAGENT_GITHUB_ENABLED=true
OPSAGENT_GITHUB_DRY_RUN=false
OPSAGENT_GITHUB_REPO=owner/repo
OPSAGENT_GITHUB_TOKEN=<user provided token>
```

## Token safety

- No token is bundled.
- The token is read only from the environment.
- The token is not written into reports.
- The token is not returned by API responses.
- Issue creation is never automatic.
