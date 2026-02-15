import json
import asyncio
import importlib.util
import logging
import os
from typing import List, Dict, Any, Optional, Type, Tuple, Callable
from pathlib import Path
import aiofiles
from pydantic import ValidationError
import faiss
import numpy as np
from datetime import datetime, timedelta
from uuid import UUID

from langchain.tools import BaseTool

# MCP Client Imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.models.tool import ToolDefinition, ToolType, ToolResponse, ExecutionStatus, ToolExecutionLog
from src.core.vector_store import VectorStore

logger = logging.getLogger(__name__)

class DynamicLocalTool(BaseTool):
    """LangChain wrapper for local Python script tools."""
    name: str
    description: str
    tool_def: ToolDefinition
    
    def _run(self, *args, **kwargs) -> Any:
        """Synchronous run not supported, use _arun."""
        raise NotImplementedError("DynamicLocalTool only supports async execution")

    async def _arun(self, **kwargs) -> Any:
        """Async execution of the tool."""
        service = ToolService()
        response = await service.execute_local_tool(self.tool_def, kwargs)
        if response.status == ExecutionStatus.SUCCESS:
            return response.data
        else:
            return f"Error: {response.message}"

class MCPToolWrapper(BaseTool):
    """LangChain wrapper for MCP tools."""
    name: str
    description: str
    server_name: str
    
    def _run(self, *args, **kwargs) -> Any:
        raise NotImplementedError("MCPToolWrapper only supports async execution")

    async def _arun(self, **kwargs) -> Any:
        service = ToolService()
        return await service.call_mcp_tool(self.server_name, self.name, kwargs)

class ToolService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ToolService, cls).__new__(cls)
        return cls._instance

    def __init__(self, tools_config_path: Optional[str] = None, mcp_config_path: Optional[str] = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        # Robust path resolution
        root = Path(os.getcwd())
        if (root / "backend").exists():
            base_dir = root / "backend"
        else:
            base_dir = root

        self.tools_config_path = Path(tools_config_path) if tools_config_path else base_dir / "src/tools/tools.json"
        self.mcp_config_path = Path(mcp_config_path) if mcp_config_path else base_dir / "src/tools/mcp.json"
        self.log_file_path = base_dir / "logs/tools.log"
        
        self.tools: Dict[str, ToolDefinition] = {}
        self.mcp_servers: Dict[str, Dict[str, Any]] = {}
        self.mcp_sessions: Dict[str, ClientSession] = {}
        
        self.update_queue = asyncio.Queue()
        self.vector_store = VectorStore(dimension=3072)
        self.tool_names_in_index: List[str] = []
        
        self._initialized = True
        asyncio.create_task(self._update_worker())
        asyncio.create_task(self._cleanup_logs_task())

    def reset_for_test(self):
        """Reset the singleton state for testing purposes."""
        self.tools = {}
        self.mcp_servers = {}
        self.mcp_sessions = {}
        self.vector_store.remove_all()
        self.tool_names_in_index = []

    async def _cleanup_logs_task(self):
        """Daily log rotation and retention per FR-016."""
        while True:
            try:
                log_dir = Path("backend/logs")
                if log_dir.exists():
                    retention_days = 30
                    cutoff = datetime.now() - timedelta(days=retention_days)
                    for log_file in log_dir.glob("tools.log.*"):
                        if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff:
                            log_file.unlink()
                            logger.info(f"Deleted old log file: {log_file}")
            except Exception as e:
                logger.error(f"Log cleanup error: {e}")
            await asyncio.sleep(86400) # Check daily

    async def _update_worker(self):
        while True:
            update_fn, future = await self.update_queue.get()
            try:
                result = await update_fn()
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                self.update_queue.task_done()

    async def submit_registry_update(self, update_fn: Callable) -> Any:
        future = asyncio.get_event_loop().create_future()
        await self.update_queue.put((update_fn, future))
        return await future

    async def load_registry(self):
        """Load both local and MCP tool definitions."""
        try:
            # 1. Local Tools
            if self.tools_config_path.exists():
                async with aiofiles.open(self.tools_config_path, mode='r') as f:
                    data = json.loads(await f.read())
                    new_tools = {}
                    for tool_data in data.get("tools", []):
                        tool = ToolDefinition(**tool_data)
                        new_tools[tool.name] = tool
                    self.tools = new_tools

            # 2. MCP Servers
            if self.mcp_config_path.exists():
                async with aiofiles.open(self.mcp_config_path, mode='r') as f:
                    data = json.loads(await f.read())
                    self.mcp_servers = data.get("mcp_servers", {})
            
            await self.index_tools()
                
        except Exception as e:
            logger.critical(f"Critical error loading tool registry: {e}", exc_info=True)
            raise SystemExit(f"Halt: Registry failure {e}")

    async def index_tools(self):
        self.vector_store.remove_all()
        self.tool_names_in_index = []
        # Index local
        for name, tool in self.tools.items():
            self.vector_store.add_skill(name, f"{name}: {tool.description}")
            self.tool_names_in_index.append(name)

    async def search_tools(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Search for tools based on a natural language query."""
        return self.vector_store.search(query, top_k=top_k)

    async def get_tool(self, name: str) -> Optional[ToolDefinition]:
        return self.tools.get(name)

    async def list_tools(self) -> List[ToolDefinition]:
        return list(self.tools.values())

    def get_langchain_tools(self) -> List[BaseTool]:
        lc_tools = []
        for tool_def in self.tools.values():
            if tool_def.type == ToolType.LOCAL:
                lc_tools.append(DynamicLocalTool(name=tool_def.name, description=tool_def.description, tool_def=tool_def))
        return lc_tools

    async def get_mcp_session(self, server_name: str) -> ClientSession:
        """Establish or return an existing MCP session with retry logic per FR-017."""
        if server_name in self.mcp_sessions:
            return self.mcp_sessions[server_name]
        
        if server_name not in self.mcp_servers:
            raise ValueError(f"MCP server {server_name} not configured")
        
        cfg = self.mcp_servers[server_name]
        params = StdioServerParameters(
            command=cfg["command"],
            args=cfg["args"],
            env={**os.environ, **cfg.get("env", {})}
        )
        
        last_err = None
        for attempt in range(3):
            try:
                transport_ctx = stdio_client(params)
                read, write = await transport_ctx.__aenter__()
                session = ClientSession(read, write)
                await session.initialize()
                self.mcp_sessions[server_name] = session
                return session
            except Exception as e:
                last_err = e
                wait = (2 ** attempt)
                logger.warning(f"MCP connection attempt {attempt+1} failed for {server_name}: {e}. Retrying in {wait}s...")
                await asyncio.sleep(wait)
        
        raise Exception(f"Failed to connect to MCP server {server_name} after 3 attempts: {last_err}")

    async def call_mcp_tool(self, server_name: str, tool_name: str, args: Dict[str, Any]) -> Any:
        try:
            session = await self.get_mcp_session(server_name)
            result = await session.call_tool(tool_name, args)
            return result.content
        except Exception as e:
            logger.error(f"MCP call error ({server_name}/{tool_name}): {e}")
            return f"Error: {str(e)}"

    async def execute_local_tool(self, tool: ToolDefinition, args: Dict[str, Any]) -> ToolResponse:
        # Resolve script path based on registry file location
        script_path = self.tools_config_path.parent / tool.config.get("script_path", "")
        entrypoint = tool.config.get("entrypoint", "run")
        if not script_path.exists():
            return ToolResponse(status=ExecutionStatus.ERROR, message=f"Script not found: {script_path}")

        start_time = datetime.now()
        try:
            spec = importlib.util.spec_from_file_location(tool.name, script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            func = getattr(module, entrypoint)
            result_data = await asyncio.wait_for(func(args), timeout=tool.timeout)
            status = ExecutionStatus.SUCCESS
            error_msg = None
        except Exception as e:
            status = ExecutionStatus.ERROR
            error_msg = str(e)
            result_data = None

        duration = int((datetime.now() - start_time).total_seconds() * 1000)
        log = ToolExecutionLog(tool_name=tool.name, input_args=args, output=result_data, duration_ms=duration, status=status, error_message=error_msg)
        await self._log_execution(log)
        return ToolResponse(status=status, data=result_data, message=error_msg, execution_id=log.id)

    async def _log_execution(self, log: ToolExecutionLog):
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(self.log_file_path, mode='a') as f:
            await f.write(log.model_dump_json() + "\n")
