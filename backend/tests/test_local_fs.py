import os
import pytest
from pathlib import Path
from src.services.local_fs import LocalFSService

def test_validate_path_boundary_success():
    service = LocalFSService()
    # Current dir should be within project root
    path = os.getcwd()
    validated = service.validate_path_boundary(path)
    assert str(validated) == str(Path(path).absolute())

def test_validate_path_boundary_failure():
    service = LocalFSService()
    # /etc is definitely outside project root
    with pytest.raises(PermissionError):
        service.validate_path_boundary("/etc")

def test_list_local_subdirectories():
    service = LocalFSService()
    # List current directory
    results = service.list_local_subdirectories(".")
    assert isinstance(results, list)
    # Check for backend folder
    assert any(r["name"] == "backend" for r in results)
