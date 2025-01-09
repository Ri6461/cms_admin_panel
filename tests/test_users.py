import pytest
from fastapi.testclient import TestClient
from app.schemas import UserCreate, UserResponse

def test_register_user(client: TestClient):
    user_data = {"name": "Test User", "email": "test@example.com", "password": "password", "role_id": 1}
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"

def test_get_users(client: TestClient):
    response = client.get("/api/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)