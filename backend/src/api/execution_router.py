from fastapi import APIRouter, HTTPException, Body
from src.models import ExecutionLog, ExecutionOutcome
from src.services.execution import execution_service

router = APIRouter(prefix="/skills", tags=["execution"])

@router.post("/execute", response_model=ExecutionLog)
async def execute_skill(query: str = Body(..., embed=True)):
    log = await execution_service.execute_query(query)
    
    if log.outcome == ExecutionOutcome.NO_MATCH:
        raise HTTPException(
            status_code=404, 
            detail=f"No matching skill found. Confidence distance: {log.confidence_score}"
        )
        
    return log
