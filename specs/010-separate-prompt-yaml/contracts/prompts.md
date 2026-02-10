# API Contract: Admin Prompts

## Admin - Reload Prompts
`POST /api/admin/prompts/reload`

Forces the `PromptLoader` to clear its internal cache and re-read all YAML files from disk.

**Response** (200 OK):
```json
{
  "status": "success",
  "reloaded_namespaces": ["registration", "execution", "search"]
}
```
