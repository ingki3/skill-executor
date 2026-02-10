# Research: Skill Risk Review

## Decision: JSON-based Batch Storage for Queue Persistence
**Rationale**: 
- Clarification Q1 requires the registration queue to be persistent across restarts. 
- A JSON file in `.pending_registrations/registry.json` is consistent with the current `SkillRegistry` implementation and provides simple, human-readable persistence without requiring a database.
- Each batch will be an entry in this registry with its associated items and scan results.

**Alternatives Considered**:
- **SQlite**: Rejected as overkill for the current scale of local administration.
- **Individual files per batch**: Rejected to keep state synchronization simpler within a single service.

## Decision: Integrated Risk Findings in Security Service
**Rationale**: 
- `SecurityService.analyze_risk` already returns a dict with risks. 
- The plan will formalize this into a `RiskFinding` model to ensure the UI can consistently render categories (PII, Malicious Code, etc.) and specific code snippets.

## Decision: Sidebar Drawer for Code Review
**Rationale**: 
- Reviewing code while looking at findings is best handled by a side-panel (Drawer) in the UI to maintain context of the batch list.
- Use `react-syntax-highlighter` for the code preview.

## Best Practices for Frontend Polling
**Rationale**: 
- Since scans are async, the frontend will poll `GET /api/skills/registration-batches/{id}` every 2 seconds until the batch status is `REVIEW_REQUIRED`.