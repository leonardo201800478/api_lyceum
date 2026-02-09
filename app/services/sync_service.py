from typing import List, Dict, Optional, Any
from datetime import datetime
import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.ly_aluno import LYAluno
from app.services.lyceum_api import LyceumAPIClientReadOnly
from app.core.security import APISecurity

logger = logging.getLogger(__name__)


class SyncService:
    """Serviço de sincronização com API Lyceum - APENAS LEITURA"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        # Usar cliente read-only
        self.api_client = LyceumAPIClientReadOnly()
        
        # Validar credenciais
        from app.core.config import settings
        APISecurity.validate_api_credentials({
            "LYCEUM_API_BASE_URL": settings.LYCEUM_API_BASE_URL,
            "LYCEUM_API_USERNAME": settings.LYCEUM_API_USERNAME,
            "LYCEUM_API_PASSWORD": settings.LYCEUM_API_PASSWORD,
        })
        
        logger.info("SyncService inicializado (modo READ-ONLY para API Lyceum)")
    
    async def check_api_health(self) -> Dict[str, Any]:
        """Verifica saúde da API Lyceum (GET apenas)"""
        return await self.api_client.health_check()
    
    # Adicionar este método após o __init__:
    async def normalize_aluno_data(self, aluno_data: Dict) -> Dict:
        """Normaliza dados do aluno da API para o modelo local"""
        normalized = {}
        
        # Mapeamento de campos
        field_mappings = {
            'aluno': ('aluno', self._safe_str),
            'ano_ingresso': ('ano_ingresso', self._safe_int),
            'anoconcl2g': ('anoconcl2g', self._safe_int),
            'areacnpq': ('areacnpq', self._safe_str),
            'candidato': ('candidato', self._safe_str),
            'nome_compl': ('nome_compl', self._safe_str),
            'nome_abrev': ('nome_abrev', self._safe_str),
            'curso': ('curso', self._safe_str),
            'serie': ('serie', self._safe_int),
            'turno': ('turno', self._safe_str),
            'sit_aluno': ('sit_aluno', self._safe_str),
            'representante_turma': ('representante_turma', self._safe_representante),
            'e_mail_interno': ('e_mail_interno', self._safe_str),
            'stamp_atualizacao': ('stamp_atualizacao', self._safe_str),
            'tipo_aluno': ('tipo_aluno', self._safe_str),
            'unidade_ensino': ('unidade_ensino', self._safe_str),
        }
        
        # Processa cada campo
        for api_field, (db_field, converter) in field_mappings.items():
            value = aluno_data.get(api_field)
            normalized[db_field] = converter(value) if converter else value
        
        # Adiciona timestamps
        normalized['data_sincronizacao'] = datetime.now()
        normalized['sincronizado'] = True
        
        return normalized

    def _safe_int(self, value) -> Optional[int]:
        """Converte valor para inteiro de forma segura"""
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    def _safe_str(self, value) -> Optional[str]:
        """Converte valor para string de forma segura"""
        if value is None:
            return None
        return str(value).strip()
    
    def _safe_representante(self, value) -> Optional[str]:
        """Valida valor de representante_turma"""
        if value is None:
            return None
        value_str = str(value).strip().upper()
        return value_str if value_str in ['S', 'N'] else None
    
    def _parse_datetime(self, value) -> Optional[datetime]:
        """Tenta parsear valor para datetime"""
        if value is None:
            return None
        try:
            # Tenta converter timestamp (milissegundos)
            if isinstance(value, (int, float)):
                if value > 1000000000000:  # Está em milissegundos
                    value = value / 1000
                return datetime.fromtimestamp(value)
            # Tenta parsear string
            elif isinstance(value, str):
                # Remove timezone se existir
                if '+' in value:
                    value = value.split('+')[0]
                return datetime.fromisoformat(value.replace('Z', ''))
        except (ValueError, TypeError):
            return None
        return None
    
    async def sync_alunos(self, incremental: bool = False) -> Dict:
        """
        Sincroniza alunos da API Lyceum com o banco local
        
        Args:
            incremental: Se True, apenas sincroniza registros alterados
            
        Returns:
            Dict com estatísticas da sincronização
        """
        logger.info(f"Iniciando sincronização de alunos (incremental={incremental})")
        
        stats = {
            "total_api": 0,
            "inseridos": 0,
            "atualizados": 0,
            "ignorados": 0,
            "erros": 0,
            "iniciado_em": datetime.now(),
        }
        
        try:
            # Obtém alunos da API
            alunos_api = await self.api_client.get_all_alunos()
            stats["total_api"] = len(alunos_api)
            
            if not alunos_api:
                logger.warning("Nenhum aluno obtido da API")
                return stats
            
            # Para incremental, obtém stamps existentes
            existing_stamps = {}
            if incremental:
                result = await self.db.execute(
                    select(LYAluno.aluno, LYAluno.stamp_atualizacao)
                )
                existing_stamps = {row[0]: row[1] for row in result.all()}
            
            # Processa cada aluno
            for i, aluno_data in enumerate(alunos_api, 1):
                try:
                    if not isinstance(aluno_data, dict):
                        stats["ignorados"] += 1
                        continue
                    
                    matricula = aluno_data.get("aluno")
                    if not matricula:
                        stats["ignorados"] += 1
                        continue
                    
                    # Verifica se precisa atualizar (modo incremental)
                    if incremental and matricula in existing_stamps:
                        stamp_existente = existing_stamps[matricula]
                        stamp_api = aluno_data.get("stamp_atualizacao")
                        
                        if stamp_existente == stamp_api:
                            stats["ignorados"] += 1
                            if i % 100 == 0:
                                logger.info(f"Processados {i}/{len(alunos_api)} alunos...")
                            continue
                    
                    # Normaliza dados
                    aluno_normalizado = await self.normalize_aluno_data(aluno_data)
                    
                    # Verifica se já existe
                    existing = await self.db.execute(
                        select(LYAluno).where(LYAluno.aluno == matricula)
                    )
                    existing = existing.scalar_one_or_none()
                    
                    if existing:
                        # Atualiza
                        for key, value in aluno_normalizado.items():
                            if key not in ["aluno", "data_criacao"]:
                                setattr(existing, key, value)
                        stats["atualizados"] += 1
                    else:
                        # Insere novo
                        aluno_db = LYAluno(**aluno_normalizado)
                        self.db.add(aluno_db)
                        stats["inseridos"] += 1
                    
                    # Log de progresso
                    if i % 100 == 0:
                        logger.info(f"Processados {i}/{len(alunos_api)} alunos...")
                        
                except Exception as e:
                    stats["erros"] += 1
                    logger.error(f"Erro processando aluno {i}: {e}")
            
            # Commit das alterações
            await self.db.commit()
            
            logger.info("Sincronização concluída com sucesso")
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Erro na sincronização: {e}")
            stats["erros"] += 1
        
        stats["concluido_em"] = datetime.now()
        stats["duracao"] = (stats["concluido_em"] - stats["iniciado_em"]).total_seconds()
        
        return stats