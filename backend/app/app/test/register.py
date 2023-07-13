from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_success():
    response = client.post(
        "/api/v1/users/open",
        json={
            "email": "test2@example.com",
            "password": "testpassword",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test2@example.com"

def test_create_user_duplicate_email():
    response = client.post(
        "/api/v1/users/open",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The user with this username already exists in the system"
    }

