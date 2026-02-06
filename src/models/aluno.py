from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Aluno(BaseModel):
    __tablename__ = "alunos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20))
    endereco = Column(Text)
    matricula = Column(String(50), unique=True, nullable=False, index=True)
    ativo = Column(Boolean, default=True, index=True)
    
    instituicao_id = Column(Integer, ForeignKey("instituicoes.id"), nullable=False, index=True)
    instituicao = relationship("Instituicao", back_populates="alunos", lazy="joined")
    
    def __repr__(self):
        return f"<Aluno {self.matricula} - {self.nome}>"
