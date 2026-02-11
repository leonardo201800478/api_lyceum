# tests/conftest.py
import sys
import os
from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def event_loop():
    """Cria um loop para toda a sessão de testes (pytest-asyncio)."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Adiciona o diretório raiz ao sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Importa as configurações e SOBRESCREVE as URLs do banco
from app.core.config import settings

# Atribuição direta (agora funcionará graças aos setters)
settings.DATABASE_URL = "sqlite+aiosqlite:///./test.db"
settings.SYNC_DATABASE_URL = "sqlite:///./test.db"

# Opcional: define variáveis de ambiente para outros componentes (ex: Redis)
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_PASSWORD"] = ""

# Agora podemos importar o app e outros módulos com segurança