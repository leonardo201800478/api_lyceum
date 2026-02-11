# app/core/database.py
import logging
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

# -------------------------
# SYNC ENGINE (Alembic, scripts)
# -------------------------
@lru_cache
def get_sync_engine():
    logger.info("Criando sync engine...")
    return create_engine(
        settings.SYNC_DATABASE_URL,
        pool_pre_ping=True,
        echo=settings.DEBUG,
    )

sync_engine = get_sync_engine()

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)

# --- ALIAS PARA COMPATIBILIDADE COM CÓDIGO LEGADO ---
SessionLocal = SyncSessionLocal   # ← ADICIONE ESTA LINHA
# ----------------------------------------------------

def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# ASYNC ENGINE (API FastAPI)
# -------------------------
@lru_cache
def get_async_engine():
    logger.info("Criando async engine...")
    return create_async_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=settings.DEBUG,
    )

async_engine = get_async_engine()

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Aliases para compatibilidade
engine = sync_engine
get_db = get_async_db