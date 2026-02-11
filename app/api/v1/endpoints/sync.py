# app/api/v1/endpoints/sync.py
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.api.deps import get_async_session
from app.services.sync_aluno import sync_alunos

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/alunos", response_model=dict)
async def sync_alunos_endpoint(
    background_tasks: BackgroundTasks,
    incremental: bool = False,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Inicia a sincronização completa dos alunos com a API Lyceum.
    A execução ocorre em background.
    """
    async def task():
        try:
            stats = await sync_alunos(db, incremental=incremental)
            logger.info(f"Sincronização de alunos concluída: {stats}")
        except Exception as e:
            logger.error(f"Erro na sincronização em background: {e}")

    background_tasks.add_task(task)
    
    return {
        "message": "Sincronização de alunos iniciada em background",
        "incremental": incremental,
        "started_at": datetime.now().isoformat(),
    }


@router.get("/status", response_model=dict)
async def get_sync_status():
    """
    Obter status da última sincronização.
    Em produção, implementar tracking de jobs com Redis/Celery.
    """
    return {
        "status": "not_implemented",
        "message": "Status tracking não implementado nesta versão",
        "suggestion": "Verifique os logs para informações de sincronização",
    }