import pytest
from fastapi.testclient import TestClient
from app.schemas import MetaDataItemCreate, MetaDataItemResponse

def test_create_metadata_item(client: TestClient):
    metadata_item_data = {"key": "author", "value": "John Doe"}
    response = client.post("/api/metadata/", json=metadata_item_data)
    assert response.status_code == 200
    metadata_item = response.json()
    assert metadata_item["key"] == "author"
    assert metadata_item["value"] == "John Doe"

def test_get_metadata_items(client: TestClient):
    response = client.get("/api/metadata/")
    assert response.status_code == 200
    metadata_items = response.json()
    assert isinstance(metadata_items, list)