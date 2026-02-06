from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from src.models.aluno import Aluno

class AlunoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, aluno_id: int) -> Optional[Aluno]:
        """Obtém um aluno pelo ID."""
        return self.db.query(Aluno).filter(Aluno.id == aluno_id).first()
    
    def get_by_cpf(self, cpf: str) -> Optional[Aluno]:
        """Obtém um aluno pelo CPF."""
        # Normalizar CPF: remover pontos e traço
        cpf_normalizado = cpf.replace(".", "").replace("-", "")
        
        # Buscar com CPF normalizado
        aluno = self.db.query(Aluno).filter(
            func.replace(func.replace(Aluno.cpf, '.', ''), '-', '') == cpf_normalizado
        ).first()
        
        # Se não encontrar com CPF normalizado, tentar exato
        if not aluno:
            aluno = self.db.query(Aluno).filter(Aluno.cpf == cpf).first()
        
        return aluno
    
    def get_by_matricula(self, matricula: str) -> Optional[Aluno]:
        """Obtém um aluno pela matrícula."""
        return self.db.query(Aluno).filter(Aluno.matricula == matricula).first()
    
    def get_by_email(self, email: str) -> Optional[Aluno]:
        """Obtém um aluno pelo email."""
        return self.db.query(Aluno).filter(func.lower(Aluno.email) == func.lower(email)).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 50,
        nome: Optional[str] = None,
        **filters
    ) -> List[Aluno]:
        """
        Obtém todos os alunos com filtros.
        
        Args:
            skip: Número de registros para pular
            limit: Limite de registros
            nome: Busca parcial por nome
            **filters: Filtros adicionais (ativo, cpf, matricula, email, instituicao_id)
        """
        query = self.db.query(Aluno)
        
        # Busca por nome (parcial, case-insensitive)
        if nome:
            query = query.filter(Aluno.nome.ilike(f"%{nome}%"))
        
        # Aplicar filtros exatos
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
        
        # Ordenar por nome e ID
        query = query.order_by(Aluno.nome, Aluno.id)
        
        # Aplicar paginação
        return query.offset(skip).limit(limit).all()
    
    def count(self, **filters) -> int:
        """Conta o total de alunos com filtros."""
        query = self.db.query(Aluno)
        
        # Aplicar filtros
        if 'ativo' in filters:
            query = query.filter(Aluno.ativo == filters['ativo'])
        
        if 'instituicao_id' in filters:
            query = query.filter(Aluno.instituicao_id == filters['instituicao_id'])
        
        return query.count()