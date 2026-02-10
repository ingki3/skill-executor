# Research: View Skill Style and Layout Fix

## Decision: Theme-Aware Text Color
**Rationale**: 
- The user requested "black text", but clarified during `/speckit.clarify` that it should be theme-aware (black in Light Mode, white in Dark Mode).
- Material UI (MUI) handles this automatically if we use the standard `Typography` components or appropriate color keys (`text.primary`).
- For the `prose` (Tailwind Typography) section, we will ensure `dark:prose-invert` is correctly applied to switch text colors based on the theme.

**Alternatives Considered**:
- Forcing black text (#000000) always: Rejected because it would be invisible in Dark Mode.

## Decision: Layout Spacing and Typography Hierarchy
**Rationale**:
- Use MUI's `Typography` with `variant="h6"` or `variant="subtitle1"` for the Title.
- Use MUI's `Typography` with `variant="body2"` and `color="text.secondary"` for the Skill Description.
- Apply a vertical margin (e.g., `mb: 2` in MUI or `mb-4` in Tailwind) between the title and description to satisfy the "line break" requirement.

**Alternatives Considered**:
- Using `<br />` tags: Rejected in favor of modern CSS spacing (margin/padding) for better consistency.