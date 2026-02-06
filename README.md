README.md
markdown
# 🚀 API Lyceum Sync - FastAPI

API moderna para sincronização de dados acadêmicos do Lyceum, construída com FastAPI e PostgreSQL.

## ✨ Funcionalidades

- ✅ **API RESTful** com FastAPI
- ✅ **Documentação automática** (Swagger/ReDoc)
- ✅ **Dockerização completa** com PostgreSQL e Redis
- ✅ **Paginação e ordenação** avançadas
- ✅ **Validação de dados** com Pydantic v2
- ✅ **ORM** com SQLAlchemy 2.0
- ✅ **CORS configurado**
- ✅ **Health check** para monitoramento
- ✅ **Sincronização em background**
- ✅ **Filtros e busca** nos endpoints
- ✅ **Migrations** com Alembic

## 🚀 Começando

### Pré-requisitos

- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)
- Git

### Configuração

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/api-lyceum-fastapi.git
   cd api-lyceum-fastapi
Configure as variáveis de ambiente

bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
Inicie com Docker Compose

bash
docker-compose -f docker/docker-compose.yml up --build
Acesse a aplicação

API: http://localhost:8000

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

pgAdmin: http://localhost:5050 (admin@lyceum.com / admin123)

📚 Endpoints da API
Health Check
GET /api/v1/health - Status da aplicação

GET /api/v1/health/ping - Ping simples

Alunos
GET /api/v1/alunos - Listar alunos (com paginação e filtros)

GET /api/v1/alunos/{matricula} - Detalhes de um aluno

GET /api/v1/alunos/stats/summary - Estatísticas dos alunos

GET /api/v1/alunos/curso/{curso} - Alunos por curso

GET /api/v1/alunos/serie/{serie} - Alunos por série

Sincronização
POST /api/v1/sync/alunos - Iniciar sincronização

GET /api/v1/sync/status - Status da sincronização

🔧 Desenvolvimento
Ambiente local sem Docker
Crie um ambiente virtual

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instale dependências

bash
pip install -r requirements.txt
Configure o banco de dados

bash
# Instale PostgreSQL localmente ou use Docker
docker run --name lyceum-db -e POSTGRES_PASSWORD=lyceum_password -p 5432:5432 -d postgres:15

# Execute migrations
alembic upgrade head
Inicie a aplicação

bash
uvicorn app.main:app --reload
Migrations
bash
# Criar nova migration
alembic revision --autogenerate -m "descrição da migration"

# Aplicar migrations
alembic upgrade head

# Reverter migration
alembic downgrade -1
📊 Estrutura do Projeto
text
api-lyceum-fastapi/
├── app/
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── core/               # Configurações e conexões
│   ├── api/                # Endpoints e rotas
│   ├── models/             # Modelos SQLAlchemy
│   ├── schemas/            # Schemas Pydantic
│   ├── services/           # Lógica de negócio
│   ├── crud/               # Operações de banco
│   └── utils/              # Utilitários
├── migrations/             # Migrations do banco
├── docker/                # Configurações Docker
├── tests/                 # Testes automatizados
└── scripts/              # Scripts auxiliares
🔒 Segurança
CORS configurado

Validação de dados com Pydantic

Pronto para autenticação JWT (implementação pendente)

Variáveis sensíveis em .env

🧪 Testes
bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar testes
pytest tests/
📈 Monitoramento
Health checks automáticos

Logs estruturados

Métricas básicas do sistema

Pronto para integração com Prometheus/Grafana

🤝 Contribuição
Fork o projeto

Crie uma branch (git checkout -b feature/nova-funcionalidade)

Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')

Push para a branch (git push origin feature/nova-funcionalidade)

Abra um Pull Request

📄 Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

👨‍💻 Autores
Seu Nome - @seu-usuario

🙏 Agradecimentos
FastAPI

SQLAlchemy

PostgreSQL

Docker