# Quickstart: Separate Prompt YAML Management

## 1. Adding a New Prompt
1. Create or open a YAML file in `backend/src/prompt/`.
2. Add a key-value pair using the literal block scalar for multi-line:
   ```yaml
   my_new_prompt: |
     Hello {name},
     Welcome to the system.
   ```

## 2. Using the Prompt in Code
```python
from src.core.prompt_loader import prompt_loader

# Fetch and format
template = prompt_loader.get("namespace", "my_new_prompt")
formatted = template.format(name="User")
```

## 3. Reloading Without Restart
If the server is running, trigger the reload endpoint:
```bash
curl -X POST http://localhost:8000/api/admin/prompts/reload
```
