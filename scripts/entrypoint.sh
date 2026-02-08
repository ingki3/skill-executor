#!/bin/bash

# Start the backend
echo "[ENTRYPOINT] Starting backend..."
cd /app/backend
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start the frontend
echo "[ENTRYPOINT] Starting frontend..."
cd /app/frontend
serve -s dist -l 3000 &
FRONTEND_PID=$!

# Helper to kill both on exit
cleanup() {
    echo "[ENTRYPOINT] Stopping processes..."
    kill -TERM "$BACKEND_PID" 2>/dev/null
    kill -TERM "$FRONTEND_PID" 2>/dev/null
    wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
    exit 0
}

# Trap signals
trap cleanup SIGINT SIGTERM

echo "[ENTRYPOINT] Services started (Backend PID: $BACKEND_PID, Frontend PID: $FRONTEND_PID)"

# Monitoring loop
while true; do
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "[ENTRYPOINT] Backend process died. Exiting..."
        cleanup
    fi
    if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo "[ENTRYPOINT] Frontend process died. Exiting..."
        cleanup
    fi
    sleep 5
done
