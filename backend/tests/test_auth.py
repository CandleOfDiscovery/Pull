from fastapi.testclient import TestClient

from app.main import app


def test_register_login_and_profile() -> None:
    with TestClient(app) as client:
        register = client.post("/api/v1/auth/register", json={"email": "person@example.com", "password": "a-secure-password", "name": "Test Person"})
        assert register.status_code == 201
        token = register.json()["access_token"]
        profile = client.get("/api/v1/profile", headers={"Authorization": f"Bearer {token}"})
        assert profile.status_code == 200
        assert profile.json()["name"] == "Test Person"
