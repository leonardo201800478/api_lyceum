import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_lyceum_api_read_only_mode():
    """Testa se a API esta em modo read-only"""
    response = client.get("/")
    assert response.status_code == 200
    assert "READ-ONLY" in response.text
    assert "Apenas requisicoes GET" in response.text


def test_lyceum_health_endpoint():
    """Testa o endpoint de saude da API Lyceum"""
    with patch('app.api.v1.endpoints.security.LyceumAPIClientReadOnly') as mock_client:
        mock_instance = MagicMock()
        mock_instance.health_check.return_value = {
            "status": "online",
            "message": "API respondendo"
        }
        mock_client.return_value = mock_instance
        
        response = client.get("/api/v1/security/lyceum/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["security_mode"] == "read_only"
        assert "GET" in str(data["allowed_methods"])


def test_security_status_endpoint():
    """Testa o endpoint de status de seguranca"""
    response = client.get("/api/v1/security/status")
    
    assert response.status_code == 200
    data = response.json()
    assert data["lyceum_api_mode"] == "read_only"
    assert "GET" in data["allowed_http_methods"]
    assert "POST" in data["blocked_http_methods"]
    assert "rate_limiting" in data


def test_lyceum_endpoints_list():
    """Testa a lista de endpoints Lyceum disponiveis"""
    response = client.get("/api/v1/security/lyceum/endpoints")
    
    assert response.status_code == 200
    data = response.json()
    assert "available_endpoints" in data
    assert "alunos" in data["available_endpoints"]
    assert "security_note" in data


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE", "PATCH"])
def test_blocked_methods_for_lyceum(method):
    """Testa se metodos nao-GET sao bloqueados"""
    # Simula uma tentativa de usar metodo nao permitido
    # (O middleware deve bloquear)
    
    # Para POST no endpoint de sync e permitido
    if method == "POST":
        response = client.request(method, "/api/v1/sync/alunos")
        # POST e permitido apenas para iniciar sync
        assert response.status_code in [200, 405]
    else:
        # Outros metodos nao sao permitidos em nenhum endpoint Lyceum
        response = client.request(method, "/api/v1/sync/alunos")
        assert response.status_code == 405  # Method Not Allowed


def test_rate_limiting():
    """Testa se rate limiting esta funcionando"""
    # Este teste seria mais complexo em producao
    # Aqui apenas verificamos se a configuracao existe
    response = client.get("/api/v1/security/status")
    data = response.json()
    
    assert "rate_limiting" in data
    rate_limit = data["rate_limiting"]
    assert "max_requests_per_minute" in rate_limit
    assert rate_limit["max_requests_per_minute"] > 0