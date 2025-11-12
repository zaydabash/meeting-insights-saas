from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1 import meetings, nlp, tasks, integrations, admin

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
api_router.include_router(nlp.router, prefix="/nlp", tags=["nlp"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

