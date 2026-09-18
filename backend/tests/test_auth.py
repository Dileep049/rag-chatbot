from fastapi.testclient import TestClient
from app.main import app
from app.config import ADMIN_EMAIL, ADMIN_PASSWORD

client = TestClient(app)

def test_admin_login_success():
    res = client.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == ADMIN_EMAIL
    assert data["user"]["role"] == "admin"

def test_admin_login_invalid_password():
    res = client.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": "WrongPassword123"})
    assert res.status_code == 401
    assert "Invalid email or password" in res.json()["detail"]

def test_auth_me_valid_token():
    login_res = client.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["user"]["role"] == "admin"

def test_auth_me_invalid_token():
    headers = {"Authorization": "Bearer invalid_token_xyz_123"}
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 401
