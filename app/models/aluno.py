# app/models/aluno.py
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(20), unique=True, nullable=False, index=True)
    nome = Column(String(150), nullable=False)
    ativo = Column(Boolean, default=True)