from fastapi.testclient import TestClient

from app.main import app

def test_lists_demo_jobs() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/jobs")
        assert response.status_code == 200
        assert response.json()["total"] == 2


def test_filters_jobs_by_remote_type() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/jobs?remote=remote")
        assert response.status_code == 200
        assert response.json()["items"][0]["company"] == "Lumen Labs"
