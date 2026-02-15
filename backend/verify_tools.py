import asyncio
import os
import json
from src.services.tool_service import ToolService
from src.models.tool import ExecutionStatus
from dotenv import load_dotenv

load_dotenv()

async def test_call():
    print("=== Tool Service Integration Test ===")
    service = ToolService()
    
    # 1. Load Registry
    await service.load_registry()
    tools = await service.list_tools()
    print(f"Registered tools: {[t.name for t in tools]}")
    
    # 2. Test Code Execution Tool
    print("\nTesting 'code_execution'...")
    code_tool = await service.get_tool("code_execution")
    if code_tool:
        test_code = "print('Hello from tool support test!'); x = 10 + 20; print(f'Result: {x}')"
        response = await service.execute_local_tool(code_tool, {"code": test_code})
        print(f"Status: {response.status}")
        if response.status == ExecutionStatus.SUCCESS:
            print(f"Stdout: {response.data.get('stdout').strip()}")
        else:
            print(f"Error: {response.message}")
    else:
        print("Error: code_execution tool not found in registry")

    # 3. Test Web Search (Mock mode)
    print("\nTesting 'web_search' (Mock mode)...")
    search_tool = await service.get_tool("web_search")
    if search_tool:
        response = await service.execute_local_tool(search_tool, {"query": "current weather in Seoul"})
        print(f"Status: {response.status}")
        print(f"Data summary: {list(response.data.keys())}")
    else:
        print("Error: web_search tool not found in registry")

    # 4. Verify Logs
    print("\nVerifying logs...")
    log_path = os.path.abspath("logs/tools.log")
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            last_lines = f.readlines()
            print(f"Total log entries: {len(last_lines)}")
    else:
        print(f"Log file not found at {log_path}")

if __name__ == "__main__":
    # Ensure current directory is in path
    import sys
    sys.path.append(os.getcwd())
    asyncio.run(test_call())
