from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

def test_login_incorrect_email():
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "wrong@example.com", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}

def test_login_incorrect_password():
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}

