import asyncio
import os
import sys
from uuid import uuid4
from datetime import datetime

# Ensure project root is in path
sys.path.append(os.getcwd())

from src.models import Skill, Complexity
from src.services.registry import registry_service

async def register_compound_skill():
    print("Registering Compound Interest Calculator skill...")
    
    skill = Skill(
        id=uuid4(),
        name="Compound Interest Calculator",
        description="Calculates compound interest based on principal, rate, and time using Python code.",
        metadata_path=".skills/compound-interest-calculator/SKILL.md",
        code_path=".skills/compound-interest-calculator/SKILL.md", # For now pointing to same file
        complexity=Complexity.COMPLEX,
        version="1.0.0",
        source_url="local"
    )
    
    registry_service.add_skill(skill)
    print(f"Skill registered with ID: {skill.id}")

if __name__ == "__main__":
    asyncio.run(register_compound_skill())
