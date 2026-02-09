# app/core/database.py

import logging
from typing import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    create_async_engine, 
    async_sessionmaker
)
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings

logger = logging.getLogger(__name__)

# ==============================================
# CONFIGURAÇÃO DOS ENGINES
# ==============================================

def create_database_engines():
    """Cria os engines de banco de dados com configuração apropriada"""
    
    # Configuração do pool baseada no ambiente
    if settings.ENVIRONMENT == "production":
        pool_config = {
            "pool_size": 20,
            "max_overflow": 30,
            "pool_pre_ping": True,
            "pool_recycle": 3600,  # Reciclar conexões a cada hora
        }
    else:
        pool_config = {
            "pool_size": 5,
            "max_overflow": 10,
            "pool_pre_ping": True,
            "pool_recycle": 3600,
        }
    
    try:
        # Engine assíncrono para FastAPI
        async_engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            **pool_config,
            connect_args={
                "server_settings": {
                    "jit": "off",  # Desabilita JIT para melhor performance
                }
            }
        )
        
        # Engine síncrono para Alembic e operações sync
        sync_engine = create_engine(
            settings.SYNC_DATABASE_URL,
            echo=settings.DEBUG,
            **pool_config,
        )
        
        logger.info("✅ Engines de banco de dados criados com sucesso")
        return async_engine, sync_engine
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar engines de banco: {e}")
        raise


# Criar engines
async_engine, sync_engine = create_database_engines()

# ==============================================
# CONFIGURAÇÃO DAS SESSÕES
# ==============================================

# Session factory síncrona para operações em background
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
)

# Session factory assíncrona para FastAPI (usando async_sessionmaker)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base para modelos SQLAlchemy
Base = declarative_base()

# ==============================================
# DEPENDENCIAS (Dependency Injection)
# ==============================================

@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para obter sessão assíncrona do banco
    
    Uso:
        async with get_async_session() as session:
            result = await session.execute(query)
            # Não faz commit automático, o chamador controla
    """
    session = AsyncSessionLocal()
    try:
        logger.debug("📦 Sessão assíncrona aberta")
        yield session
        # Não faz commit automático! O chamador deve fazer
    except SQLAlchemyError as e:
        logger.error(f"❌ Erro na sessão do banco: {e}")
        await session.rollback()
        raise
    finally:
        logger.debug("📦 Fechando sessão assíncrona")
        await session.close()


@contextmanager
def get_sync_session() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão síncrona do banco
    
    Uso:
        with get_sync_session() as session:
            result = session.execute(query)
            session.commit()  # Chamador controla o commit
    """
    session = SyncSessionLocal()
    try:
        logger.debug("📦 Sessão síncrona aberta")
        yield session
        # Não faz commit automático!
    except SQLAlchemyError as e:
        logger.error(f"❌ Erro na sessão síncrona do banco: {e}")
        session.rollback()
        raise
    finally:
        logger.debug("📦 Fechando sessão síncrona")
        session.close()


# ==============================================
# FUNÇÕES ÚTEIS
# ==============================================

async def check_database_connection() -> bool:
    """Verifica se a conexão com o banco está funcionando"""
    try:
        async with get_async_session() as session:
            await session.execute("SELECT 1")
        logger.info("✅ Conexão com banco de dados está OK")
        return True
    except Exception as e:
        logger.error(f"❌ Falha na conexão com banco: {e}")
        return False


async def init_database():
    """Inicializa o banco de dados (cria tabelas se não existirem)"""
    try:
        # Para async, precisamos criar as tabelas usando sync engine
        # porque create_all() não é async nativo no SQLAlchemy 2.0
        with sync_engine.begin() as conn:
            Base.metadata.create_all(conn)
        
        logger.info("✅ Tabelas do banco de dados verificadas/criadas")
        
        # Testa a conexão
        if await check_database_connection():
            return True
        return False
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco: {e}")
        raise


async def close_database_connections():
    """Fecha todas as conexões com o banco (para shutdown)"""
    try:
        await async_engine.dispose()
        sync_engine.dispose()
        logger.info("✅ Conexões com banco fechadas")
    except Exception as e:
        logger.error(f"❌ Erro ao fechar conexões: {e}")


# ==============================================
# MÉTODOS DE CONEXÃO ALTERNATIVOS (para diferentes casos de uso)
# ==============================================

async def get_db():
    """
    Dependency para FastAPI endpoints (padrão FastAPI)
    
    Uso em endpoints:
        @router.get("/")
        async def read_items(db: AsyncSession = Depends(get_db)):
    """
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


def get_sync_db():
    """
    Dependency para operações síncronas
    
    Uso em tarefas em background:
        with get_sync_db() as db:
            db.add(object)
            db.commit()
    """
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()


# ==============================================
# ATALHOS PARA IMPORT
# ==============================================

# Exporta engines (mantém compatibilidade)
engine = async_engine