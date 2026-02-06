import os
import yaml
import shutil
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from typing import Optional
from src.models import Skill, Complexity
from src.services.github import github_service
from src.services.security import security_service
from src.services.registry import registry_service

class RegistrationService:
    def __init__(self, storage_dir: str = ".skills"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def register_from_url(self, url: str) -> Skill:
        # 1. Clone
        temp_path = github_service.clone_repository(url)
        try:
            # 2. Find and Load Metadata
            metadata_file = self._find_metadata(temp_path)
            if not metadata_file:
                raise ValueError("Skill metadata (skill.yaml) not found in repository.")
            
            with open(metadata_file, "r") as f:
                metadata = yaml.safe_load(f)

            # 3. Security Scan
            prompt = metadata.get("prompt", "")
            code_file = temp_path / metadata.get("code_file", "")
            if not code_file.exists():
                raise ValueError(f"Code file {metadata.get('code_file')} not found.")
            
            with open(code_file, "r") as f:
                code = f.read()

            is_safe, reason = await security_service.scan_skill(prompt, code)
            if not is_safe:
                raise ValueError(f"Security Rejection: {reason}")

            # 4. Permanent Storage
            skill_id = uuid4()
            skill_dir = self.storage_dir / str(skill_id)
            skill_dir.mkdir(parents=True, exist_ok=True)
            
            shutil.copytree(temp_path, skill_dir, dirs_exist_ok=True)

            # 5. Create Skill Model
            skill = Skill(
                id=skill_id,
                name=metadata.get("name", "Unknown Skill"),
                description=metadata.get("description", ""),
                metadata_path=str(skill_dir / "skill.yaml"),
                code_path=str(skill_dir / metadata.get("code_file")),
                complexity=Complexity(metadata.get("complexity", "SIMPLE").upper()),
                version=metadata.get("version", "1.0.0"),
                source_url=url
            )

            # 6. Registry Update
            registry_service.add_skill(skill)
            return skill

        finally:
            github_service.cleanup(temp_path)

    def _find_metadata(self, path: Path) -> Optional[Path]:
        # Search for skill.yaml or skill.yml
        for p in path.glob("**/skill.y*ml"):
            return p
        return None

    async def sync_skill(self, skill_id: str) -> Skill:
        skill = registry_service.get_skill(skill_id)
        if not skill:
            raise ValueError("Skill not found.")
        
        # Re-register using same URL
        updated_skill = await self.register_from_url(skill.source_url)
        # Preserve original ID if needed, but here we just replace it for simplicity
        return updated_skill

registration_service = RegistrationService()
