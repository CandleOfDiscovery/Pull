from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_lists_demo_jobs() -> None:
    response = client.get("/api/v1/jobs")
    assert response.status_code == 200
    assert response.json()["total"] == 2


def test_filters_jobs_by_remote_type() -> None:
    response = client.get("/api/v1/jobs?remote=remote")
    assert response.status_code == 200
    assert response.json()["items"][0]["company"] == "Lumen Labs"
