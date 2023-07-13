from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success() -> str:
    email = "chchdelm3@icloud.com"
    password = "adminjun!!"

    response = client.post(
        "/api/v1/login/access-token",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"
    return token["access_token"]

def test_get_balance_success():
    token = test_login_success()
    response = client.get(
        "/api/v1/balance",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    balance = response.json()
    print(balance)
    exchanges = set(balance.keys())
    print(exchanges)
    assert exchanges == ("UPBIT", "KIS")

