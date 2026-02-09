"""
Dependencies para endpoints da API
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db, get_async_session


# Para compatibilidade com codigo existente
async def get_database() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para obter sessao do banco (alias para get_db)
    
    Uso:
        @router.get("/")
        async def endpoint(db: AsyncSession = Depends(get_database)):
    """
    async for session in get_db():
        yield session


# Exporta as mesmas funcoes
__all__ = ['get_db', 'get_async_session', 'get_database']