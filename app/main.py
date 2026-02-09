from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.core.database import engine
from app.api.v1.api import api_router
from app.middleware.security import LyceumAPISecurityMiddleware, RateLimitMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager para eventos de startup/shutdown"""
    logger.info("🚀 Iniciando API Lyceum Sync (MODO READ-ONLY)")
    logger.info("⚠  AVISO: Apenas metodos GET sao permitidos para API Lyceum")
    yield
    logger.info("🛑 Encerrando API Lyceum Sync")


# Criar aplicacao FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME + " (READ-ONLY)",
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    description="""
    ## 🔒 API Lyceum Sync - Modo Read-Only
    
    **IMPORTANTE:** Esta API opera em modo READ-ONLY para a API Lyceum externa.
    
    ### Restricoes de Seguranca:
    - ✅ Apenas requisicoes GET sao permitidas para API Lyceum
    - ❌ Metodos POST, PUT, DELETE sao bloqueados
    - ✅ Rate limiting para evitar sobrecarga
    - ✅ Validacao de credenciais
    
    ### Endpoints Disponiveis:
    - `/api/v1/alunos` - Consulta alunos sincronizados
    - `/api/v1/sync/alunos` - Inicia sincronizacao (usa apenas GET na API Lyceum)
    - `/api/v1/health` - Verifica saude do sistema
    """,
)

# Adicionar middlewares de seguranca
app.add_middleware(LyceumAPISecurityMiddleware)
app.add_middleware(RateLimitMiddleware)

# Configurar CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST"],  # POST apenas para endpoints internos
        allow_headers=["*"],
    )

# Incluir rotas da API
app.include_router(api_router, prefix=settings.API_V1_STR)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME + " (READ-ONLY)",
        version=settings.APP_VERSION,
        description=app.description,
        routes=app.routes,
    )
    
    # Adicionar nota de seguranca
    openapi_schema["info"]["x-security-note"] = "API Lyceum operates in READ-ONLY mode. Only GET methods are allowed for external API calls."
    
    # Adicionar tags de seguranca
    if "tags" not in openapi_schema:
        openapi_schema["tags"] = []
    
    openapi_schema["tags"].append({
        "name": "security",
        "description": "Endpoints relacionados à seguranca e validacoes"
    })
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """Pagina inicial com informacoes de seguranca"""
    security_html = """
    <div class="security-note">
        <h3>🔒 Modo Read-Only</h3>
        <p>Esta API opera em modo <strong>READ-ONLY</strong> para a API Lyceum.</p>
        <ul>
            <li>✅ Apenas requisicoes GET sao permitidas</li>
            <li>❌ POST, PUT, DELETE sao bloqueados</li>
            <li>✅ Rate limiting ativo</li>
            <li>✅ Validacao de credenciais</li>
        </ul>
    </div>
    """
    
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>API Lyceum Sync (READ-ONLY)</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    border-bottom: 2px solid #4CAF50;
                    padding-bottom: 10px;
                }}
                .security-note {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .security-note h3 {{
                    color: #856404;
                    margin-top: 0;
                }}
                .links {{
                    margin-top: 30px;
                }}
                .link {{
                    display: block;
                    padding: 10px 15px;
                    margin: 10px 0;
                    background: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background 0.3s;
                }}
                .link:hover {{
                    background: #45a049;
                }}
                .link.docs {{
                    background: #2196F3;
                }}
                .link.docs:hover {{
                    background: #1976D2;
                }}
                .link.redoc {{
                    background: #FF9800;
                }}
                .link.redoc:hover {{
                    background: #F57C00;
                }}
                .warning {{
                    color: #856404;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔒 API Lyceum Sync (READ-ONLY)</h1>
                <p>Sistema de sincronizacao de dados acadêmicos do Lyceum</p>
                <p><strong>Versao:</strong> {settings.APP_VERSION}</p>
                <p><strong>Ambiente:</strong> {settings.ENVIRONMENT}</p>
                <p class="warning">⚠ MODE: READ-ONLY (Apenas GET para API Lyceum)</p>
                
                {security_html}
                
                <div class="links">
                    <a href="/docs" class="link docs">📚 Swagger UI Documentation</a>
                    <a href="/redoc" class="link redoc">📖 ReDoc Documentation</a>
                    <a href="/api/v1/health" class="link">🔍 Health Check</a>
                    <a href="/api/v1/alunos" class="link">👥 Listar Alunos</a>
                    <a href="/api/v1/sync/alunos" class="link">🔄 Sincronizar Alunos</a>
                </div>
            </div>
        </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )