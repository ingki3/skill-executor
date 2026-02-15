from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Skill Executor Agent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.on_event("startup")
async def startup_event():
    from src.services.session_registry import session_registry
    import asyncio
    asyncio.create_task(session_registry.start_cleanup_task())

from src.api.registration_router import router as registration_router
from src.api.execution_router import router as execution_router
from src.api.tools import router as tools_router
app.include_router(registration_router)
app.include_router(execution_router)
app.include_router(tools_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
