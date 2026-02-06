import logging
from typing import Dict, Any
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class APISecurity:
    """Classe para validações de segurança da API"""
    
    @staticmethod
    def validate_lyceum_request(method: str, endpoint: str) -> bool:
        """
        Valida se uma requisição para API Lyceum é permitida
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE, etc.)
            endpoint: Endpoint da API
            
        Returns:
            True se permitido, False caso contrário
            
        Raises:
            HTTPException: Se método não for GET
        """
        method = method.upper()
        
        # APENAS GET é permitido para API Lyceum
        if method != "GET":
            logger.error(f"Tentativa de uso de método {method} na API Lyceum (não permitido)")
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail=f"Método {method} não é permitido para API Lyceum (apenas GET)"
            )
        
        # Validar endpoint (opcional - lista de endpoints permitidos)
        allowed_endpoints = [
            "/v2/tabela/alunos",
            "/v2/tabela/cursos",
            "/v2/tabela/disciplinas",
            "/v2/tabela/turmas",
            "/v2/tabela/docente",
            "/v2/tabela/matriculas",
            "/v2/tabela/curriculos",
            "/v2/tabela/grades",
            "/v2/tabela/coordenacao",
            "/v2/tabela/turma-docente",
        ]
        
        # Verificar se endpoint começa com algum permitido
        if not any(endpoint.startswith(allowed) for allowed in allowed_endpoints):
            logger.warning(f"Endpoint não reconhecido: {endpoint}")
            # Não bloqueia, apenas loga warning
        
        return True
    
    @staticmethod
    def get_lyceum_rate_limits() -> Dict[str, Any]:
        """
        Retorna limites de rate limiting para API Lyceum
        
        Para evitar sobrecarga na API externa
        """
        return {
            "max_requests_per_minute": 60,
            "max_requests_per_hour": 1000,
            "delay_between_requests": 0.1,  # segundos
            "max_concurrent_requests": 5,
        }
    
    @staticmethod
    def validate_api_credentials(config: Dict[str, Any]) -> bool:
        """
        Valida se as credenciais da API Lyceum estão configuradas
        
        Args:
            config: Configurações da aplicação
            
        Returns:
            True se credenciais válidas
            
        Raises:
            HTTPException: Se credenciais não estiverem configuradas
        """
        required_fields = [
            "LYCEUM_API_BASE_URL",
            "LYCEUM_API_USERNAME", 
            "LYCEUM_API_PASSWORD"
        ]
        
        missing_fields = []
        
        for field in required_fields:
            value = config.get(field, "").strip()
            if not value:
                missing_fields.append(field)
        
        if missing_fields:
            logger.error(f"Credenciais da API Lyceum não configuradas: {missing_fields}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Credenciais da API Lyceum não configuradas: {', '.join(missing_fields)}"
            )
        
        return True