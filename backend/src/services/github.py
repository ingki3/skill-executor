import os
import shutil
from pathlib import Path
from git import Repo
from typing import Optional, Tuple
from urllib.parse import urlparse

class GitHubService:
    def __init__(self, temp_dir: str = ".temp_skills"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def _parse_github_url(self, url: str) -> Tuple[str, Optional[str], Optional[str]]:
        """
        Parses a GitHub URL to extract the repository URL, branch, and subdirectory.
        Supports standard repo URLs and tree URLs (e.g., /tree/branch/subdir).
        """
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")
        
        if len(path_parts) >= 4 and path_parts[2] == "tree":
            # Format: /user/repo/tree/branch/subdir...
            user = path_parts[0]
            repo = path_parts[1]
            branch = path_parts[3]
            subdir = "/".join(path_parts[4:])
            repo_url = f"{parsed.scheme}://{parsed.netloc}/{user}/{repo}.git"
            return repo_url, branch, subdir
        else:
            # Format: /user/repo or /user/repo.git
            if url.endswith(".git"):
                repo_url = url
            else:
                repo_url = f"{url}.git"
            return repo_url, None, None

    def clone_repository(self, url: str) -> Path:
        repo_url, branch, subdir = self._parse_github_url(url)
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        # Use a unique path or handle existing ones safely. For now, we clean up.
        target_path = self.temp_dir / repo_name
        
        if target_path.exists():
            shutil.rmtree(target_path)
            
        if branch:
            Repo.clone_from(repo_url, target_path, branch=branch, depth=1)
        else:
            Repo.clone_from(repo_url, target_path, depth=1)
            
        if subdir:
            return target_path / subdir
        return target_path

    def cleanup(self, path: Path):
        # We need to find the root of the temp repo to clean up correctly if we returned a subdir.
        # But 'path' might be the subdir.
        # Simple heuristic: go up until we hit temp_dir or reach root.
        # Or, just try to remove the path given. But if it's a subdir, the rest of the repo remains.
        # The best way is to clean up by repo_name. 
        # However, the registration service calls cleanup with the path returned by clone_repository.
        # If we return a subdir, we should be careful.
        
        # Let's verify if path is relative to temp_dir
        if not path.exists():
            return

        # If path is a subdirectory of a cloned repo, we want to delete the whole repo.
        # The Current implementation of clone_repository creates directories directly under temp_dir.
        # So we can traverse up until the parent is temp_dir.
        
        current = path
        while current.parent != self.temp_dir and current.parent != current:
            current = current.parent
            
        if current.parent == self.temp_dir:
            if current.exists():
                shutil.rmtree(current)

github_service = GitHubService()
