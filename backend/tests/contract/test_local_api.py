import httpx
import pytest

@pytest.mark.asyncio
async def test_list_local_api_contract():
    url = "http://localhost:8000/skills/list-from-local?absolute_path=."
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                assert "absolute_path" in data
                assert "skills" in data
                assert isinstance(data["skills"], list)
                if len(data["skills"]) > 0:
                    item = data["skills"][0]
                    assert "name" in item
                    assert "path" in item
                    assert "has_metadata" in item
        except httpx.ConnectError:
            pytest.skip("Server not running")
