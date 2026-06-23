from typing import Any


def evaluate_state(state: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    score = 100

    disk = state.get("system", {}).get("disk_root", {})
    used = disk.get("used_percent", 0)

    if used >= 90:
        score -= 35
        findings.append(
            {"severity": "critical", "area": "disk", "message": f"Root disk usage is {used}%."}
        )
    elif used >= 80:
        score -= 15
        findings.append(
            {"severity": "warning", "area": "disk", "message": f"Root disk usage is {used}%."}
        )
    else:
        findings.append(
            {"severity": "ok", "area": "disk", "message": f"Root disk usage is {used}%."}
        )

    docker_state = state.get("docker", {})
    method = docker_state.get("collector_method", "unknown")
    if not docker_state.get("docker_available"):
        score -= 10
        findings.append(
            {
                "severity": "warning",
                "area": "docker",
                "message": "Docker socket/API not available to collector. Container inspection is limited.",
            }
        )
    else:
        count = len(docker_state.get("containers", []))
        findings.append(
            {
                "severity": "ok",
                "area": "docker",
                "message": f"{count} running containers detected by {method}.",
            }
        )

    health = "healthy"
    if score < 70:
        health = "degraded"
    if score < 40:
        health = "critical"

    return {
        "score": max(score, 0),
        "health": health,
        "findings": findings,
        "recommended_actions": [
            "Review warning and critical findings.",
            "Confirm backups are current before making changes.",
            "Create or update runbooks for recurring issues.",
            "Re-run analysis after any approved remediation.",
        ],
    }
