# Feature Specification: View Skill Popup and Style Fixes

**Feature Branch**: `007-view-skill-popup`  
**Created**: 2026-02-08  
**Status**: Draft  
**Input**: User description: "view docs 메뉴 이름을 view skill 로 바꿔줘. 그리고, 해당 버튼을 클릭하면 layed popup 으로 띄워줘. 그리고, 지금 글씨와 배경 색이 같아서 글자가 보이지 않아. 수정해줘."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Skill Documentation in Popup (Priority: P1)

As an administrator, I want to view skill documentation in a dedicated popup so that I can focus on the details without losing my place in the skill list.

**Why this priority**: Core functionality upgrade from expanding card to a more focused modal interface.

**Independent Test**: Click the "View Skill" button and verify a modal opens with the documentation content.

**Acceptance Scenarios**:

1. **Given** the skill management dashboard, **When** I locate a skill card, **Then** I should see a button labeled "View Skill" instead of "View Docs".
2. **Given** I click the "View Skill" button, **When** the documentation is fetched, **Then** it should appear in a centered layered popup (modal) overlaying the dashboard.
3. **Given** the documentation popup is open, **When** I look at the text, **Then** it must be clearly visible and readable (fix for same-color text/background issue).

---

### User Story 2 - Documentation Popup Navigation (Priority: P2)

As an administrator, I want to easily close the documentation popup so that I can quickly return to the skill management view.

**Why this priority**: Essential for a smooth user experience and efficient workflow.

**Independent Test**: Open the popup and close it using multiple methods (close button, overlay click, ESC key).

**Acceptance Scenarios**:

1. **Given** the documentation popup is open, **When** I click a "Close" button or an "X" icon, **Then** the popup should disappear.
2. **Given** the documentation popup is open, **When** I click outside the popup area (on the overlay), **Then** the popup should close.
3. **Given** the documentation popup is open, **When** I press the ESC key, **Then** the popup should close.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The "View Docs" button on the Skill Card MUST be renamed to "View Skill".
- **FR-002**: Documentation content MUST be displayed in a modal/popup dialog instead of the current `Collapse` component.
- **FR-003**: The modal MUST support markdown rendering (preserving existing `react-markdown` and `rehype-sanitize` integration).
- **FR-004**: The documentation text color MUST be adjusted to ensure high contrast against the modal background in both light and dark themes.
- **FR-005**: The modal MUST include a scrollable area for long documentation content, with a maximum height of 80% of the viewport.
- **FR-006**: The system MUST show a loading indicator within the modal if documentation fetching is in progress.

### Key Entities *(include if feature involves data)*

- **SkillDocumentation**: Human-readable documentation content fetched from the backend.
- **SkillCard**: The UI component hosting the "View Skill" trigger.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Documentation popup renders and displays content (or loading state) in under 100ms from the user click event.
- **SC-002**: 100% of documentation text meets WCAG 2.1 AA contrast standards (minimum 4.5:1 for normal text) in both light and dark themes, verified via automated accessibility auditing tools.
- **SC-003**: The popup is responsive and usable on screen widths from 375px to 1920px.
- **SC-004**: Documentation section is removed from the inline `SkillCard` view, reducing the default card height.