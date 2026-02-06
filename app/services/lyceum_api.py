import httpx
import asyncio
from typing import List, Dict, Optional, Any
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class LyceumAPIClient:
    """Cliente assíncrono para API Lyceum - APENAS GET"""
    
    def __init__(self):
        self.base_url = settings.LYCEUM_API_BASE_URL.rstrip("/")
        self.auth = httpx.BasicAuth(
            username=settings.LYCEUM_API_USERNAME,
            password=settings.LYCEUM_API_PASSWORD,
        )
        self.timeout = settings.LYCEUM_API_TIMEOUT
        self.page_size = settings.LYCEUM_API_PAGE_SIZE
        self.delay = settings.LYCEUM_API_DELAY
        
    async def _make_get_request(
        self,
        endpoint: str,
        params: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Faz uma requisição HTTP GET APENAS
        
        Args:
            endpoint: Endpoint da API
            params: Parâmetros de query string
            
        Returns:
            Resposta JSON ou None em caso de erro
        """
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    url=url,
                    params=params,
                    auth=self.auth,
                    headers={"Accept": "application/json"}
                )
                
                if response.status_code != 200:
                    logger.error(f"HTTP {response.status_code} → {url}")
                    logger.error(f"Resposta: {response.text[:200]}")
                    return None
                
                return response.json()
                
            except httpx.TimeoutException:
                logger.error(f"Timeout na requisição GET → {url}")
                return None
            except httpx.RequestError as e:
                logger.error(f"Erro na requisição GET → {url}: {e}")
                return None
    
    async def get_alunos_paginated(self, page: int = 0) -> Optional[Dict]:
        """Obtém uma página de alunos da API (GET apenas)"""
        params = {
            "page": page,
            "size": self.page_size
        }
        return await self._make_get_request("/v2/tabela/alunos", params=params)
    
    async def get_all_alunos(self) -> List[Dict]:
        """Obtém todos os alunos paginando automaticamente (GET apenas)"""
        all_alunos = []
        page = 0
        
        logger.info("Iniciando paginação de alunos (método GET)...")
        
        while True:
            logger.info(f"Buscando página {page} (GET)...")
            
            data = await self.get_alunos_paginated(page)
            
            if not data:
                logger.warning(f"Página {page} retornou None, interrompendo...")
                break
            
            if isinstance(data, dict) and 'data' in data:
                items = data['data']
                if not isinstance(items, list):
                    logger.error(f"'data' não é uma lista: {type(items)}")
                    break
                
                if len(items) == 0:
                    logger.info(f"Página {page} vazia, fim da paginação")
                    break
                
                all_alunos.extend(items)
                logger.info(f"Página {page}: {len(items)} registros (total: {len(all_alunos)})")
                
            elif isinstance(data, list):
                if len(data) == 0:
                    logger.info(f"Página {page} vazia, fim da paginação")
                    break
                
                all_alunos.extend(data)
                logger.info(f"Página {page}: {len(data)} registros (total: {len(all_alunos)})")
            else:
                logger.error(f"Formato inesperado: {type(data)}")
                break
            
            page += 1
            
            # Delay para não sobrecarregar a API
            await asyncio.sleep(self.delay)
        
        logger.info(f"Paginação completa: {len(all_alunos)} alunos obtidos via GET")
        return all_alunos
    
    async def get_aluno_by_matricula(self, matricula: str) -> Optional[Dict]:
        """Obtém um aluno específico por matrícula (GET apenas)"""
        params = {"pk[aluno]": matricula}
        data = await self._make_get_request("/v2/tabela/alunos", params=params)
        
        if data and isinstance(data, dict) and 'data' in data:
            items = data['data']
            if isinstance(items, list) and len(items) > 0:
                return items[0]
        
        return None
    
    # Métodos adicionais SOMENTE GET para outras entidades
    async def get_cursos(self, page: int = 0) -> Optional[Dict]:
        """Obtém cursos da API (GET apenas)"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/cursos", params=params)
    
    async def get_disciplinas(self, page: int = 0) -> Optional[Dict]:
        """Obtém disciplinas da API (GET apenas)"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/disciplinas", params=params)
    
    async def get_turmas(self, page: int = 0) -> Optional[Dict]:
        """Obtém turmas da API (GET apenas)"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/turmas", params=params)
    
    async def get_docentes(self, page: int = 0) -> Optional[Dict]:
        """Obtém docentes da API (GET apenas)"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/docente", params=params)
    
    async def get_matriculas(self, page: int = 0) -> Optional[Dict]:
        """Obtém matrículas da API (GET apenas)"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/matriculas", params=params)
    
    # Método de verificação de saúde da API Lyceum (GET apenas)
    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica se a API Lyceum está respondendo (GET apenas)
        
        Returns:
            Dict com status da API Lyceum
        """
        try:
            # Tenta uma requisição simples
            data = await self._make_get_request("/v2/tabela/alunos", params={"page": 0, "size": 1})
            
            if data is not None:
                return {
                    "status": "online",
                    "message": "API Lyceum respondendo normalmente",
                    "timestamp": asyncio.get_event_loop().time()
                }
            else:
                return {
                    "status": "offline",
                    "message": "API Lyceum não respondeu",
                    "timestamp": asyncio.get_event_loop().time()
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao verificar API Lyceum: {str(e)}",
                "timestamp": asyncio.get_event_loop().time()
            }


class LyceumAPIClientReadOnly(LyceumAPIClient):
    """
    Cliente Lyceum com validação explícita para garantir que é READ-ONLY
    
    Esta classe herda do LyceumAPIClient mas adiciona verificações
    explícitas para garantir que apenas GET seja usado
    """
    
    def __init__(self):
        super().__init__()
        logger.info("Cliente Lyceum READ-ONLY inicializado (apenas GET permitido)")
    
    # Sobrescrever qualquer método que não seja GET para lançar exceção
    async def _make_request(self, method: str, **kwargs):
        """Método bloqueado - usar apenas _make_get_request"""
        raise NotImplementedError(
            "Este cliente é READ-ONLY. Use apenas métodos GET específicos."
        )
    
    # Métodos explícitos apenas GET
    GET_ENDPOINTS = {
        "alunos": "/v2/tabela/alunos",
        "cursos": "/v2/tabela/cursos",
        "disciplinas": "/v2/tabela/disciplinas",
        "turmas": "/v2/tabela/turmas",
        "docentes": "/v2/tabela/docente",
        "matriculas": "/v2/tabela/matriculas",
        "curriculos": "/v2/tabela/curriculos",
        "grades": "/v2/tabela/grades",
        "coordenacao": "/v2/tabela/coordenacao",
        "turma-docente": "/v2/tabela/turma-docente",
    }
    
    async def get_endpoint(self, endpoint_name: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Método genérico para endpoints GET apenas
        
        Args:
            endpoint_name: Nome do endpoint (deve estar em GET_ENDPOINTS)
            params: Parâmetros de query string
            
        Returns:
            Dados da API ou None
            
        Raises:
            ValueError: Se endpoint_name não for válido
        """
        if endpoint_name not in self.GET_ENDPOINTS:
            raise ValueError(
                f"Endpoint '{endpoint_name}' não é válido. "
                f"Endpoints válidos: {list(self.GET_ENDPOINTS.keys())}"
            )
        
        endpoint = self.GET_ENDPOINTS[endpoint_name]
        return await self._make_get_request(endpoint, params=params)