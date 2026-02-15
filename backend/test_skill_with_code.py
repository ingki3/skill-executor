import asyncio
import os
import sys
from uuid import UUID

# Ensure project root is in path
sys.path.append(os.getcwd())

from src.services.execution import execution_service
from src.models import ExecutionMode, ExecutionStatus

async def test_compound_interest_skill():
    print("=== Testing Skill with Code Execution ===")
    
    query = "Calculate compound interest for $10,000 at 5% interest rate, compounded monthly for 10 years."
    print(f"Query: {query}")
    
    # 1. Search for the skill
    from src.services.search import search_service
    skill, distance = search_service.find_best_skill(query)
    if not skill or skill.name != "Compound Interest Calculator":
        print(f"Error: Expected 'Compound Interest Calculator', got '{skill.name if skill else 'None'}'")
        return
    
    print(f"Found skill: {skill.name} (ID: {skill.id})")
    
    # 2. Start session
    session = await execution_service.start_session(
        skill_id=str(skill.id),
        query=query,
        mode=ExecutionMode.AUTONOMOUS
    )
    print(f"Session started: {session.session_id}")
    
    # 3. Run the agent loop
    await execution_service._execute_agent_loop(session)
    
    # 4. Verify results
    from src.services.session_registry import session_registry
    final_session = session_registry.get_session(session.session_id)
    
    print(f"\nFinal Status: {final_session.status}")
    for msg in final_session.history:
        print(f"\n[{msg.role.upper()}]:\n{msg.content}")

    if final_session.status == ExecutionStatus.COMPLETED:
        print("\nSuccess: Agent successfully executed the skill using code_execution!")
    else:
        print(f"\nFailure: Agent ended with status {final_session.status}")

if __name__ == "__main__":
    asyncio.run(test_compound_interest_skill())
