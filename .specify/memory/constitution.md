<!--
Sync Impact Report:
- Version change: [CONSTITUTION_VERSION] → 1.0.0
- Modified principles:
    - [PRINCIPLE_1_NAME] → I. Modern Python Backend (uv + Python 3.12)
    - [PRINCIPLE_2_NAME] → II. React Frontend (Node.js + Tailwind CSS)
    - [PRINCIPLE_3_NAME] → III. Dockerized Testing & Deployment
    - [PRINCIPLE_4_NAME] → IV. Secure Skill Registration
    - [PRINCIPLE_5_NAME] → V. Adaptive Execution & Observability
- Added sections: Technology Stack, Development Workflow
- Removed sections: N/A
- Templates requiring updates:
    - .specify/templates/plan-template.md (✅ updated)
    - .specify/templates/tasks-template.md (✅ updated)
- Follow-up TODOs: None
-->

# Skill Executor Agent Constitution

## Core Principles

### I. Modern Python Backend
The backend MUST use Python 3.12. All package management, dependency resolution, and environment isolation MUST be handled by `uv`. No other environment managers (e.g., conda, poetry) are permitted.

### II. React Frontend
The frontend MUST be built using Node.js, React, and Tailwind CSS. Modern UI/UX principles, specifically Material Design, SHOULD be followed to ensure a professional and functional admin interface.

### III. Dockerized Testing & Deployment (NON-NEGOTIABLE)
All development, testing, and production environments MUST be defined via Docker. Every implementation MUST be validated within a Docker container to ensure environment parity and reproducible test results.

### IV. Secure Skill Registration
Security is the primary constraint. Every skill registration MUST undergo an automated risk analysis (scanning for PII theft, malicious code, and dangerous system operations) before being accepted into the registry.

### V. Adaptive Execution & Observability
The system MUST intelligently route execution requests between Lightweight (e.g., Gemini Flash) and Advanced (e.g., Gemini Pro) LLMs based on skill metadata. Full traceability of the execution loop (especially for ReACT patterns) is mandatory for observability.

## Technology Stack

### Backend
- **Language**: Python 3.12
- **Manager**: `uv`
- **Framework**: FastAPI (preferred for async AI operations)
- **Vector DB**: FAISS

### Frontend
- **Runtime**: Node.js
- **Framework**: React (with TypeScript)
- **Styling**: Tailwind CSS
- **Package Manager**: npm

## Development Workflow

### Testing Discipline
1. **Docker-First**: All tests must be runnable inside a Docker image.
2. **Contract Testing**: Any changes to the API contracts between frontend and backend must be verified via contract tests.
3. **Security Scans**: Registration logic MUST include security check unit tests.

## Governance
- This constitution supersedes all other development practices in the Skill Executor Agent project.
- Amendments require a version bump (Semantic Versioning) and a Sync Impact Report.
- All Pull Requests must be verified against these principles.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06