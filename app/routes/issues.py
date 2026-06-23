from __future__ import annotations

from fastapi import APIRouter

from app.connectors.github_issues import (
    connector_status,
    create_issue_from_latest_report,
    dry_run_latest_issue,
)

router = APIRouter(prefix="/issues", tags=["issues"])


@router.get("/status")
def issue_status():
    return connector_status()


@router.post("/dry-run")
def issue_dry_run():
    try:
        return dry_run_latest_issue()
    except FileNotFoundError as exc:
        return {"status": "blocked", "reason": str(exc)}


@router.post("/create")
def issue_create():
    try:
        return create_issue_from_latest_report()
    except FileNotFoundError as exc:
        return {"status": "blocked", "reason": str(exc)}
