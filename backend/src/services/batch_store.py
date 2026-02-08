import json
import os
from pathlib import Path
from typing import List, Optional
from uuid import UUID
from src.models.registration import RegistrationBatch, BatchStatus

class BatchStoreService:
    def __init__(self, storage_path: str = ".pending_registrations/registry.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.batches: List[RegistrationBatch] = []
        self._load_batches()

    def _load_batches(self):
        if self.storage_path.exists():
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                self.batches = [RegistrationBatch(**b) for b in data]

    def _save_batches(self):
        with open(self.storage_path, "w") as f:
            json.dump([b.model_dump(mode='json') for b in self.batches], f, indent=2)

    def add_batch(self, batch: RegistrationBatch):
        self.batches.append(batch)
        self._save_batches()

    def get_batch(self, batch_id: UUID) -> Optional[RegistrationBatch]:
        for batch in self.batches:
            if batch.id == batch_id:
                return batch
        return None

    def update_batch(self, batch: RegistrationBatch):
        for i, b in enumerate(self.batches):
            if b.id == batch.id:
                self.batches[i] = batch
                self._save_batches()
                return
        self.add_batch(batch)

    def list_batches(self) -> List[RegistrationBatch]:
        return self.batches

    def cleanup_completed_batches(self):
        """Remove batches that are marked as COMPLETED or FAILED."""
        self.batches = [b for b in self.batches if b.status not in [BatchStatus.COMPLETED, BatchStatus.FAILED]]
        self._save_batches()

batch_store_service = BatchStoreService()
