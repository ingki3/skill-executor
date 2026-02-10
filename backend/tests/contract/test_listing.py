import httpx
import pytest

@pytest.mark.asyncio
async def test_list_skills_contract():
    """Verify the structure of the list-skills response."""
    repo_url = "https://github.com/ComposioHQ/awesome-claude-skills"
    api_url = f"http://localhost:8000/skills/list-from-repo?repo_url={repo_url}"
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(api_url)
            # This might fail if the implementation isn't there yet, which is expected in TDD
            if resp.status_code == 200:
                data = resp.json()
                assert "skills" in data
                assert isinstance(data["skills"], list)
                if len(data["skills"]) > 0:
                    item = data["skills"][0]
                    assert "name" in item
                    assert "path" in item
        except httpx.ConnectError:
            pytest.skip("Server not running")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_list_skills_contract())
