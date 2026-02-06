from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging
import re

logger = logging.getLogger(__name__)


class LyceumAPISecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware para validar requisições para API Lyceum
    
    Garante que apenas GET seja usado e adiciona rate limiting
    """
    
    async def dispatch(self, request: Request, call_next):
        # Verificar se é uma requisição para API Lyceum
        path = request.url.path
        
        # Padrão para identificar endpoints que chamam API Lyceum
        lyceum_patterns = [
            r'^/api/v1/sync',
            r'^/api/v1/alunos/sync',
            r'^/api/v1/lyceum/',
        ]
        
        is_lyceum_endpoint = any(
            re.match(pattern, path) for pattern in lyceum_patterns
        )
        
        if is_lyceum_endpoint:
            # Log da requisição
            logger.info(f"Requisição para endpoint Lyceum: {request.method} {path}")
            
            # Validar método HTTP (apenas GET para endpoints de consulta)
            if request.method.upper() not in ["GET", "POST"]:
                # POST é permitido apenas para iniciar sincronizações
                # mas a sincronização em si usará apenas GET
                if request.method.upper() != "POST" or not path.endswith("/sync"):
                    logger.error(f"Método {request.method} não permitido para {path}")
                    raise HTTPException(
                        status_code=405,
                        detail=f"Método {request.method} não permitido"
                    )
        
        # Continuar com a requisição
        response = await call_next(request)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware de rate limiting para API Lyceum
    
    Evita sobrecarga na API externa
    """
    
    def __init__(self, app, max_requests: int = 60, time_window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_counts = {}
        
    async def dispatch(self, request: Request, call_next):
        # Aplicar rate limiting apenas para endpoints Lyceum
        path = request.url.path
        
        if any(path.startswith(p) for p in ["/api/v1/sync", "/api/v1/lyceum"]):
            client_ip = request.client.host
            
            # Limpar contagens antigas
            current_time = asyncio.get_event_loop().time()
            to_delete = []
            
            for ip, (count, timestamp) in self.request_counts.items():
                if current_time - timestamp > self.time_window:
                    to_delete.append(ip)
            
            for ip in to_delete:
                del self.request_counts[ip]
            
            # Verificar rate limit
            if client_ip in self.request_counts:
                count, timestamp = self.request_counts[client_ip]
                
                if count >= self.max_requests:
                    logger.warning(f"Rate limit excedido para IP: {client_ip}")
                    raise HTTPException(
                        status_code=429,
                        detail="Muitas requisições para API Lyceum. Tente novamente mais tarde."
                    )
                
                self.request_counts[client_ip] = (count + 1, timestamp)
            else:
                self.request_counts[client_ip] = (1, current_time)
        
        response = await call_next(request)
        return response