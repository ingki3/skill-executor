# Product Requirements Document: Skill Executor Agent

## 1. Introduction
This project aims to build an **Agentic Skill Executor** application. The system allows users to register "skills" (defined by prompts and code) to a local environment, inspect them, and execute them intelligently based on complexity. It mimics the capability of agents like Claude Code or Cursor but allows for a custom, self-hosted skill registry and execution engine.

## 2. Core Objectives
- **Secure Skill Registration**: Register skills from external sources (GitHub) or local directories while filtering out security risks through LLM-based verification.
- **Adaptive Execution**: Choose the most efficient LLM (Lightweight vs. Advanced) and strategy (Direct vs. ReACT) based on the skill's defined complexity.
- **Management & Visibility**: Provide a clear Admin UI to manage, test, and view registered skills with comprehensive documentation preview.
- **Unified Deployment**: Provide a single Docker image containing both frontend and backend for simplified deployment.

## 3. Product Features

### 3.1 Skill Registration System
- **Register via URL**: Users can input a GitHub repository URL to register a skill.
  - Supports root repository URLs (triggers skill listing) and deep links to specific skill folders (triggers direct registration).
  - Deep link parsing supports `tree/{branch}/path` and `blob/{branch}/path` URL variants.
- **Register via Local Directory**: Users can search a local directory on the server and register skills from subdirectories.
  - Paths are restricted to the project root directory for security.
  - Prompts user for confirmation before overwriting existing skills.
- **Directory Structure**:
    - Skills are stored locally in a `.skills/` directory.
    - Each skill has its own subdirectory: `.skills/<skill_name>/`.
- **Metadata Definition**:
    - Skills must include a `skill.yaml` or `SKILL.md` metadata file.
    - **Differentiation**: Metadata flags the skill as "Simple" or "Complex".
        - **Simple**: Low complexity prompts, direct code execution -> Maps to **Lightweight LLM**.
        - **Complex**: Complex reasoning required, multi-step actions -> Maps to **Advanced LLM**.
- **Batch Registration API**:
    - Endpoint to scan a specific folder in a Git repository or local directory and register multiple skills found within it simultaneously.

### 3.2 Security & Risk Review
- **LLM-based Risk Analysis**: Before registration, the system scans prompts and code using LLM-based verification for:
    - Personal Information (PII) theft risks.
    - Malicious code execution risks.
    - Dangerous system operations.
- **Registration Queue**: Skills are placed in a "Pending" queue for user review.
    - Each skill displays a safety status (Safe/Risky) and detailed risk findings.
    - **Manual Judgment**: All skills (safe or risky) require explicit user approval to register.
    - Users can "Approve" or "Reject" individual skills.
    - "Register All Safe" bulk action for skills marked as safe.
- **Persistent Queue**: Registration queue state is persisted across application restarts.
- **Rejection/Blocking**: If rejected by user or high risk is detected without approval, registration is blocked.

### 3.3 Skill Execution Engine
- **Skill Discovery**:
    - Skill metadata is indexed in a **Vector Database (FAISS)**.
    - User queries are vectorized to search for the most relevant skill.
    - If no skill meets the minimum confidence threshold, respond with "No matching skill found".
- **Execution Workflow**:
    1.  **Search**: Identify target skill via FAISS.
    2.  **Routing**:
        - If `Simple`: Execute using a fast, cost-effective model (e.g., Gemini Flash, GPT-4o-mini).
        - If `Complex`: Execute using a high-reasoning model (e.g., Gemini Pro/Ultra, GPT-4o, Claude 3.5 Sonnet) using a **ReACT** (Reasoning + Acting) loop with a maximum of 10 steps.
    3.  **Code Execution**: Execute Python scripts and terminal commands bundled with the skill.
- **Code & Command Execution**:
    - Skills can include separate files for Python code (`*.py`) or shell scripts (`*.sh`).
    - **Python Execution**: Secure Python interpreter with sandboxing options (Docker, E2B).
    - **Terminal Commands**: Execute shell commands defined in skill configuration.
    - **CodeAgent Pattern**: LLM generates actions as Python code snippets (inspired by [smolagents](https://github.com/huggingface/smolagents)), enabling multi-tool calls in a single action.
- **Human-in-the-Loop (HITL) Options**:
    - Users can select execution mode when running a skill:
        - **HITL Enabled**: Agent can pause and ask clarifying questions to the user.
        - **HITL Disabled (Autonomous)**: Agent runs autonomously without human intervention.
    - **HITL Enabled Mode**:
        - **Session Management**: Maintain persistent session context during skill execution.
        - **Conversation Memory**: Use LangChain's memory modules (`ConversationBufferMemory`, `ConversationSummaryMemory`) to retain dialogue history.
        - **Interactive Loop**: Agent pauses for user input when clarification is needed, then resumes execution.
        - **Session Timeout**: Configurable session expiration (default: 30 minutes).
    - **HITL Disabled Mode (Autonomous)**:
        - Agent executes in a fully autonomous ReACT loop.
        - No human intervention; agent makes decisions independently.
        - Fallback strategies for ambiguous situations (retry with different approach, use default values, or fail gracefully).
        - Maximum iteration limit to prevent infinite loops.

### 3.4 Admin Dashboard (UI)
- **Skill Management**:
    - Register new skills (Single URL, Deep Link, Batch Folder, or Local Directory).
    - View list of all registered skills.
    - **View Skill Popup**: Click "View Skill" button to open a modal popup displaying:
        - Skill Name (Title)
        - Skill Description (with clear visual separation from title)
        - Rendered Markdown documentation (`skill.md` or `SKILL.md`)
    - Theme-aware styling: Black text in Light Mode, White text in Dark Mode for accessibility.
    - Delete skills.
    - **Sync Skills**: Manual "Sync" button to update skills from source repository.
    - **Version Control**: Manage skill versions via a local JSON registry file.
- **Registration Queue**:
    - View pending skills with safety status and risk details.
    - Approve/Reject individual skills.
    - Bulk approve all safe skills.
- **Testing & Monitoring**:
    - **Health Check**: Display API server status.
    - **Test Runner**: Interface to run a test execution of a skill and display Success/Failure status.

## 4. Technical Architecture
- **Deployment**: Unified Docker image containing both frontend and backend.
    - Multiple ports exposed (separate ports for UI and API).
    - Data persistence via Docker Volumes (registry and skills persist across container restarts).
- **Server**: Python 3.12 (FastAPI) managed by `uv`.
- **Client**: Node.js with React + Tailwind CSS.
- **Database**: 
    - **Vector Store**: FAISS (for skill semantic search).
    - **Registry**: JSON/YAML based local file system storage.
    - **Pending Registrations**: JSON-based persistence in `.pending_registrations/`.
    - **Session Store**: In-memory session storage with optional Redis for persistence.
- **Model Integration**: Support for configurable LLM endpoints (Simple vs. Advanced tiers).
- **Agent Framework**: 
    - **LangChain**: ReACT orchestration, conversation memory (`ConversationBufferMemory`, `ConversationSummaryMemory`).
    - **CodeAgent Pattern**: Inspired by [smolagents](https://github.com/huggingface/smolagents) for code-based action generation.
- **Code Execution Sandbox**:
    - Secure Python interpreter with restricted builtins.
    - Docker-based sandboxing for isolated execution.
    - Optional E2B integration for cloud-based sandboxing.
- **GitHub Integration**: `gitpython` for repository operations.
- **Markdown Rendering**: `react-markdown` with `rehype-sanitize` for frontend documentation display.