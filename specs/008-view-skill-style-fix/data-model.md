# Data Model: View Skill Style and Layout Fix

*This feature is purely UI-based and does not introduce new backend entities or modify existing database schemas.*

## UI State (SkillCard.tsx)

- **Skill Name**: Displayed as `DialogTitle`.
- **Skill Description**: Displayed at the top of `DialogContent`, before the markdown documentation.
- **Documentation Content**: Fetched from existing endpoint and rendered via `ReactMarkdown`.