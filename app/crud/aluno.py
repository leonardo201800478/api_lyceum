from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, or_
from sqlalchemy.orm import joinedload
from app.models.ly_aluno import LYAluno
from app.schemas.aluno import AlunoCreate, AlunoUpdate
from app.utils.pagination import paginate_query
import logging

logger = logging.getLogger(__name__)


class CRUDAluno:
    """CRUD operations for LYAluno"""
    
    def __init__(self, model: LYAluno = LYAluno):
        self.model = model
    
    async def get(self, db: AsyncSession, aluno_id: str) -> Optional[LYAluno]:
        """Get aluno by matrícula"""
        result = await db.execute(
            select(self.model).where(self.model.aluno == aluno_id)
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
    ) -> List[LYAluno]:
        """Get multiple alunos with optional filtering"""
        query = select(self.model)
        
        # Apply filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    if isinstance(value, str):
                        query = query.where(
                            getattr(self.model, key).ilike(f"%{value}%")
                        )
                    else:
                        query = query.where(
                            getattr(self.model, key) == value
                        )
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by.lstrip('- ')):
            if order_by.startswith('-'):
                query = query.order_by(
                    getattr(self.model, order_by[1:]).desc()
                )
            else:
                query = query.order_by(
                    getattr(self.model, order_by)
                )
        else:
            query = query.order_by(self.model.aluno)
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_paginated(
        self,
        db: AsyncSession,
        *,
        page: int = 1,
        size: int = 50,
        search: Optional[str] = None,
        curso: Optional[str] = None,
        serie: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get paginated alunos with filtering and ordering"""
        query = select(self.model)
        
        # Apply search
        if search:
            query = query.where(
                or_(
                    self.model.nome_compl.ilike(f"%{search}%"),
                    self.model.nome_abrev.ilike(f"%{search}%"),
                    self.model.aluno.ilike(f"%{search}%"),
                    self.model.e_mail_interno.ilike(f"%{search}%"),
                )
            )
        
        # Apply filters
        if curso:
            query = query.where(self.model.curso.ilike(f"%{curso}%"))
        
        if serie:
            query = query.where(self.model.serie == serie)
        
        # Apply ordering
        order_fields = {
            "aluno": self.model.aluno,
            "nome": self.model.nome_compl,
            "curso": self.model.curso,
            "serie": self.model.serie,
            "data_sincronizacao": self.model.data_sincronizacao,
        }
        
        if order_by and order_by.lstrip('-') in order_fields:
            field = order_fields[order_by.lstrip('-')]
            if order_by.startswith('-'):
                query = query.order_by(field.desc())
            else:
                query = query.order_by(field)
        else:
            query = query.order_by(self.model.nome_compl)
        
        return await paginate_query(db, query, page=page, size=size)
    
    async def create(self, db: AsyncSession, *, obj_in: AlunoCreate) -> LYAluno:
        """Create new aluno"""
        db_obj = self.model(**obj_in.dict(exclude_unset=True))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: LYAluno,
        obj_in: AlunoUpdate
    ) -> LYAluno:
        """Update existing aluno"""
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def remove(self, db: AsyncSession, *, aluno_id: str) -> Optional[LYAluno]:
        """Delete aluno"""
        aluno = await self.get(db, aluno_id=aluno_id)
        if aluno:
            await db.delete(aluno)
            await db.commit()
        return aluno
    
    async def count(self, db: AsyncSession) -> int:
        """Count total alunos"""
        result = await db.execute(select(func.count()).select_from(self.model))
        return result.scalar()
    
    async def get_stats(self, db: AsyncSession) -> Dict[str, Any]:
        """Get statistics about alunos"""
        # Total count
        total_result = await db.execute(
            select(func.count()).select_from(self.model)
        )
        total = total_result.scalar()
        
        # Count by curso
        curso_result = await db.execute(
            select(self.model.curso, func.count())
            .where(self.model.curso.isnot(None))
            .group_by(self.model.curso)
            .order_by(func.count().desc())
        )
        by_curso = {row[0]: row[1] for row in curso_result.all()}
        
        # Count by serie
        serie_result = await db.execute(
            select(self.model.serie, func.count())
            .where(self.model.serie.isnot(None))
            .group_by(self.model.serie)
            .order_by(self.model.serie)
        )
        by_serie = {str(row[0]): row[1] for row in serie_result.all()}
        
        # Last sync
        last_sync_result = await db.execute(
            select(func.max(self.model.data_sincronizacao))
        )
        last_sync = last_sync_result.scalar()
        
        return {
            "total": total,
            "by_curso": by_curso,
            "by_serie": by_serie,
            "last_sync": last_sync,
        }


aluno = CRUDAluno()