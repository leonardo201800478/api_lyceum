from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime
import psutil
from app.api.deps import get_db

router = APIRouter()


@router.get("/", response_model=dict)
async def health_check(
    db: AsyncSession = Depends(get_db)
):
    """Health check da aplicação"""
    # Verifica conexão com banco de dados
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Informações do sistema
    system_info = {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
    }
    
    return {
        "status": "ok",
        "database": db_status,
        "system": system_info,
        "version": "1.0.0",
    }


@router.get("/ping")
async def ping():
    """Endpoint simples de ping"""
    return {"message": "pong", "timestamp": datetime.now().isoformat()}