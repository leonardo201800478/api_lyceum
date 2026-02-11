# app/core/security.py
import logging
from typing import Dict, Any
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class APISecurity:
    @staticmethod
    def validate_api_credentials(config: Dict[str, Any]) -> bool:
        required_fields = [
            "LYCEUM_API_BASE_URL",
            "LYCEUM_API_USERNAME",
            "LYCEUM_API_PASSWORD",
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

    @staticmethod
    def validate_lyceum_request(method: str, endpoint: str) -> bool:
        if method.upper() != "GET":
            logger.error(f"Tentativa de uso de método {method} na API Lyceum (não permitido)")
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail=f"Método {method} não é permitido para API Lyceum (apenas GET)"
            )
        return True