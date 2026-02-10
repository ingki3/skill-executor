
import json
import asyncio
from pathlib import Path
from uuid import UUID
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from ..models.execution import ExecutionSession, ExecutionStatus

class SessionRegistry:
    def __init__(self, storage_dir: str = ".skill-executor-data/sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._sessions: Dict[UUID, ExecutionSession] = {}
        self._load_sessions()

    def _load_sessions(self):
        """FR-002: Restore sessions from JSON serialization on startup."""
        for file_path in self.storage_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    session_data = json.load(f)
                    session = ExecutionSession.model_validate(session_data)
                    self._sessions[session.session_id] = session
            except Exception as e:
                print(f"Failed to load session {file_path}: {e}")

    def create_session(self, skill_id: str, mode: str, config: dict = None) -> ExecutionSession:
        session = ExecutionSession(
            skill_id=skill_id,
            mode=mode,
            status=ExecutionStatus.RUNNING,
            config=config or {}
        )
        self._sessions[session.session_id] = session
        self.save_session(session.session_id)
        return session

    def get_session(self, session_id: UUID) -> Optional[ExecutionSession]:
        return self._sessions.get(session_id)

    def update_session(self, session_id: UUID, **kwargs):
        session = self.get_session(session_id)
        if session:
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            session.last_active = datetime.now()
            self.save_session(session_id)

    def add_message(self, session_id: UUID, message):
        session = self.get_session(session_id)
        if session:
            session.history.append(message)
            session.last_active = datetime.now()
            self.save_session(session_id)

    def list_active_sessions(self) -> List[ExecutionSession]:
        return [s for s in self._sessions.values() if s.status in [ExecutionStatus.RUNNING, ExecutionStatus.PAUSED]]

    async def start_cleanup_task(self):
        """FR-006: Background task for 30-minute session cleanup."""
        while True:
            await asyncio.sleep(60) # Check every minute
            self.cleanup_expired_sessions()

    def cleanup_expired_sessions(self, timeout_minutes: int = 30):
        now = datetime.now()
        expired_ids = [
            sid for sid, s in self._sessions.items()
            if now - s.last_active > timedelta(minutes=timeout_minutes)
        ]
        for sid in expired_ids:
            # Delete file and memory
            file_path = self.storage_dir / f"{sid}.json"
            if file_path.exists():
                file_path.unlink()
            del self._sessions[sid]
            print(f"Cleaned up expired session {sid}")

    def save_session(self, session_id: UUID):
        session = self.get_session(session_id)
        if session:
            file_path = self.storage_dir / f"{session_id}.json"
            with open(file_path, "w") as f:
                f.write(session.model_dump_json())

# Global registry instance
session_registry = SessionRegistry()
