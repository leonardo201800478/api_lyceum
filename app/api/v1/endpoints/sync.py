from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.api.deps import get_db
from app.services.sync_service import SyncService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/alunos", response_model=dict)
async def sync_alunos(
    background_tasks: BackgroundTasks,
    incremental: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    Iniciar sincronizacao de alunos
    
    - **incremental**: Se True, sincroniza apenas registros alterados
    """
    try:
        sync_service = SyncService(db)
        
        # Executa sincronizacao em background
        async def run_sync():
            try:
                stats = await sync_service.sync_alunos(incremental=incremental)
                logger.info(f"Sincronizacao concluida: {stats}")
            except Exception as e:
                logger.error(f"Erro na sincronizacao em background: {e}")
        
        # Adiciona tarefa em background
        background_tasks.add_task(run_sync)
        
        return {
            "message": "Sincronizacao iniciada em background",
            "incremental": incremental,
            "started_at": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Erro ao iniciar sincronizacao: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao iniciar sincronizacao: {str(e)}"
        )


@router.get("/status", response_model=dict)
async def get_sync_status():
    """
    Obter status da ultima sincronizacao
    
    Nota: Em producao, implementar tracking de jobs
    """
    return {
        "status": "not_implemented",
        "message": "Status tracking nao implementado nesta versao",
        "suggestion": "Verifique os logs para informacoes de sincronizacao",
    }