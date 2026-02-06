from fastapi import APIRouter, HTTPException, Query
from typing import List
from src.models import Skill, SkillRegistry
from src.services.registration import registration_service
from src.services.registry import registry_service

router = APIRouter(prefix="/skills", tags=["skills"])

@router.post("/register", response_model=Skill, status_code=201)
async def register_skill(url: str = Query(..., description="GitHub repository URL")):
    try:
        skill = await registration_service.register_from_url(url)
        return skill
    except ValueError as e:
        raise HTTPException(status_code=403 if "Security" in str(e) else 400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/{skill_id}/sync", response_model=Skill)
async def sync_skill(skill_id: str):
    try:
        skill = await registration_service.sync_skill(skill_id)
        return skill
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

@router.get("", response_model=List[Skill])
async def list_skills():
    registry = registry_service.list_skills()
    return registry.skills

@router.get("/{skill_id}", response_model=Skill)
async def get_skill(skill_id: str):
    skill = registry_service.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.delete("/{skill_id}")
async def delete_skill(skill_id: str):
    registry_service.remove_skill(skill_id)
    return {"message": "Skill deleted successfully"}
