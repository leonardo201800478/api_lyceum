from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.utils.pagination import PaginatedResponse


class AlunoBase(BaseModel):
    """Base schema para aluno"""
    aluno: Optional[str] = Field(None, description="Matrícula do aluno")
    ano_ingresso: Optional[int] = Field(None, description="Ano de ingresso")
    anoconcl2g: Optional[int] = Field(None, description="Ano conclusão 2º grau")
    nome_compl: Optional[str] = Field(None, description="Nome completo")
    nome_abrev: Optional[str] = Field(None, description="Nome abreviado")
    curso: Optional[str] = Field(None, description="Curso")
    serie: Optional[int] = Field(None, description="Série")
    turno: Optional[str] = Field(None, description="Turno")
    sit_aluno: Optional[str] = Field(None, description="Situação do aluno")


class AlunoCreate(AlunoBase):
    """Schema para criação de aluno"""
    aluno: str = Field(..., description="Matrícula do aluno (obrigatório)")


class AlunoUpdate(BaseModel):
    """Schema para atualização de aluno"""
    ano_ingresso: Optional[int] = None
    anoconcl2g: Optional[int] = None
    nome_compl: Optional[str] = None
    nome_abrev: Optional[str] = None
    curso: Optional[str] = None
    serie: Optional[int] = None
    turno: Optional[str] = None
    sit_aluno: Optional[str] = None


class AlunoInDB(AlunoBase):
    """Schema para aluno no banco de dados"""
    id: int
    data_criacao: datetime
    data_atualizacao: datetime
    sincronizado: bool
    
    class Config:
        from_attributes = True


class AlunoResponse(AlunoInDB):
    """Schema para resposta de aluno"""
    pass


class AlunoListResponse(PaginatedResponse):
    """Schema para resposta paginada de alunos"""
    items: List[AlunoResponse]


# Schema completo com todos os campos
class AlunoFull(BaseModel):
    """Schema completo com todos os campos do aluno"""
    aluno: str = Field(..., description="Matrícula do aluno")
    ano_ingresso: Optional[int] = None
    anoconcl2g: Optional[int] = None
    areacnpq: Optional[str] = None
    candidato: Optional[str] = None
    cidade2g: Optional[str] = None
    classif_aluno: Optional[str] = None
    cod_cartao: Optional[str] = None
    concurso: Optional[str] = None
    cred_educativo: Optional[str] = None
    creditos: Optional[int] = None
    curriculo: Optional[str] = None
    curso: Optional[str] = None
    curso_ant: Optional[str] = None
    discipoutraserie: Optional[str] = None
    dist_aluno_unidade: Optional[int] = None
    dt_ingresso: Optional[datetime] = None
    e_mail_interno: Optional[str] = None
    faculdade_conveniada: Optional[str] = None
    grupo: Optional[str] = None
    instituicao: Optional[str] = None
    nome_abrev: Optional[str] = None
    nome_compl: Optional[str] = None
    nome_conjuge: Optional[str] = None
    nome_social: Optional[str] = None
    num_chamada: Optional[int] = None
    obs_aluno_finan: Optional[str] = None
    obs_tel_com: Optional[str] = None
    obs_tel_res: Optional[str] = None
    outra_faculdade: Optional[str] = None
    pais2g: Optional[str] = None
    pessoa: Optional[int] = None
    ref_aluno_ant: Optional[str] = None
    representante_turma: Optional[str] = None
    sem_ingresso: Optional[int] = None
    serie: Optional[int] = None
    sit_aluno: Optional[str] = None
    sit_aprov: Optional[str] = None
    stamp_atualizacao: Optional[str] = None
    tipo_aluno: Optional[str] = None
    tipo_escola: Optional[str] = None
    tipo_ingresso: Optional[str] = None
    turma_pref: Optional[str] = None
    turno: Optional[str] = None
    unidade_ensino: Optional[str] = None
    unidade_fisica: Optional[str] = None
    data_sincronizacao: Optional[datetime] = None
    
    @validator('representante_turma')
    def validate_representante(cls, v):
        if v and v not in ['S', 'N']:
            raise ValueError('representante_turma deve ser "S" ou "N"')
        return v
    
    class Config:
        from_attributes = True