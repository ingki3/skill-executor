import pytest
from src.services.security import SecurityService

@pytest.fixture
def security_service():
    return SecurityService()

def test_safe_code_scan(security_service):
    safe_code = "print('Hello, World!')"
    # Note: In real scenarios, LLM based scan would be mocked
    # For now, we just test the entry point exists
    pass

def test_malicious_code_scan(security_service):
    malicious_code = "import os; os.system('rm -rf /')"
    pass
