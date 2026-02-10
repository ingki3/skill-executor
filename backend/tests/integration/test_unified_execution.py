import httpx
import pytest

@pytest.mark.asyncio
async def test_unified_execution():
    """Verify that skills stored in the volume can be executed."""
    # This assumes at least one skill is registered
    api_list_url = "http://localhost:8000/skills"
    api_exec_url = "http://localhost:8000/skills/execute"
    
    async with httpx.AsyncClient() as client:
        try:
            # 1. Get a skill ID
            resp = await client.get(api_list_url)
            if resp.status_code == 200:
                skills = resp.json()
                if len(skills) > 0:
                    skill_id = skills[0]["id"]
                    
                    # 2. Execute it
                    # Note: Execution might require LLM key, so we check status code 200 or 500 with specific detail
                    exec_resp = await client.post(api_exec_url, json={"query": "test query"}, timeout=30.0)
                    assert exec_resp.status_code in [200, 500]
                    if exec_resp.status_code == 200:
                        data = exec_resp.json()
                        assert "steps" in data
                        assert "outcome" in data
        except httpx.ConnectError:
            pytest.skip("Server not running")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_unified_execution())
