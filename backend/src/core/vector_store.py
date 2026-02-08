import os
import faiss
import numpy as np
from typing import List, Tuple, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self, dimension: int = 768): # Default for embedding-001 is 768
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.skill_ids: List[str] = []
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)

    def get_embedding(self, text: str) -> np.ndarray:
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return np.array(result['embedding'], dtype=np.float32)
        except Exception as e:
            print(f"Embedding error: {e}")
            # Return a zero vector as fallback to avoid crashing
            return np.zeros(self.dimension, dtype=np.float32)

    def add_skill(self, skill_id: str, text: str):
        embedding = self.get_embedding(text)
        self.index.add(np.array([embedding]))
        self.skill_ids.append(skill_id)

    def search(self, query: str, top_k: int = 1) -> List[Tuple[str, float]]:
        if self.index.ntotal == 0:
            return []
            
        query_embedding = self.get_embedding(query)
        distances, indices = self.index.search(np.array([query_embedding]), top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                results.append((self.skill_ids[idx], float(distances[0][i])))
        return results

    def remove_all(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.skill_ids = []

# Global instance
vector_store = VectorStore()
