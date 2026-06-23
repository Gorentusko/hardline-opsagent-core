from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import settings


def build_prompt(state: dict[str, Any], evaluation: dict[str, Any]) -> str:
    return (
        "Create an ops runbook from this system state and evaluation. "
        "Use only the provided facts. Keep it actionable.\n\n"
        f"STATE:\n{json.dumps(state, indent=2)[: settings.max_input_chars]}\n\n"
        f"EVALUATION:\n{json.dumps(evaluation, indent=2)}"
    )


def write_report(state: dict[str, Any], evaluation: dict[str, Any], ai_runbook: str) -> dict[str, str]:
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%d_%H%M%S")
    report_dir = Path(settings.report_dir)
    state_dir = Path(settings.state_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    report = report_dir / f"{stamp}_opsagent_health_report.md"
    state_file = state_dir / "latest_state.json"

    findings = "\n".join(
        f"- **{f.get('severity', 'unknown').upper()}** `{f.get('area', 'general')}`: "
        f"{f.get('message', '')}"
        for f in evaluation.get("findings", [])
    )

    actions = "\n".join(f"- {a}" for a in evaluation.get("recommended_actions", []))

    content = f"""# Hardline OpsAgent Health Report

Generated UTC: `{now.isoformat()}`

## Summary

- Health: **{evaluation.get("health")}**
- Score: **{evaluation.get("score")}**

## Findings

{findings}

## Recommended Actions

{actions}

{ai_runbook}

## Proof

State snapshot: `data/state/latest_state.json`
"""

    report.write_text(content)
    state_file.write_text(json.dumps({"state": state, "evaluation": evaluation}, indent=2))

    return {"report": str(report), "state": str(state_file)}
