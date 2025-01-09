import pytest
from fastapi.testclient import TestClient
from app.schemas import ContentCreate, ContentResponse

def test_create_content(client: TestClient):
    content_data = {"title": "Test Content", "body": "This is a test content.", "published": True}
    response = client.post("/api/content/", json=content_data)
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == "Test Content"
    assert content["body"] == "This is a test content."

def test_get_content(client: TestClient):
    response = client.get("/api/content/")
    assert response.status_code == 200
    content_list = response.json()
    assert isinstance(content_list, list)