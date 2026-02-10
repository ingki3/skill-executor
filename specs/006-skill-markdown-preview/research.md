# Research: Skill Markdown Preview

## Decision: Use `react-markdown` with `rehype-sanitize`
**Rationale**: 
- `react-markdown` is the industry standard for React applications. It converts markdown into React components rather than using `dangerouslySetInnerHTML`.
- `rehype-sanitize` provides robust protection against XSS by white-listing allowed tags and attributes.
- It integrates well with Tailwind CSS via the `prose` class from `@tailwindcss/typography`.

**Alternatives Considered**:
- `markdown-it`: Rejected because it requires `dangerouslySetInnerHTML` or extra wrappers for React integration.

## Decision: Backend File Retrieval via `RegistryService`
**Rationale**: 
- The `RegistryService` already knows the base directory for skills (`.skills/`).
- We can implement a method that securely resolves the path to `skill.md` or `SKILL.md` within a specific skill's UUID-named folder.
- This avoids exposing arbitrary filesystem paths to the API.

## Handling Relative Links and Images
**Rationale**: 
- Many skills may contain relative links to other files or images.
- **Initial Scope**: Relative links will be rendered as-is (they may break if they point to local files not served by the API).
- **Future Enhancement**: Rewrite relative links to point back to the GitHub source or a local file server.

## Best Practices for File Reading in FastAPI
- Use `aiofiles` or standard `open` within a thread-pool for async-friendly file I/O.
- Ensure proper error handling for `FileNotFoundError` and permission issues.
