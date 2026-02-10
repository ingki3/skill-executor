
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class HumanInterrupt(Exception):
    """Exception raised when the agent needs human input."""
    def __init__(self, prompt: str):
        self.prompt = prompt
        super().__init__(self.prompt)

class RequestInputArgs(BaseModel):
    prompt: str = Field(description="The question or prompt to ask the human.")

class RequestInputTool(BaseTool):
    name: str = "request_human_input"
    description: str = "Use this tool when you need clarification or more information from the human to proceed."
    args_schema: Type[BaseModel] = RequestInputArgs

    def _run(self, prompt: str) -> str:
        # In a real execution, this tool is "caught" by the agent loop
        # and doesn't actually return a value here normally.
        raise HumanInterrupt(prompt)

    async def _arun(self, prompt: str) -> str:
        raise HumanInterrupt(prompt)
