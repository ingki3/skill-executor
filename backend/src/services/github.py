import os
import shutil
from pathlib import Path
from git import Repo
from typing import Optional

class GitHubService:
    def __init__(self, temp_dir: str = ".temp_skills"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def clone_repository(self, url: str) -> Path:
        repo_name = url.split("/")[-1].replace(".git", "")
        target_path = self.temp_dir / repo_name
        
        if target_path.exists():
            shutil.rmtree(target_path)
            
        Repo.clone_from(url, target_path, depth=1)
        return target_path

    def cleanup(self, path: Path):
        if path.exists() and path.is_relative_to(self.temp_dir):
            shutil.rmtree(path)

github_service = GitHubService()
