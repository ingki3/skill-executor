
import asyncio
import httpx
import json
import pytest
import websockets
from uuid import UUID
import time
import subprocess
import os
import signal

# Test configuration
API_BASE_URL = "http://localhost:8001"
WS_BASE_URL = "ws://localhost:8001"

@pytest.fixture(scope="module")
def server():
    # Start the backend server on a test port
    env = os.environ.copy()
    # Ensure src is findable
    env["PYTHONPATH"] = os.getcwd()
    
    cmd = ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
    process = subprocess.Popen(
        cmd,
        env=env,
        preexec_fn=os.setsid,
        cwd=os.getcwd()
    )
    
    # Wait for server to be ready with more robust check
    start_time = time.time()
    ready = False
    while time.time() - start_time < 15:
        try:
            with httpx.Client() as client:
                if client.get(f"{API_BASE_URL}/health", timeout=1.0).status_code == 200:
                    ready = True
                    break
        except Exception:
            time.sleep(0.5)
    
    if not ready:
        # Print logs if failed to start
        out, err = process.communicate(timeout=1)
        print(f"Server failed to start. STDOUT: {out.decode()}, STDERR: {err.decode()}")
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        pytest.fail("Server failed to start")
    
    yield
    
    # Cleanup
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except:
        pass

@pytest.fixture(autouse=True)
def clear_sessions():
    """Clear sessions before each test using a sync client."""
    with httpx.Client() as client:
        try:
            client.delete(f"{API_BASE_URL}/execution/sessions/clear")
        except:
            pass
    yield

@pytest.mark.asyncio
async def test_hitl_full_flow(server):
    async with httpx.AsyncClient() as client:
        # 1. Start Session
        response = await client.post(
            f"{API_BASE_URL}/execution/start",
            json={
                "skill_id": "test-skill",
                "input": "Test HITL Input",
                "mode": "HITL"
            }
        )
        assert response.status_code == 201
        session_data = response.json()
        session_id = session_data["session_id"]
        
        # 2. Connect to WebSocket
        async with websockets.connect(f"{WS_BASE_URL}/execution/ws/{session_id}") as ws:
            # Wait for connection to be fully registered
            await asyncio.sleep(1.0)
            
            # 3. Listen for Events
            prompt_received = False
            
            # The agent might send THINKING before we connect, so we focus on request_input
            for _ in range(10):
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
                    event = json.loads(msg)
                    if event["event"] == "request_input":
                        prompt_received = True
                        assert event["payload"]["prompt"] == "Which color do you prefer?"
                        break
                except asyncio.TimeoutError:
                    break
            
            assert prompt_received, "Did not receive request_input event"
            
            # 4. Provide User Response
            await ws.send(json.dumps({
                "event": "user_response",
                "payload": {"content": "Blue"}
            }))
            
            # 5. Verify Completion
            completed_received = False
            for _ in range(10):
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
                    event = json.loads(msg)
                    if event["event"] == "final_answer":
                        assert "Blue" in event["payload"]["content"]
                        completed_received = True
                        break
                except asyncio.TimeoutError:
                    break
            
            assert completed_received

@pytest.mark.asyncio
async def test_autonomous_fallback(server):
    async with httpx.AsyncClient() as client:
        # 1. Start Autonomous Session
        response = await client.post(
            f"{API_BASE_URL}/execution/start",
            json={
                "skill_id": "test-skill",
                "input": "Test Autonomous Fallback",
                "mode": "AUTONOMOUS"
            }
        )
        assert response.status_code == 201
        session_id = response.json()["session_id"]
        
        # 2. Verify it fails on ambiguity via WS
        async with websockets.connect(f"{WS_BASE_URL}/execution/ws/{session_id}") as ws:
            error_received = False
            for _ in range(10):
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
                    event = json.loads(msg)
                    if event["event"] == "error":
                        assert "Ambiguity encountered" in event["payload"]["message"]
                        error_received = True
                        break
                except asyncio.TimeoutError:
                    break
            
            assert error_received

@pytest.mark.asyncio
async def test_concurrency_limit(server):
    async with httpx.AsyncClient() as client:
        # Start 5 sessions in HITL mode so they stay active
        for i in range(5):
            response = await client.post(
                f"{API_BASE_URL}/execution/start",
                json={"skill_id": f"skill-{i}", "input": "...", "mode": "HITL"}
            )
            assert response.status_code == 201
        
        # 6th should fail
        response = await client.post(
            f"{API_BASE_URL}/execution/start",
            json={"skill_id": "skill-6", "input": "...", "mode": "HITL"}
        )
        assert response.status_code == 429
        assert "Maximum concurrent sessions reached" in response.json()["detail"]
