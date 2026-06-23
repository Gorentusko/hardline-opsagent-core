# v0.2 GitHub Issue Connector Plan

## Goal

Turn Hardline OpsAgent Core from a report-only demo into a small operations workflow tool.

Current flow:

```text
system/container state -> health score -> findings -> Markdown report
```

v0.2 target flow:

```text
system/container state -> health score -> findings -> Markdown report -> optional GitHub issue
```

## Positioning

This feature should stay safe, explicit, and portfolio-ready.

Hardline OpsAgent Core should not automatically spam GitHub issues or perform remediation. The user must intentionally trigger issue creation.

## Feature summary

Add an optional GitHub issue connector that can create an issue from the latest OpsAgent report.

Example issue title:

```text
OpsAgent Report: Health score 90 - Review recommended
```

Example issue body:

```markdown
# OpsAgent Report

- Health score: 90
- Provider: mock
- Generated: 2026-06-22

## Findings

- Docker collector warning
- Report generated successfully

## Recommended next action

Review the generated Markdown report and confirm whether the warning is expected.
```

## Safety model

Defaults:

```env
OPSAGENT_GITHUB_ENABLED=false
OPSAGENT_GITHUB_DRY_RUN=true
```

No GitHub write should happen unless both are true:

```env
OPSAGENT_GITHUB_ENABLED=true
OPSAGENT_GITHUB_DRY_RUN=false
```

Required user-provided settings:

```env
OPSAGENT_GITHUB_TOKEN=
OPSAGENT_GITHUB_REPO=owner/repo
```

Rules:

- Never bundle a token.
- Never print the token.
- Never save the token into reports.
- Never auto-create issues on page load.
- Never create issues on a schedule in v0.2.
- Require an explicit endpoint/button action.
- Keep mock/dry-run mode testable without GitHub access.

## Proposed endpoints

```text
GET  /issues/status
POST /issues/dry-run
POST /issues/create
```

### GET /issues/status

Returns connector readiness:

```json
{
  "enabled": false,
  "dry_run": true,
  "repo_configured": false,
  "token_configured": false
}
```

### POST /issues/dry-run

Builds the issue payload from the latest report but does not send it.

Returns:

```json
{
  "status": "dry_run",
  "title": "OpsAgent Report: Health score 90 - Review recommended",
  "body_preview": "...",
  "repo": "owner/repo"
}
```

### POST /issues/create

Creates the issue only when enabled and not dry-run.

Returns:

```json
{
  "status": "created",
  "issue_url": "https://github.com/owner/repo/issues/123"
}
```

If safety gates are not satisfied, return a clear blocked response.

## Proposed files

```text
app/connectors/github_issues.py
app/routes/issues.py
tests/test_github_issue_connector.py
docs/V0_2_GITHUB_ISSUE_CONNECTOR_PLAN.md
```

## Implementation notes

The connector should use a small dedicated client function rather than spreading GitHub logic across routes.

Recommended structure:

```text
load config
find latest report
build title/body
dry-run returns payload
create sends POST to GitHub API
return issue URL
```

## Testing plan

Tests should cover:

- status when disabled
- dry-run payload creation
- create blocked when disabled
- create blocked when dry-run is enabled
- create blocked when token is missing
- create success with mocked HTTP response
- token never appears in response

## Version plan

v0.2.0 should include:

- GitHub issue connector
- dashboard button for issue dry-run
- dashboard button for issue create only when enabled
- tests for connector safety gates
- README update
- release notes

