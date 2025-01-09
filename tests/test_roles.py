import pytest
from fastapi.testclient import TestClient
from app.schemas import RoleCreate, RoleResponse

def test_create_role(client: TestClient):
    role_data = {"name": "Editor", "description": "Can edit content", "permissions": {"content": ["read", "edit"]}}
    response = client.post("/api/roles/", json=role_data)
    assert response.status_code == 200
    role = response.json()
    assert role["name"] == "Editor"
    assert role["description"] == "Can edit content"

def test_get_roles(client: TestClient):
    response = client.get("/api/roles/")
    assert response.status_code == 200
    roles = response.json()
    assert isinstance(roles, list)