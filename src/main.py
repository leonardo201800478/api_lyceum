from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.alunos import router as alunos_router

app = FastAPI(
    title="API Lyceum - Alunos",
    description="API para consulta de dados de alunos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(alunos_router)

@app.get("/")
async def root():
    """Endpoint raiz com informações da API."""
    return {
        "message": "API Lyceum - Alunos",
        "version": "1.0.0",
        "description": "API para consulta de dados de alunos",
        "endpoints": {
            "listar_alunos": "/alunos",
            "aluno_por_id": "/alunos/{id}",
            "aluno_por_cpf": "/alunos/cpf/{cpf}",
            "aluno_por_matricula": "/alunos/matricula/{matricula}",
            "aluno_por_email": "/alunos/email/{email}",
            "documentacao": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check para monitoramento."""
    return {
        "status": "healthy",
        "service": "api-lyceum",
        "version": "1.0.0"
    }
