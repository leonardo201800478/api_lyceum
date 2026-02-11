# app/api/v1/endpoints/__init__.py
from .alunos import router as alunos_router
from .health import router as health_router
from .sync import router as sync_router
from .security import router as security_router

__all__ = [
    "alunos_router",
    "health_router",
    "sync_router",
    "security_router",
]