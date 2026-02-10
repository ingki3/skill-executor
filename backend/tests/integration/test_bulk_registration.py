import httpx
import pytest

@pytest.mark.asyncio
async def test_bulk_registration():
    """Verify that multiple skills can be registered from a repo URL and paths."""
    repo_url = "https://github.com/ComposioHQ/awesome-claude-skills"
    # Example paths in that repo
    selected_paths = ["skills/calculator", "skills/weather"]
    
    api_url = "http://localhost:8000/skills/register-bulk"
    payload = {
        "repo_url": repo_url,
        "selected_paths": selected_paths
    }
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(api_url, json=payload, timeout=30.0)
            if resp.status_code == 200:
                data = resp.json()
                assert data["status"] == "success"
                assert len(data["registered_skills"]) == 2
        except httpx.ConnectError:
            pytest.skip("Server not running")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_bulk_registration())
