# Quickstart: Unified Docker Image (Updated)

## Building the Image
From the project root:

```bash
docker build -t skill-executor-unified .
```

## Running with Volumes
Ensure you mount the persistent directories:

```bash
docker run -p 3000:3000 -p 8000:8000 \
  -v $(pwd)/.skills:/app/.skills \
  -v $(pwd)/.skill-executor-data:/app/.skill-executor-data \
  -e GEMINI_API_KEY=your_key \
  skill-executor-unified
```

## Using the UI for Registration
1. Access \`http://localhost:3000\`.
2. Enter the repository URL.
3. Select 3-4 skills from the list.
4. Confirm registration.
5. Verify skills are listed and can be executed.