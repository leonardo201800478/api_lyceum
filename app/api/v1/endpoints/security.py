from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.lyceum_api import LyceumAPIClientReadOnly
from app.core.security import APISecurity
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/lyceum/health")
async def check_lyceum_api_health():
    """
    Verifica a saude da API Lyceum externa
    
    - Realiza uma requisicao GET simples
    - Verifica se as credenciais estao configuradas
    - Retorna status da conexao
    """
    try:
        client = LyceumAPIClientReadOnly()
        
        # Validar credenciais primeiro
        from app.core.config import settings
        APISecurity.validate_api_credentials({
            "LYCEUM_API_BASE_URL": settings.LYCEUM_API_BASE_URL,
            "LYCEUM_API_USERNAME": settings.LYCEUM_API_USERNAME,
            "LYCEUM_API_PASSWORD": settings.LYCEUM_API_PASSWORD,
        })
        
        # Verificar saude
        health_status = await client.health_check()
        
        return {
            "api_lyceum": health_status,
            "security_mode": "read_only",
            "allowed_methods": ["GET"],
            "message": "API Lyceum configurada em modo READ-ONLY"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro ao verificar saude da API Lyceum: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao verificar API Lyceum: {str(e)}"
        )


@router.get("/lyceum/endpoints")
async def list_lyceum_endpoints():
    """
    Lista os endpoints Lyceum disponiveis (apenas GET)
    
    Retorna todos os endpoints que podem ser consultados
    no modo read-only
    """
    client = LyceumAPIClientReadOnly()
    
    return {
        "available_endpoints": list(client.GET_ENDPOINTS.keys()),
        "security_note": "Todos os endpoints sao acessiveis apenas via GET",
        "rate_limits": APISecurity.get_lyceum_rate_limits()
    }


@router.get("/security/status")
async def get_security_status():
    """
    Retorna o status de seguranca atual
    
    Mostra configuracoes de seguranca ativas para API Lyceum
    """
    return {
        "lyceum_api_mode": "read_only",
        "allowed_http_methods": ["GET"],
        "blocked_http_methods": ["POST", "PUT", "DELETE", "PATCH"],
        "rate_limiting": APISecurity.get_lyceum_rate_limits(),
        "security_features": [
            "Method validation",
            "Credential validation", 
            "Rate limiting",
            "Request logging",
            "Read-only mode enforcement"
        ]
    }