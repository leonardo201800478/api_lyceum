from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
import math

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Modelo para resposta paginada"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
    
    @classmethod
    def create(cls, items: List[T], total: int, page: int, size: int) -> 'PaginatedResponse[T]':
        pages = math.ceil(total / size) if size > 0 else 1
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )


async def paginate_query(
    session: AsyncSession,
    query: Select,
    page: int = 1,
    size: int = 50,
    max_size: int = 100
) -> PaginatedResponse:
    """
    Pagina uma query SQLAlchemy
    
    Args:
        session: Sessão do banco de dados
        query: Query SQLAlchemy
        page: Número da página (1-indexed)
        size: Tamanho da página
        max_size: Tamanho máximo permitido
        
    Returns:
        PaginatedResponse: Resultado paginado
    """
    from sqlalchemy import func
    
    # Validação de parâmetros
    if page < 1:
        page = 1
    if size < 1:
        size = 50
    if size > max_size:
        size = max_size
    
    # Conta total de registros
    count_query = query.with_only_columns(func.count()).order_by(None)
    total_result = await session.execute(count_query)
    total = total_result.scalar()
    
    # Aplica paginação
    offset = (page - 1) * size
    paginated_query = query.offset(offset).limit(size)
    
    # Executa query paginada
    result = await session.execute(paginated_query)
    items = result.scalars().all()
    
    return PaginatedResponse.create(
        items=items,
        total=total,
        page=page,
        size=size,
    )