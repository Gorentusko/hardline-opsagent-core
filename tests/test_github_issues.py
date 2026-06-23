from pathlib import Path

from fastapi.testclient import TestClient

from app.config import settings
from app.connectors.github_issues import build_issue_payload
from app.main import app

client = TestClient(app)


def _set(name: str, value):
    object.__setattr__(settings, name, value)


def test_issue_status_defaults():
    response = client.get("/issues/status")
    assert response.status_code == 200
    data = response.json()
    assert data["enabled"] is False
    assert data["dry_run"] is True
    assert data["token_configured"] is False


def test_issue_dry_run_blocked_when_no_report(tmp_path: Path):
    _set("report_dir", str(tmp_path))
    response = client.post("/issues/dry-run")
    assert response.status_code == 200
    assert response.json()["status"] == "blocked"


def test_issue_payload_redacts_token():
    _set("github_token", "super-secret-token")
    report = "# Report\n\n- Health: **healthy**\n- Score: **100**\n"
    payload = build_issue_payload(report, "sample.md")
    assert "super-secret-token" not in payload.body
    assert payload.title == "OpsAgent Report: Health score 100 - Review recommended"


def test_issue_create_blocked_by_default(tmp_path: Path):
    _set("report_dir", str(tmp_path))
    (tmp_path / "sample.md").write_text("# Report\n\n- Health: **healthy**\n- Score: **100**\n")
    _set("github_enabled", False)
    _set("github_dry_run", True)
    response = client.post("/issues/create")
    assert response.status_code == 200
    assert response.json()["status"] == "blocked"


def test_issue_create_success_with_mocked_post(tmp_path: Path, monkeypatch):
    _set("report_dir", str(tmp_path))
    _set("github_enabled", True)
    _set("github_dry_run", False)
    _set("github_repo", "owner/repo")
    _set("github_token", "super-secret-token")
    (tmp_path / "sample.md").write_text("# Report\n\n- Health: **healthy**\n- Score: **100**\n")

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"html_url": "https://github.com/owner/repo/issues/1", "number": 1}

    captured = {}

    def fake_post(url, timeout, headers, json):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        return FakeResponse()

    monkeypatch.setattr("app.connectors.github_issues.requests.post", fake_post)
    response = client.post("/issues/create")
    data = response.json()
    assert data["status"] == "created"
    assert data["issue_number"] == 1
    assert captured["url"].endswith("/repos/owner/repo/issues")
    assert "super-secret-token" not in str(data)
