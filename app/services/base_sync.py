# app/services/base_sync.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Type
from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import Base
from app.services.lyceum_api import LyceumAPIClientReadOnly
from app.core.config import settings
from app.core.security import APISecurity

logger = logging.getLogger(__name__)

class BaseSyncService(ABC):
    """
    Serviço base para sincronização de entidades da API Lyceum.
    Herdeiros devem definir:
        - MODEL: classe do modelo SQLAlchemy
        - API_ENDPOINT_METHOD: nome do método no cliente (ex: "get_all_alunos")
        - UNIQUE_FIELD: nome do campo chave primária na API (ex: "aluno")
    """

    MODEL: Type[Base]
    API_ENDPOINT_METHOD: str
    UNIQUE_FIELD: str

    def __init__(self, db: AsyncSession):
        self.db = db
        self.api_client = LyceumAPIClientReadOnly()
        # Valida credenciais uma vez
        APISecurity.validate_api_credentials({
            "LYCEUM_API_BASE_URL": settings.LYCEUM_API_BASE_URL,
            "LYCEUM_API_USERNAME": settings.LYCEUM_API_USERNAME,
            "LYCEUM_API_PASSWORD": settings.LYCEUM_API_PASSWORD,
        })

    @abstractmethod
    async def normalize_data(self, raw_data: Dict) -> Dict:
        """Converte dados crus da API para o formato do modelo."""
        pass

    async def sync_all(self, incremental: bool = False) -> Dict[str, Any]:
        """
        Executa sincronização completa de todos os registros.
        Retorna estatísticas da operação.
        """
        logger.info(f"Iniciando sincronização de {self.MODEL.__tablename__} (incremental={incremental})")
        stats = {
            "total_api": 0,
            "inseridos": 0,
            "atualizados": 0,
            "ignorados": 0,
            "erros": 0,
            "iniciado_em": datetime.now(),
        }

        # 1. Obter dados da API
        method = getattr(self.api_client, self.API_ENDPOINT_METHOD)
        items = await method()
        stats["total_api"] = len(items)

        if not items:
            logger.warning(f"Nenhum dado obtido para {self.MODEL.__tablename__}")
            return stats

        # 2. (Opcional) Para incremental, carregar stamps existentes
        existing_stamps = {}
        if incremental and hasattr(self.MODEL, "stamp_atualizacao"):
            result = await self.db.execute(
                select(self.MODEL.id, getattr(self.MODEL, self.UNIQUE_FIELD), self.MODEL.stamp_atualizacao)
            )
            existing_stamps = {getattr(row, self.UNIQUE_FIELD): row.stamp_atualizacao for row in result.all()}

        # 3. Processar cada item
        for i, item in enumerate(items, 1):
            try:
                unique_value = item.get(self.UNIQUE_FIELD)
                if not unique_value:
                    stats["ignorados"] += 1
                    continue

                # Incremental: verificar se stamp mudou
                if incremental and unique_value in existing_stamps:
                    stamp_atual = item.get("stamp_atualizacao")
                    if stamp_atual == existing_stamps[unique_value]:
                        stats["ignorados"] += 1
                        if i % 100 == 0:
                            logger.info(f"Processados {i}/{len(items)} registros...")
                        continue

                # Normalizar dados
                normalized = await self.normalize_data(item)

                # Buscar existente
                stmt = select(self.MODEL).where(
                    getattr(self.MODEL, self.UNIQUE_FIELD) == unique_value
                )
                result = await self.db.execute(stmt)
                existing = result.scalar_one_or_none()

                if existing:
                    # Atualizar
                    for key, value in normalized.items():
                        if key != self.UNIQUE_FIELD and key not in ["id", "data_criacao"]:
                            setattr(existing, key, value)
                    stats["atualizados"] += 1
                else:
                    # Inserir
                    new_obj = self.MODEL(**normalized)
                    self.db.add(new_obj)
                    stats["inseridos"] += 1

                if i % 100 == 0:
                    logger.info(f"Processados {i}/{len(items)} registros...")

            except Exception as e:
                stats["erros"] += 1
                logger.error(f"Erro no registro {i} ({self.UNIQUE_FIELD}={item.get(self.UNIQUE_FIELD)}): {e}")

        # 4. Commit
        try:
            await self.db.commit()
            logger.info(f"Sincronização de {self.MODEL.__tablename__} concluída com sucesso")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Erro no commit: {e}")
            stats["erros"] += 1

        stats["concluido_em"] = datetime.now()
        stats["duracao"] = (stats["concluido_em"] - stats["iniciado_em"]).total_seconds()
        return stats

    # Conversores auxiliares (podem ser reutilizados)
    @staticmethod
    def _safe_int(v):
        if v is None:
            return None
        try:
            return int(v)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _safe_float(v):
        if v is None:
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _safe_str(v):
        if v is None:
            return None
        return str(v).strip()

    @staticmethod
    def _parse_datetime(v):
        if v is None:
            return None
        try:
            if isinstance(v, (int, float)):
                if v > 1_000_000_000_000:
                    v = v / 1000
                return datetime.fromtimestamp(v)
            elif isinstance(v, str):
                v = v.replace("Z", "+00:00")
                return datetime.fromisoformat(v.split("+")[0])
        except Exception:
            return None
        return None