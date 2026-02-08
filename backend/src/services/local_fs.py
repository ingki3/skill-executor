import os
from pathlib import Path
from typing import List, Dict

class LocalFSService:
    def __init__(self):
        # We assume the project root is where the server is started
        self.root_dir = Path(os.getcwd()).absolute()

    def validate_path_boundary(self, path_str: str) -> Path:
        """Ensure path is within project root."""
        path = Path(path_str).absolute()
        if not str(path).startswith(str(self.root_dir)):
            raise PermissionError(f"Access denied: Path {path_str} is outside of project root.")
        if not path.exists():
            raise FileNotFoundError(f"Path {path_str} not found.")
        if not path.is_dir():
            raise NotADirectoryError(f"Path {path_str} is not a directory.")
        return path

    def list_local_subdirectories(self, base_path_str: str) -> List[Dict]:
        """List immediate subdirectories with metadata check."""
        base_path = self.validate_path_boundary(base_path_str)
        
        results = []
        for item in base_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                has_metadata = self._check_metadata(item)
                results.append({
                    "name": item.name,
                    "path": str(item.absolute()),
                    "has_metadata": has_metadata
                })
        
        # Sort by name
        return sorted(results, key=lambda x: x["name"])

    def _check_metadata(self, path: Path) -> bool:
        """Check if path contains skill.yaml or SKILL.md."""
        for p in path.glob("skill.y*ml"):
            return True
        for p in path.glob("SKILL.md"):
            return True
        return False

local_fs_service = LocalFSService()