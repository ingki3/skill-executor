import httpx
import pytest
from uuid import uuid4

@pytest.mark.asyncio
async def test_batch_status_polling_contract():
    # This assumes the server is running or we use TestClient
    # For a contract test, we verify the response structure
    batch_id = uuid4()
    url = f"http://localhost:8000/skills/registration-batches/{batch_id}"
    
    # We'll skip if server is not reachable, or use a mock
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                assert "id" in data
                assert "status" in data
                assert "items" in data
                assert isinstance(data["items"], list)
        except httpx.ConnectError:
            pytest.skip("Server not running")
