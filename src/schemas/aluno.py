from pydantic import BaseModel, EmailStr, validator
from datetime import date, datetime
from typing import Optional
import re

class InstituicaoBase(BaseModel):
    """Schema base para instituição (apenas para relacionamento)."""
    id: int
    nome: str
    codigo_inep: str
    tipo: str
    
    class Config:
        from_attributes = True

class AlunoBase(BaseModel):
    """Schema base para aluno."""
    nome: str
    email: EmailStr
    cpf: str
    data_nascimento: date
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    matricula: str
    ativo: bool = True
    instituicao_id: int
    
    @validator('cpf')
    def validate_cpf(cls, v):
        """Valida e formata CPF."""
        # Remover caracteres não numéricos
        cpf = re.sub(r'\D', '', v)
        
        if len(cpf) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        
        # Validar primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if digito1 != int(cpf[9]):
            raise ValueError('CPF inválido')
        
        # Validar segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        if digito2 != int(cpf[10]):
            raise ValueError('CPF inválido')
        
        # Formatar CPF
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

class Aluno(AlunoBase):
    """Schema completo de aluno com dados da instituição."""
    id: int
    created_at: datetime
    updated_at: datetime
    instituicao: InstituicaoBase
    
    class Config:
        from_attributes = True