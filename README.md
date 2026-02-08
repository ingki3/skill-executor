# Skill Executor Agent

A unified agent for registering and executing AI skills from community repositories.

## Quick Start (Unified Docker)

Build the unified image (contains both frontend and backend):

```bash
docker build -t skill-executor .
```

Run with persistent volumes:

```bash
docker run -p 3000:3000 -p 8000:8000 \
  -v $(pwd)/.skills:/app/backend/.skills \
  -v $(pwd)/.skill-executor-data:/app/backend/.skill-executor-data \
  -e GOOGLE_API_KEY=your_api_key \
  skill-executor
```

Access the dashboard at `http://localhost:3000`.

## Features

- **Unified Image**: Frontend and Backend served from a single container.
- **Bulk Registration**: Search and select multiple skills from GitHub repositories.
- **Persistent Storage**: Skills and registry data are persisted across container restarts.
- **Security Scan**: Automated risk analysis for all registered skills.

## Community Skills

You can register skills from [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) by entering the URL in the dashboard and selecting the desired tools.
