# app/utils/pagination.py
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
import math

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int      # página atual (0‑indexada)
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
            has_next=page + 1 < pages,
            has_prev=page > 0,
        )

async def paginate_query(
    session: AsyncSession,
    query: Select,
    page: int = 0,          # ← página 0‑indexada (padrão)
    size: int = 50,
    max_size: int = 100
) -> PaginatedResponse:
    from sqlalchemy import func

    if page < 0:
        page = 0
    if size < 1:
        size = 50
    if size > max_size:
        size = max_size

    # Total de registros
    count_query = query.with_only_columns(func.count()).order_by(None)
    total_result = await session.execute(count_query)
    total = total_result.scalar() or 0

    # Offset = página * tamanho (página 0 → offset 0)
    offset = page * size
    paginated_query = query.offset(offset).limit(size)
    result = await session.execute(paginated_query)
    items = result.scalars().all()

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=page,
        size=size,
    )