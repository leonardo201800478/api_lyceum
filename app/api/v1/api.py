from fastapi import APIRouter
from app.api.v1.endpoints import alunos, health, sync, security

api_router = APIRouter()

api_router.include_router(alunos.router, prefix="/alunos", tags=["alunos"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])
api_router.include_router(security.router, prefix="/security", tags=["security"])