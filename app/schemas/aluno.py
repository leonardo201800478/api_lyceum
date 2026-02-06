# app/schemas/aluno.py
from pydantic import BaseModel


class AlunoBase(BaseModel):
    matricula: str
    nome: str
    ativo: bool = True


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(BaseModel):
    nome: str | None = None
    ativo: bool | None = None


class AlunoOut(AlunoBase):
    id: int

    class Config:
        orm_mode = True