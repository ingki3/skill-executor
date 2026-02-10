# Feature Specification: Unified Docker Image and Skill Testing

**Feature Branch**: `002-unified-docker-image`  
**Created**: 2026-02-07  
**Status**: Draft  
**Input**: User description: "docker 이미지를 하나로 빌드해서 실행하도록 해줘. 하나의 이미지에 front와 backend 가 함께 빌드되도록 수정해줘. 변경 후 테스트  진행해줘. 테스트는 https://github.com/ComposioHQ/awesome-claude-skills 의 스킬 가운데 3~4개를 등록해 보고 제대로 동작하는지 테스트해줘."

## Clarifications

### Session 2026-02-07

- Q: Networking Strategy → A: Multiple ports (separate ports for UI and API)
- Q: Skill Selection Method → A: UI-based selection (fetch list, user selects)
- Q: Skill Execution Environment → A: Same container (skills run in the unified container)
- Q: Frontend-Backend Communication → A: Static config (UI points to API port via config)
- Q: Data Persistence Strategy → A: Docker Volumes (persist registry and skills across cycles)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Single Image Deployment (Priority: P1)

As a developer or operator, I want to build and run the entire Skill Executor application using a single Docker image so that deployment and local setup are simplified.

**Why this priority**: Core requirement to unify the architecture and simplify the distribution of the application.

**Independent Test**: Build the unified image and run it. Verify that both the User Interface and the Core API are accessible on their respective ports.

**Acceptance Scenarios**:

1. **Given** a single build configuration, **When** I build the image, **Then** a single artifact is created containing both User Interface and Core API components.
2. **Given** the unified image, **When** I execute it, **Then** the application starts and the User Interface is accessible via its designated port.


---

### User Story 2 - Bulk Skill Registration (Priority: P1)

As a user, I want to register multiple skills from the "awesome-claude-skills" repository so that I can quickly expand the capabilities of my agent.

**Why this priority**: Necessary to verify that the registration service works correctly with external community-provided skills as requested.

**Independent Test**: Provide the repository URL to the registration service, select 3-4 skills from the generated list, and verify they are successfully added to the local registry.

**Acceptance Scenarios**:

1. **Given** the repository URL `https://github.com/ComposioHQ/awesome-claude-skills`, **When** the system lists available skills and I select 3-4 for registration, **Then** those skills appear in the "Registered Skills" list.

---

### User Story 3 - Verified Skill Execution (Priority: P2)

As a user, I want to execute the newly registered skills to ensure they are fully functional within the unified container environment.

**Why this priority**: Ensures that the unification of the image hasn't introduced networking or environment issues that prevent skills from running.

**Independent Test**: Trigger an execution request for each of the 3-4 registered skills and verify a successful response.

**Acceptance Scenarios**:

1. **Given** 3-4 registered skills, **When** I trigger an execution for each, **Then** I receive a valid response from the skill service for all of them.

---

### Edge Cases

- **Service Connectivity**: How do internal components communicate if they are bundled in the same image? (Resolution: UI is configured via environment variables or static config to point to the backend's exposed API port).
- **Environment Configuration**: How are sensitive configurations managed in a unified image?
- **Large Skill Repositories**: What happens if the registration process takes too long?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a unified build configuration that produces a single image for both User Interface and Core API.
- **FR-002**: The unified image MUST serve both components simultaneously, exposing separate network ports for the User Interface and the Core API.
- **FR-003**: System MUST support registering skills directly from provided repository links.
- **FR-004**: System MUST fetch and display available skills from a repository link to allow user selection before registration.
- **FR-005**: System MUST allow selecting multiple specific skills from a repository for registration.
- **FR-006**: System MUST persist the registered skills and registry data using persistent storage (e.g., Docker volumes) and execute them directly within the unified environment.
- **FR-007**: System MUST provide a way to verify the execution status of registered skills.

### Key Entities

- **Unified Image**: The single deployable artifact containing all application components.
- **External Skill**: A skill definition sourced from a remote repository.
- **Registry**: The local storage within the application where skill definitions are cached and managed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Deployment is simplified to a single execution command instead of managing multiple distinct services.
- **SC-002**: Successfully register at least 4 distinct skills from the specified repository.
- **SC-003**: 100% of the 4 test skills successfully complete a basic execution check.
- **SC-004**: System initialization time is under 15 seconds.