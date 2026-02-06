from .alunos import router as alunos_router
from .health import router as health_router
from .sync import router as sync_router

__all__ = ["alunos_router", "health_router", "sync_router"]