# app/services/lyceum_api.py
import httpx
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class LyceumAPIClient:
    """Cliente assíncrono para API Lyceum – APENAS GET com paginação automática."""

    ENDPOINTS = {
        "alunos": "/v2/tabela/alunos",
        "cursos": "/v2/tabela/cursos",
        "disciplinas": "/v2/tabela/disciplinas",
        "turmas": "/v2/tabela/turmas",
        "docentes": "/v2/tabela/docente",
        "matriculas": "/v2/tabela/matriculas",
        "curriculos": "/v2/tabela/curriculos",
        "grades": "/v2/tabela/grades",
        "coordenacao": "/v2/tabela/coordenacao",
        "turma_docente": "/v2/tabela/turma-docente",
    }

    def __init__(self):
        self.base_url = settings.LYCEUM_API_BASE_URL.rstrip("/")
        self.auth = httpx.BasicAuth(
            username=settings.LYCEUM_API_USERNAME,
            password=settings.LYCEUM_API_PASSWORD,
        )
        self.timeout = settings.LYCEUM_API_TIMEOUT
        self.page_size = settings.LYCEUM_API_PAGE_SIZE
        self.delay = settings.LYCEUM_API_DELAY

    async def _make_get_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                logger.debug(f"GET → {url} | params={params}")
                resp = await client.get(url, params=params, auth=self.auth, headers={"Accept": "application/json"})
                if resp.status_code != 200:
                    logger.error(f"HTTP {resp.status_code} – {url}")
                    return None
                return resp.json()
            except httpx.TimeoutException:
                logger.error(f"Timeout – {url}")
                return None
            except Exception as e:
                logger.error(f"Erro na requisição GET – {url}: {e}")
                return None

    async def fetch_all_pages(
        self,
        endpoint: str,
        custom_params: Optional[Dict] = None,
        page_start: int = 0,
    ) -> List[Dict]:
        all_data = []
        page = page_start
        while True:
            params = {"page": page, "size": self.page_size}
            if custom_params:
                params.update(custom_params)

            data = await self._make_get_request(endpoint, params)
            if data is None:
                logger.warning(f"⚠️ Página {page} retornou erro – interrompendo")
                break

            items = []
            if isinstance(data, dict) and "data" in data:
                items = data["data"]
            elif isinstance(data, list):
                items = data
            else:
                logger.error(f"Formato de resposta inesperado: {type(data)}")
                break

            if not items:
                logger.info(f"✅ Página {page} vazia – fim da paginação")
                break

            all_data.extend(items)
            logger.info(f"📄 Página {page}: {len(items)} registros (total: {len(all_data)})")
            page += 1
            await asyncio.sleep(self.delay)

        return all_data

    async def get_all_alunos(self) -> List[Dict]:
        return await self.fetch_all_pages(self.ENDPOINTS["alunos"])

    async def get_all_cursos(self) -> List[Dict]:
        return await self.fetch_all_pages(self.ENDPOINTS["cursos"])

    # ... demais métodos get_all_* ...

    async def health_check(self) -> Dict[str, Any]:
        data = await self._make_get_request(self.ENDPOINTS["alunos"], params={"page": 0, "size": 1})
        if data is not None:
            return {"status": "online", "message": "API Lyceum respondendo", "timestamp": datetime.now().isoformat()}
        return {"status": "offline", "message": "API Lyceum não respondeu", "timestamp": datetime.now().isoformat()}

class LyceumAPIClientReadOnly(LyceumAPIClient):
    """Garantia de que apenas métodos GET são usados."""
    def __init__(self):
        super().__init__()
        logger.info("🔒 Cliente Lyceum READ-ONLY ativo (apenas GET)")