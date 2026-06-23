from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import requests

from app.config import settings


@dataclass(frozen=True)
class IssuePayload:
    title: str
    body: str
    report_name: str


def connector_status() -> dict[str, Any]:
    return {
        "enabled": settings.github_enabled,
        "dry_run": settings.github_dry_run,
        "repo_configured": bool(settings.github_repo),
        "token_configured": bool(settings.github_token),
        "api_url": settings.github_api_url,
    }


def latest_report_path() -> Path:
    report_dir = Path(settings.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    reports = sorted(report_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not reports:
        raise FileNotFoundError("No Markdown reports are available. Run /analyze first.")
    return reports[0]


def _extract_score(report_text: str) -> str:
    match = re.search(r"Score:\s*\*\*(\d+)\*\*", report_text)
    if match:
        return match.group(1)
    return "unknown"


def _extract_health(report_text: str) -> str:
    match = re.search(r"Health:\s*\*\*([^*]+)\*\*", report_text)
    if match:
        return match.group(1).strip()
    return "unknown"


def build_issue_payload(report_text: str, report_name: str) -> IssuePayload:
    score = _extract_score(report_text)
    health = _extract_health(report_text)
    title = f"OpsAgent Report: Health score {score} - Review recommended"
    body = f"""# OpsAgent Report

Source report: `{report_name}`

## Summary

- Health: **{health}**
- Score: **{score}**
- Provider: `{settings.llm_provider}`

## Report

{report_text[:10000]}

## Safety

This issue was generated from a local OpsAgent report. No automatic remediation was performed.
"""
    return IssuePayload(title=title, body=body, report_name=report_name)


def build_latest_issue_payload() -> IssuePayload:
    report = latest_report_path()
    return build_issue_payload(report.read_text(), report.name)


def dry_run_latest_issue() -> dict[str, Any]:
    payload = build_latest_issue_payload()
    return {
        "status": "dry_run",
        "repo": settings.github_repo or "not_configured",
        "title": payload.title,
        "body_preview": payload.body[:1200],
        "report_name": payload.report_name,
        "would_create_issue": False,
    }


def create_issue_from_latest_report() -> dict[str, Any]:
    if not settings.github_enabled:
        return {"status": "blocked", "reason": "GitHub connector is disabled."}
    if settings.github_dry_run:
        return {"status": "blocked", "reason": "GitHub connector is in dry-run mode."}
    if not settings.github_repo:
        return {"status": "blocked", "reason": "OPSAGENT_GITHUB_REPO is not configured."}
    if not settings.github_token:
        return {"status": "blocked", "reason": "OPSAGENT_GITHUB_TOKEN is not configured."}

    payload = build_latest_issue_payload()
    url = f"{settings.github_api_url.rstrip('/')}/repos/{settings.github_repo}/issues"
    response = requests.post(
        url,
        timeout=settings.github_timeout_seconds,
        headers={
            "Authorization": f"Bearer {settings.github_token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "hardline-opsagent-core",
        },
        json={"title": payload.title, "body": payload.body},
    )
    response.raise_for_status()
    data = response.json()
    return {
        "status": "created",
        "issue_url": data.get("html_url"),
        "issue_number": data.get("number"),
        "report_name": payload.report_name,
    }
