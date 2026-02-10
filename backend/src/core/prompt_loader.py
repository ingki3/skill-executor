
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class PromptLoader:
    def __init__(self, prompt_dir: str = "backend/src/prompt"):
        self.prompt_dir = Path(prompt_dir)
        self._cache: Dict[str, Dict[str, str]] = {}

    def _load_namespace(self, namespace: str) -> Dict[str, str]:
        if namespace in self._cache:
            return self._cache[namespace]

        file_path = self.prompt_dir / f"{namespace}.yaml"
        if not file_path.exists():
            # If not found in default dir, try relative to src
            # (Handy for different execution contexts)
            alt_path = Path(__file__).parent.parent / "prompt" / f"{namespace}.yaml"
            if alt_path.exists():
                file_path = alt_path
            else:
                logger.error(f"Prompt namespace file not found: {file_path}")
                return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if not isinstance(data, dict):
                    logger.error(f"Invalid YAML format in {file_path}. Expected dictionary.")
                    return {}
                self._cache[namespace] = data
                return data
        except Exception as e:
            logger.error(f"Error loading prompt namespace {namespace}: {e}")
            return {}

    def get(self, namespace: str, key: str) -> str:
        """Retrieve a prompt template string by namespace and key."""
        templates = self._load_namespace(namespace)
        template = templates.get(key)
        if template is None:
            logger.warning(f"Prompt key '{key}' not found in namespace '{namespace}'")
            return f"Prompt [{namespace}:{key}] not found"
        return str(template)

    def reload(self):
        """Clear the internal cache to force re-reading from disk."""
        self._cache.clear()
        logger.info("Prompt cache cleared.")

# Singleton instance
prompt_loader = PromptLoader()
