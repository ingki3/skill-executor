FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory.
WORKDIR /app

# Install system dependencies.
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*


# Install dependencies.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Copy the application code.
COPY src ./src
COPY README.md ./

# Expose the application port.
EXPOSE 8000

# Run the application.
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
