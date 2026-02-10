# Data Model: Unified Image and Skill Registry (Updated)

## Entities

### Unified Docker Image
- **UI Port**: Exposed port for the React application (e.g., 3000).
- **API Port**: Exposed port for the FastAPI backend (e.g., 8000).
- **Base Image**: Python 3.12-slim.

### Skill Registry (Persistent)
- **Location**: \`.skills/\` directory (mounted via Docker Volume).
- **Metadata**: JSON/YAML files containing skill definitions.
- **Source**: GitHub repository URL and specific sub-path.

### External Skill Repository
- **URL**: \`https://github.com/ComposioHQ/awesome-claude-skills\`.
- **Tree**: Fetched dynamically via GitHub API for selection.

## Validation Rules
- Selected skills must have a recognized entry point.
- Volume mounts must be writable by the container user.