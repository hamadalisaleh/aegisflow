from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI(
    title="AegisFlow API",
    description="Control plane for reliable AI agent execution",
    version="0.1.0"
)

app.include_router(auth_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "aegisflow"
    }
