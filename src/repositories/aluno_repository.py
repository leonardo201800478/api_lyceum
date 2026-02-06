from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from src.models.aluno import Aluno

class AlunoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, aluno_id: int) -> Optional[Aluno]:
        return self.db.query(Aluno).filter(Aluno.id == aluno_id).first()
    
    def get_by_cpf(self, cpf: str) -> Optional[Aluno]:
        cpf_normalizado = cpf.replace(".", "").replace("-", "")
        aluno = self.db.query(Aluno).filter(
            func.replace(func.replace(Aluno.cpf, '.', ''), '-', '') == cpf_normalizado
        ).first()
        
        if not aluno:
            aluno = self.db.query(Aluno).filter(Aluno.cpf == cpf).first()
        
        return aluno
    
    def get_by_matricula(self, matricula: str) -> Optional[Aluno]:
        return self.db.query(Aluno).filter(Aluno.matricula == matricula).first()
    
    def get_by_email(self, email: str) -> Optional[Aluno]:
        return self.db.query(Aluno).filter(func.lower(Aluno.email) == func.lower(email)).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 50,
        nome: Optional[str] = None,
        **filters
    ) -> List[Aluno]:
        query = self.db.query(Aluno)
        
        if nome:
            query = query.filter(Aluno.nome.ilike(f"%{nome}%"))
        
        if 'ativo' in filters:
            query = query.filter(Aluno.ativo == filters['ativo'])
        
        if 'cpf' in filters:
            cpf = filters['cpf']
            cpf_normalizado = cpf.replace(".", "").replace("-", "")
            query = query.filter(
                or_(
                    Aluno.cpf == cpf,
                    func.replace(func.replace(Aluno.cpf, '.', ''), '-', '') == cpf_normalizado
                )
            )
        
        if 'matricula' in filters:
            query = query.filter(Aluno.matricula == filters['matricula'])
        
        if 'email' in filters:
            query = query.filter(func.lower(Aluno.email) == func.lower(filters['email']))
        
        if 'instituicao_id' in filters:
            query = query.filter(Aluno.instituicao_id == filters['instituicao_id'])
        
        query = query.order_by(Aluno.nome, Aluno.id)
        
        return query.offset(skip).limit(limit).all()
