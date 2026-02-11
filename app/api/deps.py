# app/api/deps.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependência para obter sessão assíncrona do banco."""
    async for session in get_async_db():
        yield session

# Alias para compatibilidade
get_db = get_async_session