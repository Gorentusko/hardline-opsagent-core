from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Hardline OpsAgent Core" in response.text


def test_api_metadata():
    response = client.get("/api")
    assert response.status_code == 200
    assert "app" in response.json()


def test_reports_list():
    response = client.get("/reports")
    assert response.status_code == 200
    assert "reports" in response.json()
