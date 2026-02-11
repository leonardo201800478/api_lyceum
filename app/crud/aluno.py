# app/crud/aluno.py
from app.crud.base import CRUDBase
from app.models.ly_aluno import LYAluno
from app.schemas.aluno import AlunoCreate, AlunoUpdate

class CRUDAluno(CRUDBase[LYAluno, AlunoCreate, AlunoUpdate]):
    async def get(self, db, aluno_id: str):
        """Busca aluno pela matrícula (campo 'aluno')."""
        return await self.get_by_unique(db, "aluno", aluno_id)

aluno = CRUDAluno(LYAluno)