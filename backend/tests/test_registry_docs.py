import pytest
from src.services.registry import RegistryService
from src.models import Skill, Complexity
from uuid import uuid4
from pathlib import Path

def test_read_documentation_success(tmp_path, monkeypatch):
    # Setup
    skill_id = uuid4()
    skill_dir = tmp_path / str(skill_id)
    skill_dir.mkdir()
    
    doc_file = skill_dir / "SKILL.md"
    doc_file.write_text("# Test Documentation", encoding="utf-8")
    
    metadata_path = skill_dir / "skill.json"
    
    skill = Skill(
        id=skill_id,
        name="Test Skill",
        description="A test skill",
        metadata_path=str(metadata_path),
        code_path=str(skill_dir / "main.py"),
        complexity=Complexity.SIMPLE,
        version="1.0",
        source_url="http://example.com"
    )
    
    # Mock get_skill
    def mock_get_skill(self, sid):
        if str(sid) == str(skill_id):
            return skill
        return None
        
    monkeypatch.setattr(RegistryService, "get_skill", mock_get_skill)
    
    # We can't easily instantiate RegistryService because it tries to load from disk and verify volumes.
    # But we can mock verify_volumes and _load_registry.
    monkeypatch.setattr(RegistryService, "verify_volumes", lambda self: None)
    monkeypatch.setattr(RegistryService, "_load_registry", lambda self: None)
    
    service = RegistryService(registry_path=str(tmp_path / "registry.json"))
    
    # Test
    doc = service.read_documentation(str(skill_id))
    
    assert doc is not None
    assert doc.skill_id == skill_id
    assert doc.content == "# Test Documentation"
    assert doc.file_name == "SKILL.md"

def test_read_documentation_not_found(tmp_path, monkeypatch):
    # Mock get_skill to return None
    monkeypatch.setattr(RegistryService, "get_skill", lambda self, sid: None)
    monkeypatch.setattr(RegistryService, "verify_volumes", lambda self: None)
    monkeypatch.setattr(RegistryService, "_load_registry", lambda self: None)
    
    service = RegistryService(registry_path=str(tmp_path / "registry.json"))
    
    doc = service.read_documentation("non-existent-id")
    assert doc is None
