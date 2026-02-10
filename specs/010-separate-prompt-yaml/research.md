# Research: Separate Prompt YAML Management

## Phase 0: Research & Decisions

### 1. Template Storage Format
**Decision**: Use YAML with a single top-level key per file or multiple keys per file.
**Rationale**: YAML's literal block scalar (`|`) is perfect for multi-line prompts. It keeps the prompts readable and maintains indentation.
**Decision**: Support multiple keys per YAML file (organized by service, e.g., `registration.yaml`).

### 2. Loading Mechanism
**Decision**: Create a `PromptLoader` class in `backend/src/core/prompt_loader.py`.
**Rationale**: 
- Provides a centralized entry point.
- Can implement caching using `functools.lru_cache` to avoid repeated disk reads.
- Can handle `.format(**kwargs)` for dynamic placeholders.

### 3. File Organization
**Decision**: Group prompts by functional area in `backend/src/prompt/`.
- `registration.yaml`: Prompts for risk analysis and metadata extraction.
- `execution.yaml`: Prompts for the ReACT loop and direct execution.
- `search.yaml`: Prompts for semantic search refinement (if applicable).

### 4. Placeholder Syntax
**Decision**: Use standard Python `.format()` syntax (curly braces `{}`).
**Rationale**: Native support in Python, no need for Jinja2 if logic is simple. If complex branching is needed later, we can swap the internal implementation to Jinja2 without changing the YAML files.

## Alternatives Considered
- **Jinja2**: Overkill for simple string substitution.
- **JSON**: Poor multi-line support.
- **Python constant files**: Still "hardcoded" in code, though cleaner. YAML allows non-technical users to edit prompts more easily.

## Conclusion
The path forward is a YAML-based filesystem registry with a Pythonic loader utility.
