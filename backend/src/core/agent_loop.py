import asyncio
import re
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from ..services.session_registry import session_registry
from ..models.execution import ExecutionMessage, MessageRole

class AgentExecutionCallbackHandler(BaseCallbackHandler):
    def __init__(self, session_id: UUID, websocket_manager: Any = None):
        self.session_id = session_id
        self.websocket_manager = websocket_manager

    async def on_thought(self, thought: str):
        if self.websocket_manager:
            await self.websocket_manager.broadcast_status(
                self.session_id, 
                "THINKING", 
                thought=thought
            )

    async def on_tool_start(self, tool_name: str, tool_input: str):
        if self.websocket_manager:
            await self.websocket_manager.broadcast_status(
                self.session_id, 
                "TOOL_CALL", 
                thought=f"Calling tool: {tool_name}", 
                tool_call=tool_name
            )

class InterruptibleAgentLoop:
    def __init__(self, session_id: UUID, websocket_manager: Any = None):
        self.session_id = session_id
        self.websocket_manager = websocket_manager
        self.max_steps = 10

    async def run(self, llm: Any, tools: List[Any], prompt_template: str, input_text: str, mode: str = "HITL"):
        session = session_registry.get_session(self.session_id)
        if not session:
            return

        callbacks = AgentExecutionCallbackHandler(self.session_id, self.websocket_manager)
        
        # Prepare tools description
        tools_str = "\n".join([f"{t.name}: {t.description}" for t in tools])
        tool_names = ", ".join([t.name for t in tools])
        
        # Build initial prompt
        history = ""
        # In a more advanced version, we'd add previous turns here
        
        current_prompt = prompt_template.format(
            tools=tools_str,
            tool_names=tool_names,
            input=input_text,
            agent_scratchpad=""
        )

        scratchpad = ""
        
        for step in range(self.max_steps):
            # 1. Get LLM response
            print(f"DEBUG: Step {step} calling LLM with prompt length {len(current_prompt + scratchpad)}")
            response = await llm.ainvoke(current_prompt + scratchpad)
            
            # Handle both string and list content (for newer Gemini models)
            if isinstance(response.content, list):
                content = "".join([part["text"] for part in response.content if "text" in part])
            else:
                content = str(response.content)
                
            print(f"DEBUG: LLM Response: {content}")
            
            # 2. Parse response
            # Look for Final Answer
            final_answer_match = re.search(r"Final Answer:\s*(.*)", content, re.DOTALL)
            if final_answer_match:
                return {"output": final_answer_match.group(1).strip()}
            
            # Look for Thought and Action
            thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|$)", content, re.DOTALL)
            action_match = re.search(r"Action:\s*(.*?)\nAction Input:\s*(.*)", content, re.DOTALL)
            
            if thought_match:
                thought = thought_match.group(1).strip()
                await callbacks.on_thought(thought)
                scratchpad += f"\nThought: {thought}"
            
            if action_match:
                tool_name = action_match.group(1).strip()
                tool_input = action_match.group(2).strip()
                
                await callbacks.on_tool_start(tool_name, tool_input)
                
                # 3. Execute tool
                tool = next((t for t in tools if t.name == tool_name), None)
                if not tool:
                    observation = f"Error: Tool {tool_name} not found."
                else:
                    try:
                        from .tools import HumanInterrupt
                        observation = await tool.ainvoke(tool_input)
                    except HumanInterrupt as e:
                        if mode == "AUTONOMOUS":
                            error_msg = f"Ambiguity encountered in autonomous mode: {e.prompt}"
                            session_registry.update_session(self.session_id, status="FAILED")
                            if self.websocket_manager:
                                await self.websocket_manager.broadcast_error(self.session_id, error_msg)
                            return {"output": error_msg}
                        
                        # HITL mode: Pause the session
                        session_registry.update_session(self.session_id, status="PAUSED")
                        if self.websocket_manager:
                            await self.websocket_manager.broadcast_input_request(self.session_id, e.prompt)
                        
                        # Record the partial state in scratchpad for when we resume
                        # We don't return here, we let the exception bubble up or handled by caller
                        # But since we're in a loop, we should stop this execution.
                        raise e
                    except Exception as err:
                        observation = f"Error: {str(err)}"
                
                scratchpad += f"\nAction: {tool_name}\nAction Input: {tool_input}\nObservation: {observation}"
            else:
                # If no action found but not final answer, LLM might be hallucinating format
                # or just gave a final answer without the prefix.
                if not final_answer_match:
                    # Fallback: Treat as final answer if it's the last step
                    if step == self.max_steps - 1:
                        return {"output": content.strip()}
                    scratchpad += f"\n{content}"
            
        return {"output": "Max steps reached without final answer."}