from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.sql import func
from app.core.database import Base


class LYAluno(Base):
    """Modelo SQLAlchemy para tabela LY_ALUNO"""
    __tablename__ = "ly_aluno"
    
    # Campos da API Lyceum
    aluno = Column(String(50), primary_key=True, index=True, comment="Matrícula do aluno")
    ano_ingresso = Column(Integer, nullable=True, comment="Ano de ingresso")
    anoconcl2g = Column(Integer, nullable=True, comment="Ano conclusão 2º grau")
    areacnpq = Column(String(100), nullable=True, comment="Área CNPQ")
    candidato = Column(String(100), nullable=True, comment="Candidato")
    cidade2g = Column(String(100), nullable=True, comment="Cidade 2º grau")
    classif_aluno = Column(String(50), nullable=True, comment="Classificação do aluno")
    cod_cartao = Column(String(50), nullable=True, comment="Código do cartão")
    concurso = Column(String(100), nullable=True, comment="Concurso")
    cred_educativo = Column(String(10), nullable=True, comment="Crédito educativo")
    creditos = Column(Integer, nullable=True, comment="Créditos acumulados")
    curriculo = Column(String(100), nullable=True, comment="Currículo")
    curso = Column(String(100), nullable=True, comment="Curso")
    curso_ant = Column(String(100), nullable=True, comment="Curso anterior")
    discipoutraserie = Column(String(10), nullable=True, comment="Disciplina outra série")
    dist_aluno_unidade = Column(Integer, nullable=True, comment="Distância aluno-unidade")
    dt_ingresso = Column(DateTime, nullable=True, comment="Data de ingresso")
    e_mail_interno = Column(String(200), nullable=True, comment="E-mail interno")
    faculdade_conveniada = Column(String(200), nullable=True, comment="Faculdade conveniada")
    grupo = Column(String(100), nullable=True, comment="Grupo")
    instituicao = Column(String(200), nullable=True, comment="Instituição")
    nome_abrev = Column(String(100), nullable=True, comment="Nome abreviado")
    nome_compl = Column(String(200), nullable=True, comment="Nome completo")
    nome_conjuge = Column(String(200), nullable=True, comment="Nome do cônjuge")
    nome_social = Column(String(200), nullable=True, comment="Nome social")
    num_chamada = Column(Integer, nullable=True, comment="Número de chamada")
    obs_aluno_finan = Column(Text, nullable=True, comment="Observações financeiras")
    obs_tel_com = Column(Text, nullable=True, comment="Observações telefone comercial")
    obs_tel_res = Column(Text, nullable=True, comment="Observações telefone residencial")
    outra_faculdade = Column(String(200), nullable=True, comment="Outra faculdade")
    pais2g = Column(String(100), nullable=True, comment="País 2º grau")
    pessoa = Column(Integer, nullable=True, comment="Código pessoa")
    ref_aluno_ant = Column(String(100), nullable=True, comment="Referência aluno anterior")
    representante_turma = Column(String(1), nullable=True, comment="Representante de turma (S/N)")
    sem_ingresso = Column(Integer, nullable=True, comment="Semestre de ingresso")
    serie = Column(Integer, nullable=True, comment="Série")
    sit_aluno = Column(String(50), nullable=True, comment="Situação do aluno")
    sit_aprov = Column(String(50), nullable=True, comment="Situação aprovação")
    stamp_atualizacao = Column(String(50), nullable=True, comment="Timestamp atualização")
    tipo_aluno = Column(String(50), nullable=True, comment="Tipo de aluno")
    tipo_escola = Column(String(100), nullable=True, comment="Tipo de escola")
    tipo_ingresso = Column(String(100), nullable=True, comment="Tipo de ingresso")
    turma_pref = Column(String(50), nullable=True, comment="Turma preferencial")
    turno = Column(String(50), nullable=True, comment="Turno")
    unidade_ensino = Column(String(100), nullable=True, comment="Unidade de ensino")
    unidade_fisica = Column(String(100), nullable=True, comment="Unidade física")
    
    # Campos de controle interno
    data_sincronizacao = Column(DateTime, server_default=func.now(), nullable=False, comment="Data da última sincronização")
    data_criacao = Column(DateTime, server_default=func.now(), nullable=False, comment="Data de criação no sistema")
    data_atualizacao = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Data da última atualização")
    sincronizado = Column(Boolean, default=False, nullable=False, comment="Sincronizado com sucesso")
    
    def __repr__(self):
        return f"<LYAluno(aluno='{self.aluno}', nome='{self.nome_compl}')>"