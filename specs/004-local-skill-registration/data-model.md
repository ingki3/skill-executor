# Data Model: Local Skill Registration

## Entities

### LocalRepositoryReference
Represents a search result from a local filesystem directory within the allowed project boundary.
- `absolute_path`: String (The validated absolute path searched)
- `found_skills`: List of `LocalSkillFolder`

### LocalSkillFolder
Represents a subdirectory identified as a potential skill.
- `name`: String (Folder name)
- `path`: String (Full absolute path to the folder)
- `has_metadata`: Boolean (Whether `skill.yaml` or `SKILL.md` was found)

## Relationships
- A `LocalRepositoryReference` contains many `LocalSkillFolder` items.

## Validation Rules
- `absolute_path` must be a child of the server's application root.
- Duplicate resolution: If a skill with the same metadata already exists in the `SkillRegistry`, the user must be prompted before the registration is processed.