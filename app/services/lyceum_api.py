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
        self.page_size = settings.LYCEUM_API_PAGE_SIZE  # Geralmente 100
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
                logger.debug(f"GET → {url} | params: {params}")
                response = await client.get(
                    url=url,
                    params=params,
                    auth=self.auth,
                    headers={"Accept": "application/json"}
                )
                
                if response.status_code != 200:
                    logger.error(f"HTTP {response.status_code} → {url}")
                    if response.status_code == 401:
                        logger.error("❌ Credenciais inválidas para API Lyceum")
                    elif response.status_code == 404:
                        logger.error(f"❌ Endpoint não encontrado: {endpoint}")
                    else:
                        logger.error(f"❌ Resposta: {response.text[:200]}...")
                    return None
                
                return response.json()
                
            except httpx.TimeoutException:
                logger.error(f"⏱️ Timeout na requisição GET → {url}")
                return None
            except httpx.RequestError as e:
                logger.error(f"❌ Erro na requisição GET → {url}: {e}")
                return None
    
    async def get_paginated_data(
        self,
        endpoint: str,
        custom_params: Optional[Dict] = None,
        page_start: int = 0
    ) -> List[Dict]:
        """
        Obtém TODOS os dados de um endpoint paginado
        
        Args:
            endpoint: Endpoint da API (ex: "/v2/tabela/alunos")
            custom_params: Parâmetros adicionais para a requisição
            page_start: Página inicial (padrão: 0)
            
        Returns:
            Lista com todos os dados obtidos
        """
        all_data = []
        page = page_start
        
        logger.info(f"🔄 Iniciando paginação em {endpoint}")
        
        while True:
            # Parâmetros base para paginação
            params = {
                "page": page,
                "size": self.page_size
            }
            
            # Adicionar parâmetros personalizados se fornecidos
            if custom_params:
                params.update(custom_params)
            
            logger.info(f"📄 Buscando página {page} (size={self.page_size})...")
            
            data = await self._make_get_request(endpoint, params=params)
            
            # Verificar se houve erro
            if data is None:
                logger.warning(f"⚠️ Página {page} retornou None, interrompendo paginação")
                break
            
            # Processar resposta baseada no formato esperado
            items = []
            
            # Formato 1: {"data": [...]}
            if isinstance(data, dict) and 'data' in data:
                items = data['data']
                if not isinstance(items, list):
                    logger.error(f"❌ 'data' não é uma lista: {type(items)}")
                    break
            
            # Formato 2: lista direta
            elif isinstance(data, list):
                items = data
            
            # Formato desconhecido
            else:
                logger.error(f"❌ Formato de resposta inesperado: {type(data)}")
                logger.debug(f"Conteúdo: {str(data)[:200]}...")
                break
            
            # Verificar se a página está vazia (fim da paginação)
            if len(items) == 0:
                logger.info(f"✅ Página {page} vazia - fim da paginação")
                break
            
            # Adicionar itens ao resultado
            all_data.extend(items)
            logger.info(f"📊 Página {page}: {len(items)} registros (total: {len(all_data)})")
            
            # Incrementar página
            page += 1
            
            # Delay para não sobrecarregar a API
            await asyncio.sleep(self.delay)
        
        logger.info(f"🎉 Paginação completa: {len(all_data)} registros obtidos")
        return all_data
    
    async def get_alunos_paginated(self, page: int = 0) -> Optional[Dict]:
        """Obtém uma página específica de alunos da API"""
        params = {
            "page": page,
            "size": self.page_size
        }
        return await self._make_get_request("/v2/tabela/alunos", params=params)
    
    async def get_all_alunos(self) -> List[Dict]:
        """Obtém TODOS os alunos paginando automaticamente"""
        return await self.get_paginated_data("/v2/tabela/alunos")
    
    async def get_aluno_by_matricula(self, matricula: str) -> Optional[Dict]:
        """Obtém um aluno específico por matrícula"""
        params = {"pk[aluno]": matricula}
        data = await self.get_paginated_data("/v2/tabela/alunos", custom_params=params)
        
        if data and len(data) > 0:
            return data[0]
        
        return None
    
    # Métodos para outras entidades (com paginação completa)
    async def get_all_cursos(self) -> List[Dict]:
        """Obtém TODOS os cursos"""
        return await self.get_paginated_data("/v2/tabela/cursos")
    
    async def get_all_disciplinas(self) -> List[Dict]:
        """Obtém TODAS as disciplinas"""
        return await self.get_paginated_data("/v2/tabela/disciplinas")
    
    async def get_all_turmas(
        self, 
        ano: Optional[int] = None, 
        semestre: Optional[int] = None
    ) -> List[Dict]:
        """Obtém TODAS as turmas com filtros opcionais"""
        params = {}
        if ano is not None:
            params["ano"] = ano
        if semestre is not None:
            params["semestre"] = semestre
        
        return await self.get_paginated_data("/v2/tabela/turmas", custom_params=params)
    
    async def get_all_docentes(self) -> List[Dict]:
        """Obtém TODOS os docentes"""
        return await self.get_paginated_data("/v2/tabela/docente")
    
    async def get_all_matriculas(
        self,
        ano: Optional[int] = None,
        semestre: Optional[int] = None
    ) -> List[Dict]:
        """Obtém TODAS as matrículas com filtros opcionais"""
        params = {}
        if ano is not None:
            params["ano"] = ano
        if semestre is not None:
            params["semestre"] = semestre
        
        return await self.get_paginated_data("/v2/tabela/matriculas", custom_params=params)
    
    async def get_all_curriculos(self) -> List[Dict]:
        """Obtém TODOS os currículos"""
        return await self.get_paginated_data("/v2/tabela/curriculos")
    
    async def get_all_grades(self) -> List[Dict]:
        """Obtém TODAS as grades"""
        return await self.get_paginated_data("/v2/tabela/grades")
    
    async def get_all_coordenacao(
        self,
        ano: Optional[int] = None,
        semestre: Optional[int] = None
    ) -> List[Dict]:
        """Obtém TODAS as coordenações com filtros opcionais"""
        params = {}
        if ano is not None:
            params["ano"] = ano
        if semestre is not None:
            params["semestre"] = semestre
        
        return await self.get_paginated_data("/v2/tabela/coordenacao", custom_params=params)
    
    async def get_all_turma_docente(
        self,
        ano: Optional[int] = None,
        semestre: Optional[int] = None
    ) -> List[Dict]:
        """Obtém TODAS as turma-docente com filtros opcionais"""
        params = {}
        if ano is not None:
            params["ano"] = ano
        if semestre is not None:
            params["semestre"] = semestre
        
        return await self.get_paginated_data("/v2/tabela/turma-docente", custom_params=params)
    
    # Métodos para obter UMA página (mantidos para compatibilidade)
    async def get_cursos_page(self, page: int = 0) -> Optional[Dict]:
        """Obtém UMA página de cursos"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/cursos", params=params)
    
    async def get_disciplinas_page(self, page: int = 0) -> Optional[Dict]:
        """Obtém UMA página de disciplinas"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/disciplinas", params=params)
    
    async def get_turmas_page(self, page: int = 0) -> Optional[Dict]:
        """Obtém UMA página de turmas"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/turmas", params=params)
    
    async def get_docentes_page(self, page: int = 0) -> Optional[Dict]:
        """Obtém UMA página de docentes"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/docente", params=params)
    
    async def get_matriculas_page(self, page: int = 0) -> Optional[Dict]:
        """Obtém UMA página de matrículas"""
        params = {"page": page, "size": self.page_size}
        return await self._make_get_request("/v2/tabela/matriculas", params=params)
    
    # Método de verificação de saúde da API Lyceum
    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica se a API Lyceum está respondendo
        
        Returns:
            Dict com status da API Lyceum
        """
        try:
            # Tenta uma requisição simples para a página 0
            data = await self._make_get_request(
                "/v2/tabela/alunos", 
                params={"page": 0, "size": 1}
            )
            
            if data is not None:
                return {
                    "status": "online",
                    "message": "API Lyceum respondendo normalmente",
                    "test_page": 0,
                    "test_size": 1,
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
        logger.info("🔒 Cliente Lyceum READ-ONLY inicializado (apenas GET permitido)")
    
    # Método genérico bloqueado para forçar uso apenas de métodos GET específicos
    async def _make_request(self, method: str, **kwargs):
        """Método bloqueado - usar apenas métodos GET específicos"""
        raise NotImplementedError(
            "❌ Este cliente é READ-ONLY. Use apenas métodos GET específicos."
        )
    
    # Dicionário de endpoints disponíveis
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
    
    async def get_endpoint(
        self, 
        endpoint_name: str, 
        params: Optional[Dict] = None,
        all_pages: bool = False
    ) -> Any:
        """
        Método genérico para endpoints GET apenas
        
        Args:
            endpoint_name: Nome do endpoint (deve estar em GET_ENDPOINTS)
            params: Parâmetros de query string
            all_pages: Se True, obtém TODAS as páginas
            
        Returns:
            Dados da API (List[Dict] se all_pages=True, Dict se uma página)
            
        Raises:
            ValueError: Se endpoint_name não for válido
        """
        if endpoint_name not in self.GET_ENDPOINTS:
            raise ValueError(
                f"❌ Endpoint '{endpoint_name}' não é válido. "
                f"Endpoints válidos: {list(self.GET_ENDPOINTS.keys())}"
            )
        
        endpoint = self.GET_ENDPOINTS[endpoint_name]
        
        if all_pages:
            # Obtém todas as páginas
            return await self.get_paginated_data(endpoint, custom_params=params)
        else:
            # Obtém apenas uma página (padrão página 0)
            if params is None:
                params = {"page": 0, "size": self.page_size}
            elif "page" not in params:
                params["page"] = 0
            if "size" not in params:
                params["size"] = self.page_size
            
            return await self._make_get_request(endpoint, params=params)