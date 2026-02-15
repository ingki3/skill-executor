# Stage 1: Build Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend Runtime
FROM python:3.12-slim AS backend-runtime
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy backend dependencies first for caching
COPY backend/pyproject.toml backend/uv.lock* /app/backend/
WORKDIR /app/backend
RUN uv sync --frozen --no-install-project

# Copy backend source
COPY backend/ /app/backend
RUN uv sync --frozen

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist
COPY frontend/package*.json /app/frontend/
COPY frontend/vite.config.ts /app/frontend/
WORKDIR /app/frontend
RUN npm install -g serve

# Entrypoint script
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/entrypoint.sh
WORKDIR /app
CMD ["./scripts/entrypoint.sh"]