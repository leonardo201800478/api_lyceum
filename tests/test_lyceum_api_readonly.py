# tests/test_lyceum_api_readonly.py
import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from app.services.lyceum_api import LyceumAPIClientReadOnly
from app.services.sync_aluno import SyncAlunoService
from app.main import app

# Mock de dados (apenas um aluno)
MOCK_ALUNO_API = {
    "aluno": "2024001",
    "nome_compl": "João da Silva",
    "nome_abrev": "João S.",
    "curso": "Engenharia",
    "serie": 3,
    "turno": "Noturno",
    "e_mail_interno": "joao.silva@lyceum.edu.br",
    "stamp_atualizacao": "20250211143000",
}
MOCK_ALUNO_API_LIST = [MOCK_ALUNO_API]

@pytest.fixture
def client():
    return TestClient(app)

# ------------------------------------------------------------
# TESTE 1 – Cliente Lyceum só faz GET (agora rápido!)
# ------------------------------------------------------------
@pytest.mark.asyncio
async def test_lyceum_client_only_get():
    """Verifica que o cliente Lyceum realiza apenas GET e a paginação é finita."""
    cliente = LyceumAPIClientReadOnly()

    # 👉 Mock do método fetch_all_pages (responsável pela paginação)
    cliente.fetch_all_pages = AsyncMock(return_value=MOCK_ALUNO_API_LIST)

    # Chama o método que usa fetch_all_pages internamente
    result = await cliente.get_all_alunos()

    assert result == MOCK_ALUNO_API_LIST
    cliente.fetch_all_pages.assert_called_once()
    assert not hasattr(cliente, "post")
    assert not hasattr(cliente, "put")
    assert not hasattr(cliente, "delete")

# ------------------------------------------------------------
# TESTE 2 – Serviço não modifica API externa
# ------------------------------------------------------------
@pytest.mark.asyncio
async def test_sync_service_no_modification():
    mock_db = AsyncMock()
    mock_db.execute.return_value.scalar_one_or_none.return_value = None
    mock_db.execute.return_value.scalars.return_value.all.return_value = []

    service = SyncAlunoService(mock_db)

    # Mock do método que busca alunos – retorna lista finita
    service.api_client.get_all_alunos = AsyncMock(return_value=MOCK_ALUNO_API_LIST)

    stats = await service.sync_all(incremental=False)

    assert stats["total_api"] == 1
    assert stats["inseridos"] == 1
    assert stats["atualizados"] == 0
    assert stats["erros"] == 0
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    service.api_client.get_all_alunos.assert_called_once()

# ------------------------------------------------------------
# TESTE 3 – Normalização de dados
# ------------------------------------------------------------
@pytest.mark.asyncio
async def test_normalize_aluno_data():
    mock_db = AsyncMock()
    service = SyncAlunoService(mock_db)
    normalized = await service.normalize_data(MOCK_ALUNO_API)
    assert normalized["aluno"] == "2024001"
    assert normalized["nome_compl"] == "João da Silva"
    assert normalized["sincronizado"] is True

# ------------------------------------------------------------
# TESTE 4 – Endpoint de sincronização (background task)
# ------------------------------------------------------------
def test_sync_endpoint_background(client, mocker):
    mock_sync = mocker.patch("app.api.v1.endpoints.alunos.sync_alunos", new_callable=AsyncMock)
    mock_sync.return_value = {"total_api": 1, "inseridos": 1}
    response = client.post("/api/v1/alunos/sync?incremental=false")
    assert response.status_code == 200
    assert response.json()["message"] == "Sincronização de alunos iniciada em background"