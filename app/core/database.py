# app/core/database.py - VERSÃO COMPLETA E CORRIGIDA
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import logging

from app.core.config import settings

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URLs de conexão
SYNC_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

logger.info(f"Conectando ao banco: {settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")

# Engine síncrono
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

# Engine assíncrono
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
    pool_pre_ping=True
)

# Session factories
SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base para modelos
Base = declarative_base()

# Função para obter sessão assíncrona
async def get_db():
    """Obtém sessão assíncrona para injeção de dependência"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Função para obter sessão síncrona (se necessário)
def get_sync_db():
    """Obtém sessão síncrona para operações síncronas"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Aliases para compatibilidade
engine = async_engine  # Para códigos que ainda usam 'engine'

logger.info("✅ Engines de banco criados com sucesso!")