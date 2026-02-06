# Product Requirements Document: Skill Executor Agent

## 1. Introduction
This project aims to build an **Agentic Skill Executor** application. The system allows users to register "skills" (defined by prompts and code) to a local environment, inspect them, and execute them intelligently based on complexity. It mimics the capability of agents like Claude Code or Cursor but allows for a custom, self-hosted skill registry and execution engine.

## 2. Core Objectives
- **Secure Skill Registration**: Register skills from external sources (GitHub) while filtering out security risks.
- **Adaptive Execution**: Choose the most efficient LLM (Lightweight vs. Advanced) and strategy (Direct vs. ReACT) based on the skill's defined complexity.
- **Management & Visibility**: Provide a clear Admin UI to manage, test, and view registered skills.

## 3. Product Features

### 3.1 Skill Registration System
- **Register via URL**: Users can input a GitHub repository URL to register a skill.
- **Directory Structure**:
    - Skills are stored locally in a `.skills/` directory.
    - Each skill has its own subdirectory: `.skills/<skill_name>/`.
- **Security & Validation**:
    - **Risk Analysis**: Before registration, the system scans prompts and code for:
        - Personal Information (PII) theft risks.
        - Malicious code execution risks.
        - Dangerous system operations.
    - **Rejection**: If high risk is detected, registration is blocked.
- **Metadata Definition**:
    - Skills must include a `yaml` metadata file.
    - **Differentiation**: Metadata flags the skill as "Simple" or "Complex".
        - **Simple**: Low complexity prompts, direct code execution -> Maps to **Lightweight LLM**.
        - **Complex**: Complex reasoning required, multi-step actions -> Maps to **Advanced LLM**.
- **Batch Registration API**:
    - Endpoint to scan a specific folder in a Git repository and register multiple skills found within it simultaneously.

### 3.2 Skill Execution Engine
- **Skill Discovery**:
    - Skill metadata is indexed in a **Vector Database (FAISS)**.
    - User queries are vectorized to search for the most relevant skill.
- **Execution Workflow**:
    1.  **Search**: Identify target skill via FAISS.
    2.  **Routing**:
        - If `Simple`: Execute using a fast, cost-effective model (e.g., Gemini Flash, GPT-4o-mini).
        - If `Complex`: Execute using a high-reasoning model (e.g., Gemini Pro/Ultra, GPT-4o, Claude 3.5 Sonnet) using a **ReACT** (Reasoning + Acting) loop.
    3.  **Code Execution**: Safely execute code blocks associated with the skill if applicable.

### 3.3 Admin Dashboard (UI)
- **Skill Management**:
    - Register new skills (Single URL or Batch Folder).
    - View list of all registered skills.
    - View details of individual skills (prompts, code, metadata).
    - Delete skills.
    - **Version Control**: Manage skill versions via a local JSON registry file.
- **Testing & Monitoring**:
    - **Health Check**: Display API server status.
    - **Test Runner**: Interface to run a test execution of a skill and display Success/Failure status.

## 4. Technical Architecture
- **Server**: Python (FastAPI or Flask recommended for AI/Vector operations).
- **Client**: Node.js with React.
- **Database**: 
    - **Vector Store**: FAISS (for skill semantic search).
    - **Registry**: JSON/YAML based local file system storage.
- **Model Integration**: Support for configurable LLM endpoints (Simple vs. Avanced tiers).