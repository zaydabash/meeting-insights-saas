from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router
from app.api.websocket import router as websocket_router

app = FastAPI(
    title="Meeting Insights API",
    description="B2B Meeting Insights SaaS API",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/api")


@app.get("/healthz")
async def health_check():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    # Prometheus metrics endpoint (stub)
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)

