from fastapi import FastAPI
from .api.routers import router as api_router
import os

app = FastAPI(title="Scientific Conferences API")

app.include_router(api_router)


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "env": os.getenv("DATABASE_URL", "not-set")}
