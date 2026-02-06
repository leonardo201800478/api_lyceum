import logging
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from src.models.aluno import Aluno
from src.schemas.aluno import AlunoCreate, AlunoUpdate

logger = logging.getLogger(__name__)

class AlunoSyncService:
    def __init__(self, db: Session):
        self.db = db
    
    def sync_from_external(self, external_data: List[dict], instituicao_id: int):
        """
        Sincroniza alunos a partir de dados externos.
        
        Args:
            external_data: Lista de dicionários com dados dos alunos
            instituicao_id: ID da instituição
            
        Returns:
            Tuple com contadores de operações
        """
        created = 0
        updated = 0
        errors = 0
        
        for aluno_data in external_data:
            try:
                # Buscar aluno pela matrícula
                aluno_existente = self.db.query(Aluno).filter(
                    Aluno.matricula == aluno_data['matricula'],
                    Aluno.instituicao_id == instituicao_id
                ).first()
                
                if aluno_existente:
                    # Atualizar aluno existente
                    self._update_aluno(aluno_existente, aluno_data)
                    updated += 1
                else:
                    # Criar novo aluno
                    self._create_aluno(aluno_data, instituicao_id)
                    created += 1
                    
            except Exception as e:
                logger.error(f"Erro ao sincronizar aluno {aluno_data.get('matricula')}: {e}")
                errors += 1
        
        self.db.commit()
        return created, updated, errors
    
    def _create_aluno(self, aluno_data: dict, instituicao_id: int):
        """Cria um novo aluno a partir dos dados."""
        aluno_create = AlunoCreate(
            nome=aluno_data['nome'],
            email=aluno_data['email'],
            cpf=aluno_data['cpf'],
            data_nascimento=datetime.strptime(aluno_data['data_nascimento'], '%Y-%m-%d').date(),
            telefone=aluno_data.get('telefone'),
            endereco=aluno_data.get('endereco'),
            matricula=aluno_data['matricula'],
            ativo=aluno_data.get('ativo', True),
            instituicao_id=instituicao_id
        )
        
        aluno = Aluno(**aluno_create.dict())
        self.db.add(aluno)
    
    def _update_aluno(self, aluno: Aluno, aluno_data: dict):
        """Atualiza um aluno existente."""
        for field, value in aluno_data.items():
            if hasattr(aluno, field) and field not in ['id', 'created_at', 'updated_at']:
                if field == 'data_nascimento':
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                setattr(aluno, field, value)
        
        aluno.ativo = aluno_data.get('ativo', aluno.ativo)