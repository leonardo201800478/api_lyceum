from typing import Generator, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency para obter sessão do banco"""
    async for session in get_async_session():
        yield session