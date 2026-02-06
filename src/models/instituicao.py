from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
import enum
from src.models.base import BaseModel

class TipoInstituicao(str, enum.Enum):
    FEDERAL = "federal"
    ESTADUAL = "estadual"
    MUNICIPAL = "municipal"
    PRIVADA = "privada"

class Instituicao(BaseModel):
    __tablename__ = "instituicoes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    codigo_inep = Column(String(20), unique=True, nullable=False)
    tipo = Column(Enum(TipoInstituicao), nullable=False)
    endereco = Column(Text)
    cidade = Column(String(100))
    estado = Column(String(2))
    telefone = Column(String(20))
    email = Column(String(100))
    
    # Relacionamento com alunos (apenas para referência)
    alunos = relationship("Aluno", back_populates="instituicao", lazy="select")
    
    def __repr__(self):
        return f"<Instituicao {self.codigo_inep} - {self.nome}>"