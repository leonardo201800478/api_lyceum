# app/api/deps.py
"""
Dependencies para endpoints da API
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db, AsyncSessionLocal


# Função principal para obter sessão assíncrona
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para obter sessao assincrona do banco
    
    Uso:
        @router.get("/")
        async def endpoint(db: AsyncSession = Depends(get_async_session)):
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Alias para compatibilidade - usa get_db se disponível, senão usa get_async_session
try:
    # Se get_db existe e é uma função async generator, use-a
    from app.core.database import get_db
    
    async def get_database() -> AsyncGenerator[AsyncSession, None]:
        """Alias para get_db para compatibilidade"""
        async for session in get_db():
            yield session
except ImportError:
    # Fallback para get_async_session
    get_database = get_async_session


# Exporta as funcoes
__all__ = ['get_db', 'get_async_session', 'get_database']