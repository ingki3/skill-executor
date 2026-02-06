import json
import os
from typing import Optional
from pathlib import Path
from datetime import datetime
from src.models import Skill, SkillRegistry
from src.core.vector_store import vector_store

class RegistryService:
    def __init__(self, registry_path: str = ".skills/registry.json"):
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self._load_registry()

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

    def list_skills(self) -> SkillRegistry:
        return self.registry

registry_service = RegistryService()
