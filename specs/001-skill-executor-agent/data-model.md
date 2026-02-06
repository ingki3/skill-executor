# Data Model: Skill Executor Agent

## Entities

### Skill
Represents a registered capability.
- `id`: UUID (Primary Key)
- `name`: String (Unique)
- `description`: Text
- `metadata_path`: String (Path to the yaml file)
- `code_path`: String (Path to the python/script file)
- `complexity`: Enum (SIMPLE, COMPLEX)
- `version`: String (Semantic versioning)
- `source_url`: String (GitHub URL)
- `last_synced`: DateTime
- `created_at`: DateTime

### SkillRegistry (Local JSON)
The persistent store for metadata.
- `skills`: List[Skill]
- `last_updated`: DateTime

### ExecutionLog
Audit trail for executions.
- `id`: UUID
- `skill_id`: UUID (Foreign Key)
- `query`: Text
- `confidence_score`: Float (Vector distance)
- `steps`: JSON (List of ReACT steps)
- `outcome`: Enum (SUCCESS, FAILURE, NO_MATCH)
- `model_used`: String
- `duration`: Float

## State Transitions: Skill Registration & Sync
1. **PENDING**: URL received.
2. **CLONING/PULLING**: Repository being downloaded/updated.
3. **SCANNING**: LLM-based security verification in progress.
4. **REGISTERED/SYNCED**: Validation passed, added/updated in FAISS and JSON.
5. **REJECTED**: Security risk found.