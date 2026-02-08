import json
import os
from typing import Optional
from pathlib import Path
from datetime import datetime
from src.models import Skill, SkillRegistry, SkillDocumentation
from src.core.vector_store import vector_store

class RegistryService:
    def __init__(self, registry_path: str = ".skills/registry.json"):
        self.registry_path = Path(registry_path)
        self.verify_volumes()
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self._load_registry()

    def verify_volumes(self):
        """Verify that necessary volumes are mounted and writable."""
        required_volumes = [".skills", ".skill-executor-data", ".temp_skills"]
        for vol in required_volumes:
            path = Path(vol)
            if not path.exists():
                print(f"Warning: Volume {vol} does not exist. Creating it.")
                path.mkdir(parents=True, exist_ok=True)
            
            # Check writability
            if not os.access(path, os.W_OK):
                print(f"Error: Volume {vol} is not writable.")
            else:
                print(f"Volume {vol} is verified and writable.")

    def _load_registry(self):
        if self.registry_path.exists():
            with open(self.registry_path, "r") as f:
                data = json.load(f)
                self.registry = SkillRegistry(**data)
        else:
            self.registry = SkillRegistry()
            self._save_registry()
        
        # Re-index skills in vector store
        vector_store.remove_all()
        for skill in self.registry.skills:
            vector_store.add_skill(str(skill.id), f"{skill.name} {skill.description}")

    def _save_registry(self):
        with open(self.registry_path, "w") as f:
            f.write(self.registry.model_dump_json(indent=2))

    def add_skill(self, skill: Skill):
        # Remove existing if ID matches (update)
        self.registry.skills = [s for s in self.registry.skills if s.id != skill.id]
        self.registry.skills.append(skill)
        self.registry.last_updated = datetime.now()
        self._save_registry()
        vector_store.add_skill(str(skill.id), f"{skill.name} {skill.description}")

    def remove_skill(self, skill_id: str):
        self.registry.skills = [s for s in self.registry.skills if str(s.id) != skill_id]
        self.registry.last_updated = datetime.now()
        self._save_registry()
        self._load_registry() # Simple way to re-index everything

    def get_skill(self, skill_id: str) -> Optional[Skill]:
        for skill in self.registry.skills:
            if str(skill.id) == skill_id:
                return skill
        return None

    def read_documentation(self, skill_id: str) -> Optional[SkillDocumentation]:
        skill = self.get_skill(skill_id)
        if not skill:
            return None
            
        try:
            # metadata_path should be relative to workspace root or absolute
            # We assume it is a valid path string that can be resolved
            skill_dir = Path(skill.metadata_path).parent
            
            for filename in ["SKILL.md", "skill.md"]:
                doc_path = skill_dir / filename
                if doc_path.exists():
                    content = doc_path.read_text(encoding="utf-8")
                    return SkillDocumentation(
                        skill_id=skill.id,
                        content=content,
                        file_name=filename
                    )
        except Exception as e:
            print(f"Error reading documentation for skill {skill_id}: {e}")
            
        return None

    def list_skills(self) -> SkillRegistry:
        return self.registry

registry_service = RegistryService()
