# Data Model: Skill Markdown Preview

## Entities

### SkillDocumentation (Transient)
Represents the human-readable documentation for a specific skill.
- `skill_id`: UUID (Primary identifier for the associated skill)
- `content`: String (Raw markdown text from `skill.md` or `SKILL.md`)
- `file_name`: String (The exact name of the file found, e.g., "SKILL.md")

## Relationships
- A `Skill` has one optional `SkillDocumentation`.

## Validation Rules
- `content` should be treated as untrusted input and sanitized by the frontend before rendering.
- `skill_id` must exist in the `SkillRegistry`.
