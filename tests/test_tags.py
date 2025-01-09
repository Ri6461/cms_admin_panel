import pytest
from fastapi.testclient import TestClient
from app.schemas import TagCreate, TagResponse

def test_create_tag(client: TestClient):
    tag_data = {"name": "Technology", "description": "Tech related content"}
    response = client.post("/api/tags/", json=tag_data)
    assert response.status_code == 200
    tag = response.json()
    assert tag["name"] == "Technology"
    assert tag["description"] == "Tech related content"

def test_get_tags(client: TestClient):
    response = client.get("/api/tags/")
    assert response.status_code == 200
    tags = response.json()
    assert isinstance(tags, list)