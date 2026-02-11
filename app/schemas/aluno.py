# app/schemas/aluno.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.utils.pagination import PaginatedResponse

# ------------------------------------------------------------
# AlunoBase – campos comuns
# ------------------------------------------------------------
class AlunoBase(BaseModel):
    aluno: Optional[str] = None
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

    @validator('representante_turma')
    def validate_representante(cls, v):
        if v is not None and v not in ['S', 'N']:
            raise ValueError('representante_turma deve ser "S" ou "N"')
        return v

# ------------------------------------------------------------
# AlunoCreate – obriga matrícula
# ------------------------------------------------------------
class AlunoCreate(AlunoBase):
    aluno: str = Field(..., description="Matrícula do aluno (obrigatório)")

# ------------------------------------------------------------
# AlunoUpdate – todos os campos opcionais
# ------------------------------------------------------------
class AlunoUpdate(BaseModel):
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

# ------------------------------------------------------------
# AlunoInDB – representa o modelo armazenado
# ------------------------------------------------------------
class AlunoInDB(AlunoBase):
    data_sincronizacao: datetime
    data_criacao: datetime
    data_atualizacao: datetime
    sincronizado: bool

    class Config:
        from_attributes = True

# ------------------------------------------------------------
# AlunoResponse – resposta padrão (igual ao InDB)
# ------------------------------------------------------------
class AlunoResponse(AlunoInDB):
    pass

# ------------------------------------------------------------
# AlunoFull – versão completa (igual ao Base, mas sem metadados)
# ------------------------------------------------------------
class AlunoFull(AlunoBase):
    """Schema completo com todos os campos do aluno (sem campos de controle)."""
    pass

# ------------------------------------------------------------
# AlunoListResponse – resposta paginada
# ------------------------------------------------------------
class AlunoListResponse(PaginatedResponse):
    items: list[AlunoResponse]