import time
import asyncio
import os
from typing import List, Optional
from src.models import Skill, ExecutionLog, ExecutionOutcome, ReACTStep, Complexity
from src.core.llm_clients import llm_clients
from src.services.search import search_service

class ExecutionService:
    def verify_skill_paths(self, skill: Skill):
        """Verify that skill files exist in the mounted volume."""
        if not os.path.exists(skill.metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {skill.metadata_path}")
        if not os.path.exists(skill.code_path):
            raise FileNotFoundError(f"Code file not found: {skill.code_path}")

    async def execute_query(self, query: str) -> ExecutionLog:
        start_time = time.time()
        
        # 1. Search
        skill, distance = search_service.find_best_skill(query)
        
        if not skill:
            duration = time.time() - start_time
            return ExecutionLog(
                query=query,
                confidence_score=distance,
                outcome=ExecutionOutcome.NO_MATCH,
                duration=duration
            )

        # Verify paths
        try:
            self.verify_skill_paths(skill)
        except Exception as e:
             duration = time.time() - start_time
             return ExecutionLog(
                query=query,
                skill_id=skill.id,
                outcome=ExecutionOutcome.FAILURE,
                steps=[ReACTStep(thought="Initialization", observation=str(e))],
                duration=duration
            )

        # 2. Route and Execute
        if skill.complexity == Complexity.SIMPLE:
            log = await self._execute_simple(skill, query)
        else:
            log = await self._execute_complex(skill, query)
            
        log.skill_id = skill.id
        log.confidence_score = distance
        log.duration = time.time() - start_time
        return log

    async def _execute_simple(self, skill: Skill, query: str) -> ExecutionLog:
        # Load skill prompt and code
        import yaml
        
        with open(skill.metadata_path, "r") as f:
            content = f.read()
            
        metadata = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                except yaml.YAMLError:
                    # Fallback if frontmatter parsing fails
                    metadata = yaml.safe_load(content)
            else:
                metadata = yaml.safe_load(content)
        else:
            metadata = yaml.safe_load(content)
            
        prompt_template = metadata.get("prompt", "")

        prompt = f"""{prompt_template}

User Query: {query}"""
        response = await llm_clients.generate_simple(prompt)
        
        return ExecutionLog(
            query=query,
            outcome=ExecutionOutcome.SUCCESS,
            model_used="gemini-3-flash-preview",
            steps=[ReACTStep(thought="Direct execution", observation=response)],
            duration=0 # Will be updated by caller
        )

    async def _execute_complex(self, skill: Skill, query: str) -> ExecutionLog:
        # Simplified ReACT implementation for demonstration
        # In a real scenario, this would use LangChain's AgentExecutor
        steps = []
        
        thought_process = f"Processing complex skill: {skill.name}. Query: {query}"
        steps.append(ReACTStep(thought=thought_process))
        
        # Simulate multi-step reasoning
        response = await llm_clients.generate_advanced(f"Execute this skill: {skill.name} for query: {query}")
        steps.append(ReACTStep(thought="Final Answer", observation=response))
        
        return ExecutionLog(
            query=query,
            outcome=ExecutionOutcome.SUCCESS,
            model_used="gemini-3-pro-preview",
            steps=steps,
            duration=0
        )

execution_service = ExecutionService()
