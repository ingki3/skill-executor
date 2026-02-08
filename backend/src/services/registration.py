import os
import re
import yaml
import shutil
import asyncio
from pathlib import Path
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, List
from src.models import Skill, Complexity
from src.services.github import github_service
from src.services.security import security_service
from src.services.registry import registry_service
from src.services.batch_store import batch_store_service
from src.services.local_fs import local_fs_service
from src.models import (
    RegistrationBatch,
    RegistrationQueueItem,
    BatchStatus,
    SafetyStatus,
    Judgment
)

class RegistrationService:
    def __init__(self, storage_dir: str = ".skills"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.pending_dir = Path(".pending_registrations")
        self.pending_dir.mkdir(parents=True, exist_ok=True)

    async def start_batch_scan(self, repo_url: str, selected_paths: List[str]) -> UUID:
        """Initialize a batch scan process. Supports both GitHub URLs and local paths."""
        batch = RegistrationBatch(repo_url=repo_url)
        for path in selected_paths:
            if not path:
                continue
            # For local paths, the 'path' is absolute. For GitHub, it's relative.
            name = Path(path).name
            batch.items.append(RegistrationQueueItem(
                path=path,
                name=name
            ))
        
        batch_store_service.add_batch(batch)
        
        # Start background task
        asyncio.create_task(self._run_batch_scan(batch))
        
        return batch.id

    def _is_github_url(self, url: str) -> bool:
        return url.startswith("http") or url.startswith("git@")

    async def _run_batch_scan(self, batch: RegistrationBatch):
        """Internal method to process a batch of skills."""
        is_github = self._is_github_url(batch.repo_url)
        temp_repo_path = None
        
        try:
            if is_github:
                try:
                    parsed = github_service.parse_github_url(batch.repo_url)
                    base_url = parsed["base_url"]
                    clone_branch = parsed["branch"]
                except:
                    base_url = batch.repo_url
                    clone_branch = None
                temp_repo_path = github_service.clone_repository(base_url, branch=clone_branch)
            
            for item in batch.items:
                item.safety_status = SafetyStatus.SCANNING
                batch_store_service.update_batch(batch)
                
                if is_github:
                    skill_source_path = temp_repo_path / item.path
                else:
                    # For local, item.path is absolute path
                    try:
                        skill_source_path = local_fs_service.validate_path_boundary(item.path)
                    except Exception as e:
                        item.safety_status = SafetyStatus.FAILED
                        item.error_message = str(e)
                        continue

                if not skill_source_path.exists():
                    item.safety_status = SafetyStatus.FAILED
                    item.error_message = f"Path {item.path} not found"
                    continue

                metadata_file = self._find_metadata(skill_source_path)
                if not metadata_file:
                    item.safety_status = SafetyStatus.FAILED
                    item.error_message = "Metadata (skill.yaml or SKILL.md) not found"
                    continue

                # Read code for preview and scan
                with open(metadata_file, "r") as f:
                    if metadata_file.name == "SKILL.md":
                        content = f.read()
                        if content.startswith("---"):
                            end_idx = content.find("---", 3)
                            metadata = yaml.safe_load(content[3:end_idx]) if end_idx != -1 else {}
                        else:
                            metadata = yaml.safe_load(content)
                    else:
                        metadata = yaml.safe_load(f)

                prompt = metadata.get("prompt", "")
                code_filename = metadata.get("code_file")
                code_file = skill_source_path / code_filename if code_filename else metadata_file
                
                with open(code_file, "r") as f:
                    item.code_content = f.read()

                # Analyze Risk
                item.risk_findings = await security_service.analyze_risk(item.code_content)
                
                # Full Scan
                is_safe, reason = await security_service.scan_skill(prompt, item.code_content)
                
                if not is_safe or len(item.risk_findings) > 0:
                    item.safety_status = SafetyStatus.RISKY
                else:
                    item.safety_status = SafetyStatus.SAFE
                
                batch_store_service.update_batch(batch)

            batch.status = BatchStatus.REVIEW_REQUIRED
            batch_store_service.update_batch(batch)

        except Exception as e:
            print(f"Batch scan failed: {e}")
            batch.status = BatchStatus.FAILED
            batch_store_service.update_batch(batch)
        finally:
            if temp_repo_path:
                github_service.cleanup(temp_repo_path)

    async def process_judgment(self, batch_id: UUID, path: str, judgment: Judgment):
        """Process a manual judgment for a skill in a batch."""
        batch = batch_store_service.get_batch(batch_id)
        if not batch:
            raise ValueError("Batch not found")
        
        for item in batch.items:
            if item.path == path:
                if item.judgment != Judgment.PENDING:
                    return
                
                item.judgment = judgment
                
                if judgment == Judgment.APPROVED:
                    # Register the skill
                    if self._is_github_url(batch.repo_url):
                        await self.register_github_skill(batch.repo_url, item.path, bypass_security=True)
                    else:
                        await self.register_local_skill(item.path, bypass_security=True)
                
                batch_store_service.update_batch(batch)
                
                if all(i.judgment != Judgment.PENDING for i in batch.items):
                    batch.status = BatchStatus.COMPLETED
                    batch_store_service.update_batch(batch)
                return
        
        raise ValueError(f"Path {path} not found in batch")

    async def approve_all_safe(self, batch_id: UUID) -> int:
        """Approve all skills in a batch that are marked as SAFE."""
        batch = batch_store_service.get_batch(batch_id)
        if not batch:
            raise ValueError("Batch not found")
        
        count = 0
        for item in batch.items:
            if item.safety_status == SafetyStatus.SAFE and item.judgment == Judgment.PENDING:
                await self.process_judgment(batch_id, item.path, Judgment.APPROVED)
                count += 1
        return count

    async def register_local_skill(self, absolute_path: str, bypass_security: bool = False) -> Skill:
        """Register a skill from a local directory."""
        path = local_fs_service.validate_path_boundary(absolute_path)
        metadata_file = self._find_metadata(path)
        if not metadata_file:
            raise ValueError(f"No skill metadata found in {absolute_path}")
        
        return await self._process_registration(absolute_path, path, metadata_file, bypass_security=bypass_security)

    async def register_github_skill(self, repo_url: str, sub_path: str, branch: str = None, bypass_security: bool = False) -> Skill:
        """Register a specific skill from a repository sub-path."""
        try:
            parsed = github_service.parse_github_url(repo_url)
            base_url = parsed["base_url"]
            clone_branch = branch or parsed["branch"]
        except ValueError:
            base_url = repo_url
            clone_branch = branch

        temp_repo_path = github_service.clone_repository(base_url, branch=clone_branch)
        try:
            skill_source_path = temp_repo_path / sub_path
            if not skill_source_path.exists():
                raise ValueError(f"Path {sub_path} not found in repository.")
            
            metadata_file = self._find_metadata(skill_source_path)
            if not metadata_file:
                raise ValueError(f"No skill metadata found in {sub_path}")

            return await self._process_registration(repo_url, skill_source_path, metadata_file, bypass_security=bypass_security)

        finally:
            github_service.cleanup(temp_repo_path)

    async def _process_registration(self, url: str, source_path: Path, metadata_file: Path, bypass_security: bool = False) -> Skill:
        with open(metadata_file, "r") as f:
            if metadata_file.name == "SKILL.md":
                content = f.read()
                if content.startswith("---"):
                    end_idx = content.find("---", 3)
                    metadata = yaml.safe_load(content[3:end_idx]) if end_idx != -1 else {}
                else:
                    metadata = yaml.safe_load(content)
            else:
                metadata = yaml.safe_load(f)

        prompt = metadata.get("prompt", "")
        code_filename = metadata.get("code_file")
        code_file = source_path / code_filename if code_filename else metadata_file
        
        with open(code_file, "r") as f:
            code = f.read()

        if not bypass_security:
            is_safe, reason = await security_service.scan_skill(prompt, code)
            if not is_safe:
                raise ValueError(f"Security Rejection: {reason}")

        # Check for duplicates (T015)
        # We'll use name and version for now
        existing_skills = registry_service.list_skills().skills
        for s in existing_skills:
            if s.name == metadata.get("name") and s.version == metadata.get("version", "1.0.0"):
                # Implementation of confirmation dialog is in frontend (T016)
                # Here we just proceed if we reached this point (bypass_security is usually True for approvals)
                pass

        skill_id = uuid4()
        skill_dir = self.storage_dir / str(skill_id)
        skill_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, skill_dir, dirs_exist_ok=True)

        skill = Skill(
            id=skill_id,
            name=metadata.get("name", source_path.name),
            description=metadata.get("description", ""),
            metadata_path=str(skill_dir / metadata_file.name),
            code_path=str(skill_dir / code_file.name),
            complexity=Complexity(metadata.get("complexity", "SIMPLE").upper()),
            version=metadata.get("version", "1.0.0"),
            source_url=url if self._is_github_url(url) else f"file://{url}"
        )

        registry_service.add_skill(skill)
        return skill

    async def register_from_url(self, url: str) -> Skill:
        if not self._is_github_url(url):
            return await self.register_local_skill(url)

        # Check for GitHub deep link
        try:
            parsed = github_service.parse_github_url(url)
            if parsed["sub_path"] or parsed["branch"]:
                return await self.register_github_skill(parsed["base_url"], parsed["sub_path"] or "", parsed["branch"])
        except ValueError:
            pass

        # Fallback for standard URL
        temp_path = github_service.clone_repository(url)
        try:
            metadata_file = self._find_metadata(temp_path)
            if not metadata_file:
                raise ValueError("Skill metadata (skill.yaml or SKILL.md) not found in repository.")
            
            return await self._process_registration(url, temp_path, metadata_file)

        finally:
            github_service.cleanup(temp_path)

    def _find_metadata(self, path: Path) -> Optional[Path]:
        for p in path.glob("skill.y*ml"):
            return p
        for p in path.glob("SKILL.md"):
            return p
        # Recursive search if not in root of source_path
        for p in path.glob("**/skill.y*ml"):
            return p
        for p in path.glob("**/SKILL.md"):
            return p
        return None

    async def sync_skill(self, skill_id: UUID) -> Skill:
        skill = registry_service.get_skill(str(skill_id))
        if not skill:
            raise ValueError("Skill not found.")
        return await self.register_from_url(skill.source_url.replace("file://", ""))

registration_service = RegistrationService()
