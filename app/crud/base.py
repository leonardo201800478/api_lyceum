# app/crud/base.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.core.database import Base
from app.utils.pagination import paginate_query, PaginatedResponse

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_by_unique(self, db: AsyncSession, field: str, value: Any) -> Optional[ModelType]:
        """Busca por campo único (ex: 'aluno', 'curso')."""
        result = await db.execute(
            select(self.model).where(getattr(self.model, field) == value)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        query = select(self.model)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    if isinstance(value, str):
                        query = query.where(getattr(self.model, key).ilike(f"%{value}%"))
                    else:
                        query = query.where(getattr(self.model, key) == value)
        if order_by and hasattr(self.model, order_by.lstrip('-')):
            if order_by.startswith('-'):
                query = query.order_by(getattr(self.model, order_by[1:]).desc())
            else:
                query = query.order_by(getattr(self.model, order_by))
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_paginated(
        self,
        db: AsyncSession,
        page: int = 1,
        size: int = 50,
        search: Optional[str] = None,
        search_fields: Optional[List[str]] = None,
        order_by: Optional[str] = None,
        **filters
    ) -> PaginatedResponse:
        query = select(self.model)
        # Busca textual
        if search and search_fields:
            conditions = [
                getattr(self.model, field).ilike(f"%{search}%")
                for field in search_fields if hasattr(self.model, field)
            ]
            if conditions:
                query = query.where(or_(*conditions))
        # Filtros exatos
        for k, v in filters.items():
            if hasattr(self.model, k) and v is not None:
                query = query.where(getattr(self.model, k) == v)
        # Ordenação
        if order_by and hasattr(self.model, order_by.lstrip('-')):
            if order_by.startswith('-'):
                query = query.order_by(getattr(self.model, order_by[1:]).desc())
            else:
                query = query.order_by(getattr(self.model, order_by))
        else:
            # Ordenação padrão pelo primeiro campo da PK
            pk = self.model.__table__.primary_key.columns.keys()[0]
            query = query.order_by(getattr(self.model, pk))
        return await paginate_query(db, query, page=page, size=size)

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: Any) -> Optional[ModelType]:
        obj = await self.get(db, id=id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count()).select_from(self.model))
        return result.scalar()