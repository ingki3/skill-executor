import pytest
import asyncio
from uuid import UUID
from unittest.mock import MagicMock, patch
from src.services.registration import RegistrationService
from src.models.registration import BatchStatus, SafetyStatus

@pytest.mark.asyncio
async def test_batch_scanning_logic():
    repo_url = "https://github.com/test/repo"
    selected_paths = ["skill1", "skill2"]
    
    with patch("src.services.registration.github_service") as mock_github, \
         patch("src.services.registration.security_service") as mock_security, \
         patch("src.services.registration.batch_store_service") as mock_store:
        
        # Setup mocks
        mock_github.clone_repository.return_value = MagicMock()
        mock_security.scan_skill.return_value = (True, "Safe")
        mock_security.analyze_risk.return_value = []
        
        service = RegistrationService()
        
        # Test starting a batch scan
        batch_id = await service.start_batch_scan(repo_url, selected_paths)
        
        assert isinstance(batch_id, UUID)
        mock_store.add_batch.assert_called_once()
        
        # Wait for the background task to complete (or mock it better)
        # For unit test, we might want to test the internal processing method directly
        batch = mock_store.add_batch.call_args[0][0]
        await service._run_batch_scan(batch)
        
        assert batch.status == BatchStatus.REVIEW_REQUIRED
        assert len(batch.items) == 2
        assert batch.items[0].safety_status == SafetyStatus.SAFE
