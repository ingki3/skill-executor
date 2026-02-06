import os
from typing import Optional, Tuple
from src.core.vector_store import vector_store
from src.services.registry import registry_service
from src.models import Skill

class SearchService:
    def __init__(self):
        self.threshold = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.5"))

    def find_best_skill(self, query: str) -> Tuple[Optional[Skill], Optional[float]]:
        results = vector_store.search(query, top_k=1)
        if not results:
            return None, None
            
        skill_id, distance = results[0]
        
        # In FAISS L2, smaller distance means higher confidence.
        # We need to calibrate the threshold based on the embedding model.
        if distance > self.threshold:
            return None, distance
            
        skill = registry_service.get_skill(skill_id)
        return skill, distance

search_service = SearchService()
