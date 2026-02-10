# Research: GitHub Direct Skill Folder Input

## Decision: Parsing Strategy for GitHub Deep Links
**Rationale**: 
- GitHub URLs use a standard structure: `https://github.com/{owner}/{repo}/(tree|blob)/{branch}/{path}`.
- `tree` links indicate a directory, while `blob` links indicate a specific file.
- If a user pastes a `blob` link (e.g., to `SKILL.md`), the system should extract the parent folder path to treat it as the skill directory.

**Implementation**: 
- Use a regular expression to extract: `owner`, `repo`, `ref` (branch), and `path`.
- If the URL contains `blob`, use `Path(path).parent` as the actual skill sub-path.

## Decision: Direct Registration Flow Integration
**Rationale**: 
- Currently, the dashboard flow is `Input URL -> Search -> List -> Select -> Scan`.
- For deep links, we can streamline this to `Input URL -> Parse -> Scan`.
- The frontend will call a new validation endpoint or simply pass the URL to the registration batch endpoint which will handle the logic internally.

**Alternatives Considered**:
- **Frontend parsing**: Rejected because URL logic belongs in the backend for consistency and security validation.

## Best Practices for `gitpython` Sub-path Cloning
- Since we only need a specific folder, we still have to clone the repo.
- Optimization: Use `git clone --depth 1 --filter=blob:none --no-checkout` followed by a sparse checkout if the repo is large. 
- Decision: For the prototype, standard `clone --depth 1` is sufficient as most skill repos are small.