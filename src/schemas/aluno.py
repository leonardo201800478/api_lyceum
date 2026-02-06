from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class InstituicaoBase(BaseModel):
    id: int
    nome: str
    codigo_inep: str
    tipo: str
    
    class Config:
        from_attributes = True

class AlunoBase(BaseModel):
    nome: str
    email: EmailStr
    cpf: str
    data_nascimento: date
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    matricula: str
    ativo: bool = True
    instituicao_id: int

class Aluno(AlunoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    instituicao: InstituicaoBase
    
    class Config:
        from_attributes = True
