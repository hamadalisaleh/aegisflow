from fastapi import FastAPI

app = FastAPI(
    title="AegisFlow API",
    description="Control plane for reliable AI agent execution",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "aegisflow"
    }
