# app/core/__init__.py
from .config import settings
from .database import (
    Base,
    get_db,
    get_sync_db,
    async_engine,
    sync_engine,
    engine,
    AsyncSessionLocal,
    SyncSessionLocal,
    SessionLocal,  # alias para compatibilidade
)
from .security import APISecurity

__all__ = [
    "settings",
    "Base",
    "get_db",
    "get_sync_db",
    "async_engine",
    "sync_engine",
    "engine",
    "AsyncSessionLocal",
    "SyncSessionLocal",
    "SessionLocal",
    "APISecurity",
]