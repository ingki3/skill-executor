# Quickstart: Skill Executor Agent

## Prerequisites
- Docker & Docker Compose
- Google AI API Key (for Gemini models)

## Setup
1. Clone this repository.
2. Create a `.env` file in the root:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   REGISTRY_PATH=./.skills
   MIN_CONFIDENCE_THRESHOLD=0.5
   ```
3. Build and start:
   ```bash
   docker-compose up --build
   ```

## Verification Scenarios

### Scenario 1: Manual Sync
```bash
# After skill registration
curl -X POST "http://localhost:8000/skills/{skill_id}/sync"
```
*Expected*: Status 200, system re-clones and re-scans the skill.

### Scenario 2: No Match Found (Low Confidence)
```bash
curl -X POST http://localhost:8000/skills/execute \
     -H "Content-Type: application/json" \
     -d '{"query": "something completely unrelated"}'
```
*Expected*: Status 404, message "No matching skill found".

### Scenario 3: LLM Security Rejection
*Expected*: Registration of a skill with suspicious prompt injection code is blocked with 403.