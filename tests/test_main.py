import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    response = await client.post("/items/", json={"name": "Test Item", "description": "This is a test item"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"


@pytest.mark.asyncio
async def test_get_all_items(client: AsyncClient):
    await client.post("/items/", json={"name": "Item 1", "description": "First item"})
    await client.post("/items/", json={"name": "Item 2", "description": "Second item"})

    response = await client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_get_single_item(client: AsyncClient):
    create_response = await client.post("/items/", json={"name": "Single Item", "description": "This is a single item"})
    item_id = create_response.json()["id"]

    response = await client.get(f"/items/{item_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Single Item"
    assert data["description"] == "This is a single item"


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient):
    create_response = await client.post("/items/", json={"name": "Old Item", "description": "Old description"})
    item_id = create_response.json()["id"]

    response = await client.put(f"/items/{item_id}/", json={"name": "Updated Item", "description": "Updated description"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Updated Item"
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    create_response = await client.post("/items/", json={"name": "Item to Delete", "description": "This item will be deleted"})
    item_id = create_response.json()["id"]

    response = await client.delete(f"/items/{item_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Item to Delete"
    assert data["description"] == "This item will be deleted"

    response = await client.get(f"/items/{item_id}/")
    assert response.status_code == 404
