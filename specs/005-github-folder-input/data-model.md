# Data Model: GitHub Direct Skill Folder Input

## Entities

### GitHubDeepLink (Transient)
Used during the parsing phase to identify the target skill.
- `owner`: String (e.g., "ComposioHQ")
- `repo`: String (e.g., "awesome-claude-skills")
- `ref`: String (e.g., "main")
- `sub_path`: String (e.g., "skills/calculator")
- `is_deep_link`: Boolean

## Validation Rules
- `repo` must be a valid GitHub repository name.
- `sub_path` must exist in the repository after cloning.
- If multiple skills exist in the sub-path, the closest one (highest metadata file) is chosen.