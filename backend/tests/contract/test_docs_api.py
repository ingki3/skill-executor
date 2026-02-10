from fastapi.testclient import TestClient
from src.main import app
from src.services.registry import registry_service
from src.models import SkillDocumentation
from uuid import uuid4
import pytest

client = TestClient(app)

def test_get_documentation_endpoint(monkeypatch):
    skill_id = uuid4()
    
    expected_doc = SkillDocumentation(
        skill_id=skill_id,
        content="# Doc",
        file_name="SKILL.md"
    )
    
    def mock_read_doc(sid):
        if sid == str(skill_id):
            return expected_doc
        return None
        
    monkeypatch.setattr(registry_service, "read_documentation", mock_read_doc)
    
    response = client.get(f"/skills/{skill_id}/documentation")
    assert response.status_code == 200
    assert response.json() == {
        "skill_id": str(skill_id),
        "content": "# Doc",
        "file_name": "SKILL.md"
    }

def test_get_documentation_404(monkeypatch):
    monkeypatch.setattr(registry_service, "read_documentation", lambda sid: None)
    response = client.get(f"/skills/{uuid4()}/documentation")
    assert response.status_code == 404
