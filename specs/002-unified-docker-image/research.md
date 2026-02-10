# Research: Unified Docker Image and Skill Selection (Updated)

## Decision: Multi-port Exposure in Single Docker Container
**Rationale**:
- User requested separate ports for UI and API within a single image.
- This can be achieved by exposing multiple ports in the Dockerfile and running both services (e.g., using a process manager like \`supervisord\` or a simple shell script entrypoint).
- **Alternative**: Serving UI from FastAPI. Rejected because the user clarified the need for separate ports.

## Decision: GitHub Repository Listing for Skill Selection
**Rationale**:
- To allow user selection, the backend must fetch the repository structure.
- Use the GitHub API (\`/repos/{owner}/{repo}/contents/{path}\`) to list subdirectories in the \`awesome-claude-skills\` repository.
- The UI will present this list for the user to select 3-4 items.

## Decision: Persistent Storage via Docker Volumes
**Rationale**:
- Docker volumes are the standard way to persist data across container life cycles.
- The \`.skills/\` and \`.skill-executor-data/\` directories will be mounted as volumes.

## Technology Choices
- **Process Management**: Shell script entrypoint (lightweight) or \`supervisord\`.
- **API Client**: \`httpx\` for fetching GitHub repository contents.
- **Frontend Config**: Build-time environment variables (\`VITE_API_URL\`) or runtime config fetch.