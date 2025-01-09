import pytest
from fastapi.testclient import TestClient
from app.schemas import Token

def test_create_access_token(client: TestClient):
    response = client.post("/api/auth/token", data={"username": "test@example.com", "password": "password"})
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

def test_invalid_credentials(client: TestClient):
    response = client.post("/api/auth/token", data={"username": "wrong@example.com", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}