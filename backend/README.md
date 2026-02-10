# Skill Executor Backend

## Prompt Management

All LLM prompts are externalized into YAML files located in `src/prompt/`. This allows for easier editing and version control without modifying Python code.

### File Structure
- `src/prompt/security.yaml`: Prompts for risk analysis and scanning.
- `src/prompt/execution.yaml`: Prompts for the ReACT loop and direct execution.
- `src/prompt/search.yaml`: Prompts for semantic search refinement.

### Usage in Code
Use the global `prompt_loader` instance:
```python
from src.core.prompt_loader import prompt_loader

template = prompt_loader.get("namespace", "key")
formatted = template.format(var1="value1", ...)
```

### Reloading
To reload prompts from disk without restarting the server, use the following endpoint:
```bash
curl -X POST http://localhost:8000/execution/prompts/reload
```
