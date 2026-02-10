# Research: View Skill Popup and Style Fixes

## Decision: Use MUI Dialog for Documentation Popup
**Rationale**: 
- The project already uses Material UI (`@mui/material`), as seen in `SkillCard.tsx`.
- `MUI Dialog` (Modal) provides built-in support for:
    - Layered popup (z-index management).
    - Centered positioning.
    - Backdrop/overlay management.
    - Keyboard (ESC) and backdrop click closing.
    - Accessibility (ARIA roles).
- This aligns with **FR-002**, **User Story 2**, and **Core Principle II** (Material Design).

**Alternatives Considered**:
- `HTML <dialog>` element: Rejected because MUI components provide a more consistent theme integration and cross-browser stability within the existing codebase.
- Custom absolute-positioned `Box`: Rejected as it requires manual implementation of z-index, focus trapping, and backdrop logic.

## Decision: CSS Class for Contrast Correction
**Rationale**: 
- **FR-004** requires fixing the same-color text issue.
- Since we use `@tailwindcss/typography` (the `prose` class), the issue likely stems from dark mode configuration or conflicting global styles.
- **Decision**: Explicitly apply `text-slate-900` (light) and `dark:text-slate-100` (dark) or use the specific MUI `Typography` color properties within the dialog to override any inheriting styles that cause low contrast.
- Using `prose-slate` or `prose-gray` with `dark:prose-invert` is the standard Tailwind way to handle this.

## Decision: Modal Responsiveness
**Rationale**: 
- **SC-003** requires responsiveness from 375px to 1920px.
- `MUI Dialog` with `fullWidth` and `maxWidth="md"` or `"lg"` handles this naturally. We will set `scroll="paper"` to ensure the content area scrolls while the header/footer stay fixed (satisfying **FR-005**).
