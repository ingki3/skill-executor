# Research: Local Skill Registration

## Decision: Path Normalization and Boundary Validation
**Rationale**: 
- Clarification Q1 requires restricting searches to the project root.
- The `LocalFSService` will use `os.path.abspath` and `os.path.commonpath` to ensure that the user-provided path is a child of the application root.
- This prevents "directory traversal" attacks (e.g., inputting `../../etc`).

## Decision: Unified Registration API for Local Paths
**Rationale**: 
- The existing `/api/skills/register-batch` and `/api/skills/registration-batches/{id}/judge` endpoints can be extended.
- For local paths, the "repo_url" field will accept an absolute file path.
- The `RegistrationService` will detect the path type and skip the `git clone` step for local paths, instead copying directly from the source directory.

## Decision: Metadata Discovery in Local Subdirectories
**Rationale**: 
- When a local base path is searched, the system will look for `skill.yaml` or `SKILL.md` in every immediate subdirectory.
- This information will be returned to the UI to help the user identify valid skill folders before initiating a scan.

## Best Practices for File System Operations
- Use `pathlib` for modern, safe path manipulations.
- Implement error handling for `PermissionError` and `FileNotFoundError`.
- Ensure that the container user has read permissions for any directories intended for registration.