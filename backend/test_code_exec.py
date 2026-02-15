import asyncio
import os
from src.services.tool_service import ToolService
from src.models.tool import ExecutionStatus
from dotenv import load_dotenv

load_dotenv()

async def test_code_execution():
    print("=== Code Execution Tool Deep Test ===")
    service = ToolService()
    await service.load_registry()
    
    code_tool = await service.get_tool("code_execution")
    if not code_tool:
        print("Error: code_execution tool not found")
        return

    # Case 1: Simple calculation and stdout
    print("\n[Case 1] Basic Calculation & Print:")
    code1 = """
def calculate_fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(f"Fibonacci sequence (10): {list(calculate_fibonacci(10))}")
"""
    res1 = await service.execute_local_tool(code_tool, {"code": code1})
    print(f"Status: {res1.status}")
    if res1.data:
        print(f"Stdout: {res1.data.get('stdout').strip()}")

    # Case 2: Intentional Syntax Error
    print("\n[Case 2] Error Handling (Syntax Error):")
    code2 = "print('Missing closing parenthesis"
    res2 = await service.execute_local_tool(code_tool, {"code": code2})
    print(f"Status: {res2.status}")
    print(f"Error Message: {res2.message}")

    # Case 3: Runtime Error
    print("\n[Case 3] Error Handling (Zero Division):")
    code3 = "x = 1 / 0"
    res3 = await service.execute_local_tool(code_tool, {"code": code3})
    print(f"Status: {res3.status}")
    if res3.data:
        print(f"Error Info in Data: {res3.data.get('error')}")

    # Case 4: Data Processing
    print("\n[Case 4] Logic & Data Processing:")
    code4 = """
data = [10, 20, 30, 40, 50]
avg = sum(data) / len(data)
print(f"Input Data: {data}")
print(f"Average: {avg}")
"""
    res4 = await service.execute_local_tool(code_tool, {"code": code4})
    if res4.data:
        print(f"Stdout: {res4.data.get('stdout').strip()}")

if __name__ == "__main__":
    import sys
    sys.path.append(os.getcwd())
    asyncio.run(test_code_execution())
