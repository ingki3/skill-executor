# Data Model: Separate Prompt YAML Management

## Entities

### PromptConfig
A conceptual entity representing a collection of prompt templates loaded from a YAML file.

| Field | Type | Description |
|-------|------|-------------|
| `namespace` | String | The YAML filename (e.g., `registration`) |
| `templates` | Dict[String, String] | Mapping of prompt keys to template strings |

### PromptTemplate
A specific template string with optional placeholders.

| Property | Type | Description |
|----------|------|-------------|
| `key` | String | Unique identifier within a namespace (e.g., `risk_scan`) |
| `raw_text` | String | The raw string from YAML |
| `formatted_text` | String | The text after placeholder injection |

## Validation Rules
1. YAML files must be valid syntax.
2. Template keys must be unique within a file.
3. Placeholders in templates must match the keys provided during formatting (handle `KeyError`).
