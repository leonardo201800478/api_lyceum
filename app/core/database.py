# app/core/database.py
import sys
import os

# CONFIGURAÇÃO DE ENCODING FORÇADA
os.environ["PYTHONUTF8"] = "1"
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf-8')

import logging
from typing import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import create_engine, text
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
# CONFIGURAÇÃO DOS ENGINES COM UTF-8
# ==============================================

def get_pool_config():
    """Retorna configuração do pool com encoding UTF-8"""
    return {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "connect_args": {
            "options": "-c client_encoding=utf8"
        }
    }

def create_database_engines():
    """Cria os engines de banco de dados com UTF-8"""
    
    pool_config = get_pool_config()
    
    try:
        # Engine assíncrono com UTF-8
        async_engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            **pool_config,
            connect_args={
                "server_settings": {
                    "client_encoding": "UTF8",
                    "TimeZone": "America/Sao_Paulo"
                }
            }
        )
        
        # Engine síncrono com UTF-8
        sync_engine = create_engine(
            settings.SYNC_DATABASE_URL,
            echo=settings.DEBUG,
            **pool_config,
            connect_args={
                "options": "-c client_encoding=utf8"
            }
        )
        
        logger.info("✅ Engines de banco criados (UTF-8)")
        return async_engine, sync_engine
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar engines: {e}")
        raise

# Criar engines
async_engine, sync_engine = create_database_engines()

# ... restante do código permanece igual ...

# ==============================================
# CONFIGURACAO DAS SESSOES
# ==============================================

# Session factory sincrona para operacoes em background
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
)

# Session factory assincrona para FastAPI (usando async_sessionmaker)
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
    Dependency para obter sessao assincrona do banco
    
    Uso:
        async with get_async_session() as session:
            result = await session.execute(query)
            # Nao faz commit automatico, o chamador controla
    """
    session = AsyncSessionLocal()
    try:
        logger.debug("📦 Sessao assincrona aberta")
        yield session
        # Nao faz commit automatico! O chamador deve fazer
    except SQLAlchemyError as e:
        logger.error(f"❌ Erro na sessao do banco: {e}")
        await session.rollback()
        raise
    finally:
        logger.debug("📦 Fechando sessao assincrona")
        await session.close()


@contextmanager
def get_sync_session() -> Generator[Session, None, None]:
    """
    Dependency para obter sessao sincrona do banco
    
    Uso:
        with get_sync_session() as session:
            result = session.execute(query)
            session.commit()  # Chamador controla o commit
    """
    session = SyncSessionLocal()
    try:
        logger.debug("📦 Sessao sincrona aberta")
        yield session
        # Nao faz commit automatico!
    except SQLAlchemyError as e:
        logger.error(f"❌ Erro na sessao sincrona do banco: {e}")
        session.rollback()
        raise
    finally:
        logger.debug("📦 Fechando sessao sincrona")
        session.close()


# ==============================================
# FUNCOES UTEIS
# ==============================================

async def check_database_connection() -> bool:
    """Verifica se a conexao com o banco esta funcionando"""
    try:
        async with get_async_session() as session:
            await session.execute("SELECT 1")
        logger.info("✅ Conexao com banco de dados esta OK")
        return True
    except Exception as e:
        logger.error(f"❌ Falha na conexao com banco: {e}")
        return False


async def init_database():
    """Inicializa o banco de dados (cria tabelas se nao existirem)"""
    try:
        # Para async, precisamos criar as tabelas usando sync engine
        # porque create_all() nao e async nativo no SQLAlchemy 2.0
        with sync_engine.begin() as conn:
            Base.metadata.create_all(conn)
        
        logger.info("✅ Tabelas do banco de dados verificadas/criadas")
        
        # Testa a conexao
        if await check_database_connection():
            return True
        return False
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco: {e}")
        raise


async def close_database_connections():
    """Fecha todas as conexoes com o banco (para shutdown)"""
    try:
        await async_engine.dispose()
        sync_engine.dispose()
        logger.info("✅ Conexoes com banco fechadas")
    except Exception as e:
        logger.error(f"❌ Erro ao fechar conexoes: {e}")


# ==============================================
# METODOS DE CONEXAO ALTERNATIVOS (para diferentes casos de uso)
# ==============================================

async def get_db():
    """
    Dependency para FastAPI endpoints (padrao FastAPI)
    
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
    Dependency para operacoes sincronas
    
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

# Exporta engines (mantem compatibilidade)
engine = async_engine