import httpx
import os
import shutil
import tempfile
import re
from git import Repo
from pathlib import Path
from typing import List, Dict

class GitHubService:
    def __init__(self):
        self.api_base = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")
        self.temp_base = Path(".temp_skills")
        self.temp_base.mkdir(parents=True, exist_ok=True)

    def clone_repository(self, repo_url: str, branch: str = None, depth: int = 1) -> Path:
        """Clone a repository to a temporary directory."""
        temp_dir = Path(tempfile.mkdtemp(dir=self.temp_base))
        print(f"Cloning {repo_url} (branch: {branch}) to {temp_dir}")
        
        kwargs = {"depth": depth}
        if branch:
            kwargs["branch"] = branch
            
        Repo.clone_from(repo_url, temp_dir, **kwargs)
        return temp_dir

    def cleanup(self, path: Path):
        """Remove a temporary directory."""
        if path.exists() and str(path).startswith(str(self.temp_base)):
            shutil.rmtree(path)

    def parse_github_url(self, url: str) -> Dict:
        """Parse a GitHub URL into components, supporting tree and blob links."""
        # Support tree (folders) and blob (files)
        pattern = r"https://github\.com/([^/]+)/([^/]+)(?:/(?:tree|blob)/([^/]+)(?:/(.*))?)?"
        match = re.match(pattern, url.rstrip("/"))
        if not match:
            raise ValueError("Invalid GitHub repository URL")
        
        owner = match.group(1)
        repo = match.group(2).replace(".git", "")
        branch = match.group(3)
        path = match.group(4)
        
        is_deep_link = bool(path)
        is_blob = "/blob/" in url
        
        # If it's a blob link (file), we resolve to parent directory
        if is_blob and path:
            path = str(Path(path).parent)
            if path == ".":
                path = ""

        return {
            "owner": owner,
            "repo": repo,
            "branch": branch,
            "sub_path": path,
            "is_deep_link": is_deep_link,
            "base_url": f"https://github.com/{owner}/{repo}"
        }

    async def list_repository_skills(self, repo_url: str) -> List[Dict[str, str]]:
        """List directories in the repository as potential skills."""
        try:
            parsed = self.parse_github_url(repo_url)
        except ValueError:
            raise ValueError("Invalid GitHub repository URL")

        owner = parsed["owner"]
        repo = parsed["repo"]
        target_path = parsed["sub_path"]
        branch = parsed["branch"]
        
        # If deep link provided, look in that path. 
        # Otherwise check 'skills' and root.
        paths_to_check = [target_path] if target_path else ["skills", ""]
        
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"

        skills = []
        async with httpx.AsyncClient() as client:
            for path in paths_to_check:
                # If path is None/Empty, contents API uses root
                api_path = path if path else ""
                url = f"{self.api_base}/repos/{owner}/{repo}/contents/{api_path}"
                
                params = {}
                if branch:
                    params["ref"] = branch
                
                try:
                    resp = await client.get(url, headers=headers, params=params, timeout=10.0)
                    if resp.status_code == 200:
                        contents = resp.json()
                        if isinstance(contents, list):
                            for item in contents:
                                if item["type"] == "dir" and not item["name"].startswith("."):
                                    skills.append({
                                        "name": item["name"],
                                        "path": item["path"]
                                    })
                        if skills:
                            break # Found some skills
                except Exception as e:
                    print(f"Error listing {path}: {e}")
        
        return skills

github_service = GitHubService()
