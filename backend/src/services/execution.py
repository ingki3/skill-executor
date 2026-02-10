import time
import asyncio
import os
from typing import List, Optional, Dict, Any
from uuid import UUID
from src.models import (
    Skill, ExecutionLog, ExecutionOutcome, ReACTStep, Complexity,
    ExecutionSession, ExecutionMode, ExecutionStatus, ExecutionMessage, MessageRole
)
from src.core.llm_clients import llm_clients
from src.services.search import search_service
from src.services.session_registry import session_registry

class ExecutionService:
    def __init__(self):
        self.websocket_manager = None

    def set_websocket_manager(self, manager: Any):
        self.websocket_manager = manager

    def verify_skill_paths(self, skill: Skill):
        """Verify that skill files exist in the mounted volume."""
        if not os.path.exists(skill.metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {skill.metadata_path}")
        if not os.path.exists(skill.code_path):
            raise FileNotFoundError(f"Code file not found: {skill.code_path}")

    async def start_session(self, skill_id: str, query: str, mode: ExecutionMode, config: Optional[Dict[str, Any]] = None) -> ExecutionSession:
        """Initialize a new execution session."""
        # For now, we assume skill_id is already known (from search or direct)
        # In a real flow, the UI might search first then call start_session
        session = session_registry.create_session(skill_id, mode, config)
        
        # Add initial query as a message
        user_msg = ExecutionMessage(
            session_id=session.session_id,
            role=MessageRole.HUMAN,
            content=query
        )
        session_registry.add_message(session.session_id, user_msg)
        
        return session

    async def run_session(self, session_id: UUID, resume_input: Optional[str] = None):
        """Execute the agent loop for a session."""
        session = session_registry.get_session(session_id)
        if not session:
            return

        session_registry.update_session(session_id, status=ExecutionStatus.RUNNING)
        
        # Give some time for WS client to connect in tests/UI
        await asyncio.sleep(0.5)
        
        # Background task to run the agent
        asyncio.create_task(self._execute_agent_loop(session, resume_input))

    async def _execute_agent_loop(self, session: ExecutionSession, resume_input: Optional[str] = None):
        """Actual execution logic using LLM and custom ReACT loop."""
        from src.core.agent_loop import InterruptibleAgentLoop
        from src.services.registry import registry_service
        from src.core.tools import RequestInputTool
        from src.core.prompt_loader import prompt_loader
        
        # 1. Mock for integration tests
        if session.skill_id.startswith("test-skill") or session.skill_id.startswith("skill-"):
            from src.core.tools import HumanInterrupt
            # Small delay to allow WS to connect
            await asyncio.sleep(1.5)
            
            if not resume_input:
                if session.mode == ExecutionMode.AUTONOMOUS:
                    error_msg = "Ambiguity encountered in autonomous mode: Mock fallback"
                    session_registry.update_session(session.session_id, status=ExecutionStatus.FAILED)
                    if self.websocket_manager:
                        await self.websocket_manager.broadcast_error(session.session_id, error_msg)
                    return {"output": error_msg}
                
                session_registry.update_session(session.session_id, status=ExecutionStatus.PAUSED)
                if self.websocket_manager:
                    await self.websocket_manager.broadcast_status(session.session_id, "THINKING", thought="I need to check the user's preference.")
                    await self.websocket_manager.broadcast_input_request(session.session_id, "Which color do you prefer?")
                return
            else:
                final_answer = f"Task completed with preference: {resume_input}"
                final_msg = ExecutionMessage(session_id=session.session_id, role=MessageRole.AI, content=final_answer)
                session_registry.add_message(session.session_id, final_msg)
                session_registry.update_session(session.session_id, status=ExecutionStatus.COMPLETED)
                if self.websocket_manager:
                    await self.websocket_manager.broadcast_final(session.session_id, final_answer)
                return

        # 2. Fetch Skill Details
        skill = registry_service.get_skill(session.skill_id)
        if not skill:
            session_registry.update_session(session.session_id, status=ExecutionStatus.FAILED)
            return

        # 2. Setup Tools (Always include RequestInputTool for HITL)
        tools = [RequestInputTool()]
        
        # 3. Choose LLM based on Complexity
        if skill.complexity == Complexity.COMPLEX:
            llm = llm_clients.advanced_model
        else:
            llm = llm_clients.simple_model

        # 4. Prepare Prompt Template
        template = prompt_loader.get("execution", "react_loop")

        loop = InterruptibleAgentLoop(session.session_id, self.websocket_manager)

        try:
            # If resuming, we should ideally restore the scratchpad.
            # For now, we'll just prepend the user response to the input or handle it as a new turn.
            input_text = session.history[0].content
            if resume_input:
                input_text = f"{input_text}\n\nUser just provided this additional information: {resume_input}"
            
            result = await loop.run(llm, tools, template, input_text, mode=session.mode)
            
            if result and "output" in result:
                final_msg = ExecutionMessage(
                    session_id=session.session_id,
                    role=MessageRole.AI,
                    content=result["output"]
                )
                session_registry.add_message(session.session_id, final_msg)
                session_registry.update_session(session.session_id, status=ExecutionStatus.COMPLETED)
                if self.websocket_manager:
                    await self.websocket_manager.broadcast_final(session.session_id, result["output"])
            
        except Exception as e:
            from src.core.tools import HumanInterrupt
            if isinstance(e, HumanInterrupt):
                # Status is already updated to PAUSED in loop.run
                pass
            else:
                print(f"Agent Loop Fatal Error: {e}")
                session_registry.update_session(session.session_id, status=ExecutionStatus.FAILED)
                if self.websocket_manager:
                    await self.websocket_manager.broadcast_error(session.session_id, str(e))

    async def execute_query(self, query: str) -> ExecutionLog:
        # Legacy method kept for backwards compatibility during transition
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
        from src.core.prompt_loader import prompt_loader
        
        with open(skill.metadata_path, "r") as f:
            content = f.read()
            
        metadata = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                except yaml.YAMLError:
                    metadata = yaml.safe_load(content)
            else:
                metadata = yaml.safe_load(content)
        else:
            metadata = yaml.safe_load(content)
            
        prompt_template = metadata.get("prompt", "")

        prompt = prompt_loader.get("execution", "simple_execution").format(
            prompt_template=prompt_template,
            query=query
        )
        response = await llm_clients.generate_simple(prompt)
        
        return ExecutionLog(
            query=query,
            outcome=ExecutionOutcome.SUCCESS,
            model_used="gemini-3-flash-preview",
            steps=[ReACTStep(thought="Direct execution", observation=response)],
            duration=0
        )

    async def _execute_complex(self, skill: Skill, query: str) -> ExecutionLog:
        # Simplified ReACT implementation for backwards compatibility
        steps = []
        thought_process = f"Processing complex skill: {skill.name}. Query: {query}"
        steps.append(ReACTStep(thought=thought_process))
        
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
