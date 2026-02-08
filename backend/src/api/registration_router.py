from fastapi import APIRouter, HTTPException, Query
from typing import List
from src.models import (
    Skill, 
    SkillRegistry,
    RegistrationBatch,
    BatchStatus,
    Judgment
)
from src.services.registration import registration_service
from src.services.registry import registry_service
from src.services.batch_store import batch_store_service

from pydantic import BaseModel
from uuid import UUID

class GitHubRegistrationRequest(BaseModel):
    repo_url: str
    selected_paths: List[str]

class JudgmentRequest(BaseModel):
    path: str
    judgment: Judgment

router = APIRouter(prefix="/skills", tags=["skills"])

@router.get("/parse-github-url")
async def parse_github_url(url: str = Query(..., description="GitHub URL to parse")):
    """Parse a GitHub URL to detect if it's a root repo or a deep link."""
    try:
        from src.services.github import github_service
        return github_service.parse_github_url(url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/register-batch")
async def start_batch_registration(request: GitHubRegistrationRequest):
    """Start an async bulk registration process."""
    try:
        batch_id = await registration_service.start_batch_scan(request.repo_url, request.selected_paths)
        return {"batch_id": batch_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/registration-batches")
async def list_registration_batches():
    """List all registration batches."""
    return batch_store_service.list_batches()

@router.get("/registration-batches/{id}")
async def get_batch_status(id: UUID):
    """Get the status of a registration batch."""
    batch = batch_store_service.get_batch(id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@router.post("/registration-batches/{id}/judge")
async def judge_batch_item(id: UUID, request: JudgmentRequest):
    """Approve or reject an item in a batch."""
    try:
        await registration_service.process_judgment(id, request.path, request.judgment)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/registration-batches/{id}/approve-all-safe")
async def approve_all_safe(id: UUID):
    """Approve all safe items in a batch."""
    try:
        count = await registration_service.approve_all_safe(id)
        return {"approved_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list-from-local")
async def list_local_skills(absolute_path: str = Query(..., description="Local absolute path")):
    """List sub-directories in a local path."""
    try:
        from src.services.local_fs import local_fs_service
        skills = local_fs_service.list_local_subdirectories(absolute_path)
        return {
            "absolute_path": absolute_path,
            "skills": skills
        }
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list local skills: {str(e)}")

@router.get("/list-from-repo")
async def list_repo_skills(repo_url: str = Query(..., description="GitHub repository URL")):
    """List sub-directories (potential skills) in a GitHub repository."""
    try:
        from src.services.github import github_service
        skills = await github_service.list_repository_skills(repo_url)
        return {"skills": skills}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list skills: {str(e)}")

@router.post("/register-bulk")
async def register_bulk(request: GitHubRegistrationRequest):
    """Register multiple skills from a GitHub repository."""
    try:
        results = []
        for path in request.selected_paths:
            skill = await registration_service.register_github_skill(request.repo_url, path)
            results.append(skill)
        return {"status": "success", "registered_skills": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk registration failed: {str(e)}")

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

@router.get("/{skill_id}/documentation")
async def get_skill_documentation(skill_id: str):
    doc = registry_service.read_documentation(skill_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documentation not found")
    return doc

@router.delete("/{skill_id}")
async def delete_skill(skill_id: str):
    registry_service.remove_skill(skill_id)
    return {"message": "Skill deleted successfully"}