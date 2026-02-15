from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List, Dict, Any
from src.services.tool_service import ToolService
from src.models.tool import ToolDefinition, ToolResponse
import os

router = APIRouter(prefix="/tools", tags=["tools"])

# Simple API Key Auth per CHK016/Spec Clarification
API_KEY = os.getenv("TOOL_API_KEY", "default-key")

async def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return x_api_key

@router.get("", response_model=List[ToolDefinition])
async def list_tools():
    service = ToolService()
    return await service.list_tools()

@router.post("/local", status_code=201)
async def register_local_tool(tool_data: Dict[str, Any], api_key: str = Depends(verify_api_key)):
    service = ToolService()
    # Logic to update registry via sequential queue
    try:
        result = await service.submit_registry_update(lambda: service.add_local_tool(tool_data))
        return {"message": "Tool registered", "name": tool_data.get("name")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{name}", status_code=204)
async def unregister_tool(name: str, api_key: str = Depends(verify_api_key)):
    service = ToolService()
    try:
        await service.submit_registry_update(lambda: service.remove_tool(name))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
