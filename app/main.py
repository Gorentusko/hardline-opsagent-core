from __future__ import annotations

from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, Response

from app.collectors.docker import collect_docker_state
from app.collectors.system import collect_system_state
from app.config import settings
from app.evaluators.rules import evaluate_state
from app.llm.providers import get_provider
from app.reports.markdown import build_prompt, write_report
from app.ui.dashboard import dashboard_html

app = FastAPI(title=settings.app_name)


@app.get("/", response_class=HTMLResponse)
def root():
    return dashboard_html()


@app.get("/api")
def api_metadata():
    return {
        "app": settings.app_name,
        "mode": settings.env,
        "llm_provider": settings.llm_provider,
        "message": "Use /health, /state, /analyze, /reports, or browser dashboard at /.",
    }


@app.get("/favicon.ico")
def favicon():
    # Tiny inline SVG favicon. Keeps browser logs clean without shipping binary assets.
    svg = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>
    <rect width='64' height='64' rx='14' fill='#0b1020'/>
    <path d='M14 34h9l5-16 8 28 5-12h9' fill='none' stroke='#3b82f6' stroke-width='5' stroke-linecap='round' stroke-linejoin='round'/>
    </svg>"""
    return Response(content=svg, media_type="image/svg+xml")


@app.get("/health")
def health():
    return {"status": "ok", "llm_provider": settings.llm_provider}


@app.get("/state")
def state():
    return {
        "system": collect_system_state(),
        "docker": collect_docker_state(),
    }


@app.get("/analyze")
def analyze():
    current_state = state()
    evaluation = evaluate_state(current_state)
    prompt = build_prompt(current_state, evaluation)
    provider = get_provider()
    ai_runbook = provider.generate(prompt)
    paths = write_report(current_state, evaluation, ai_runbook)
    return {
        "status": "ok",
        "health": evaluation["health"],
        "score": evaluation["score"],
        "findings": evaluation["findings"],
        "report_paths": paths,
        "llm_provider": settings.llm_provider,
    }


@app.get("/reports")
def list_reports():
    report_dir = Path(settings.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    reports = []
    for report in sorted(report_dir.glob("*.md"), reverse=True):
        reports.append(
            {
                "name": report.name,
                "size_bytes": report.stat().st_size,
                "modified_epoch": int(report.stat().st_mtime),
            }
        )
    return {"reports": reports}


@app.get("/reports/{name}", response_class=PlainTextResponse)
def read_report(name: str):
    if "/" in name or "\\" in name or not name.endswith(".md"):
        raise HTTPException(status_code=400, detail="Invalid report name.")
    report = Path(settings.report_dir) / name
    if not report.exists():
        raise HTTPException(status_code=404, detail="Report not found.")
    return report.read_text()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.bind_host, port=settings.bind_port, reload=False)

