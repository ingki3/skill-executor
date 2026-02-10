import httpx
import pytest
import time
import subprocess
import os

@pytest.mark.asyncio
async def test_unified_services_health():
    """Test that both UI (3000) and API (8000) are reachable in the unified environment."""
    
    # In a real CI, we might start the container here.
    # For local test, we assume the environment is running or we test against the logic.
    
    api_url = "http://localhost:8000/health"
    ui_url = "http://localhost:3000"
    
    async with httpx.AsyncClient() as client:
        # Check Backend
        try:
            resp = await client.get(api_url)
            assert resp.status_code == 200
            assert resp.json()["status"] == "healthy"
        except Exception as e:
            pytest.fail(f"Backend unreachable at {api_url}: {e}")
            
        # Check Frontend (Vite preview)
        try:
            resp = await client.get(ui_url)
            assert resp.status_code == 200
            assert "html" in resp.text.lower()
        except Exception as e:
            pytest.fail(f"Frontend unreachable at {ui_url}: {e}")

if __name__ == "__main__":
    # This test assumes the container is already running
    import asyncio
    asyncio.run(test_unified_services_health())
