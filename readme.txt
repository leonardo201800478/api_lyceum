# API Lyceum

API para consulta de dados de alunos desenvolvida com FastAPI, PostgreSQL e Docker.

## 🚀 Visão Geral

A **API Lyceum** é uma API RESTful para consulta de dados de alunos com estrutura modular e preparada para integração com sistemas educacionais. A API oferece endpoints apenas para leitura (GET) com suporte a múltiplos filtros e paginação.

## 🎯 Funcionalidades

- ✅ Consulta de alunos com múltiplos filtros
- ✅ Busca por ID, CPF, matrícula ou email
- ✅ Paginação e ordenação
- ✅ Documentação automática (Swagger/ReDoc)
- ✅ Dockerização completa
- ✅ PostgreSQL como banco principal
- ✅ Health check para monitoramento
- ✅ CORS configurado
- ✅ Validação de dados com Pydantic
- ✅ ORM com SQLAlchemy

## 📋 Requisitos

- Docker e Docker Compose
- Python 3.11+
- PostgreSQL 15+

## 🏗️ Estrutura do Projeto

```
api_lyceum/
├── .env                    # Variáveis de ambiente
├── .env.example           # Exemplo de variáveis
├── docker-compose.yml     # Configuração Docker
├── requirements.txt       # Dependências Python
├── run.py                # Ponto de entrada da API
├── setup_complete.py     # Script de configuração
├── src/
│   ├── main.py           # Aplicação FastAPI
│   ├── core/
│   │   ├── config.py     # Configurações
│   │   └── database.py   # Conexão com banco
│   ├── models/
│   │   ├── base.py       # Modelo base
│   │   ├── aluno.py      # Modelo Aluno
│   │   └── instituicao.py # Modelo Instituição
│   ├── schemas/
│   │   └── aluno.py      # Schemas Pydantic
│   ├── api/
│   │   └── alunos.py     # Endpoints da API
│   └── repositories/
│       └── aluno_repository.py # Lógica de acesso a dados
└── scripts/
    └── init_db.py        # Inicialização do banco
```

## 🚀 Instalação Rápida

### Método 1: Com Docker (Recomendado)

```bash
# 1. Clone o projeto
git clone https://github.com/leonardo201800478/api_lyceum.git
cd api_lyceum

# 2. Configure o ambiente
cp .env.example .env

# 3. Inicie os containers
docker-compose up -d

# 4. Acesse a API
# Documentação: http://localhost:8000/docs
# Health check: http://localhost:8000/health
```

### Método 2: Local (Python + Docker PostgreSQL)

```bash
# 1. Clone e acesse o projeto
git clone https://github.com/leonardo201800478/api_lyceum.git
cd api_lyceum

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Inicie PostgreSQL no Docker
docker run -d --name lyceum_postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=lyceum_db \
  -p 5432:5432 \
  postgres:15-alpine

# 6. Configure o .env
cp .env.example .env

# 7. Inicialize o banco de dados
python scripts/init_db.py

# 8. Execute a API
python run.py
```

## 📦 Docker Compose

O `docker-compose.yml` configura dois serviços:

1. **PostgreSQL**: Banco de dados na porta 5432
2. **API**: Aplicação FastAPI na porta 8000

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: lyceum_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/lyceum_db
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# API Configuration
API_V1_STR=/
PROJECT_NAME=API Lyceum - Alunos

# Database Configuration
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lyceum_db
```

### Inicialização do Banco de Dados

O script `scripts/init_db.py` cria as tabelas e insere dados de exemplo:

```bash
python scripts/init_db.py
```

**Dados de exemplo incluídos:**
- 2 instituições (UFMG e PUC Minas)
- 3 alunos (João, Maria, Carlos)

## 📚 Endpoints da API

### 🔍 Listar Alunos
```
GET /alunos
```

**Parâmetros de consulta:**
- `pagina` (opcional): Número da página (padrão: 1)
- `limite` (opcional): Itens por página (padrão: 50, máximo: 200)
- `ativo` (opcional): Filtrar por status (true/false)
- `cpf` (opcional): Filtrar por CPF exato
- `matricula` (opcional): Filtrar por matrícula exata
- `nome` (opcional): Busca parcial por nome
- `email` (opcional): Filtrar por email exato
- `instituicao_id` (opcional): Filtrar por ID da instituição

**Exemplo:**
```bash
curl "http://localhost:8000/alunos?pagina=1&limite=10&ativo=true&nome=joao"
```

### 🔍 Obter Aluno por ID
```
GET /alunos/{id}
```

**Exemplo:**
```bash
curl http://localhost:8000/alunos/1
```

### 🔍 Obter Aluno por CPF
```
GET /alunos/cpf/{cpf}
```

**Exemplo:**
```bash
curl http://localhost:8000/alunos/cpf/123.456.789-09
# ou
curl http://localhost:8000/alunos/cpf/12345678909
```

### 🔍 Obter Aluno por Matrícula
```
GET /alunos/matricula/{matricula}
```

**Exemplo:**
```bash
curl http://localhost:8000/alunos/matricula/20230001
```

### 🔍 Obter Aluno por Email
```
GET /alunos/email/{email}
```

**Exemplo:**
```bash
curl http://localhost:8000/alunos/email/joao.silva@email.com
```

### 📊 Health Check
```
GET /health
```

**Resposta:**
```json
{
  "status": "healthy",
  "service": "api-lyceum",
  "version": "1.0.0"
}
```

### ℹ️ Informações da API
```
GET /
```

Retorna informações sobre a API e endpoints disponíveis.

## 🗄️ Modelos de Dados

### Aluno
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | ID único |
| nome | String(200) | Nome completo |
| email | String(100) | Email único |
| cpf | String(14) | CPF formatado |
| data_nascimento | Date | Data de nascimento |
| telefone | String(20) | Telefone |
| endereco | Text | Endereço completo |
| matricula | String(50) | Número de matrícula |
| ativo | Boolean | Status ativo/inativo |
| instituicao_id | Integer | ID da instituição |

### Instituição
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | ID único |
| nome | String(200) | Nome da instituição |
| codigo_inep | String(20) | Código INEP único |
| tipo | String(20) | Tipo (federal/estadual/municipal/privada) |
| endereco | Text | Endereço completo |
| cidade | String(100) | Cidade |
| estado | String(2) | Estado (sigla) |
| telefone | String(20) | Telefone |
| email | String(100) | Email |

## 🔍 Exemplos de Uso

### 1. Listar todos os alunos ativos:
```bash
curl "http://localhost:8000/alunos?ativo=true"
```

### 2. Buscar aluno por CPF:
```bash
curl "http://localhost:8000/alunos/cpf/123.456.789-09"
```

### 3. Buscar alunos por nome parcial:
```bash
curl "http://localhost:8000/alunos?nome=Silva"
```

### 4. Listar alunos com paginação:
```bash
curl "http://localhost:8000/alunos?pagina=2&limite=20"
```

### 5. Filtrar por instituição:
```bash
curl "http://localhost:8000/alunos?instituicao_id=1"
```

## 🧪 Testes

### Testar com curl:
```bash
# Testar health check
curl http://localhost:8000/health

# Testar listagem
curl http://localhost:8000/alunos

# Testar documentação (disponível no navegador)
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

### Testar com Python:
```python
import requests

# Listar alunos
response = requests.get("http://localhost:8000/alunos")
alunos = response.json()
print(f"Total de alunos: {len(alunos)}")

# Buscar por CPF
response = requests.get("http://localhost:8000/alunos/cpf/123.456.789-09")
aluno = response.json()
print(f"Aluno encontrado: {aluno['nome']}")
```

## 🛠️ Desenvolvimento

### Scripts Úteis

```bash
# Configurar ambiente do zero
python setup_complete.py

# Inicializar banco de dados
python scripts/init_db.py

# Executar API em modo desenvolvimento
python run.py

# Executar com uvicorn diretamente
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Verificar logs do Docker
docker-compose logs -f

# Parar containers
docker-compose down

# Limpar volumes
docker-compose down -v
```

### Dependências

Principais dependências do projeto:

```txt
fastapi==0.104.1          # Framework web
uvicorn[standard]==0.24.0 # Servidor ASGI
sqlalchemy==2.0.23        # ORM
alembic==1.12.1           # Migrações
psycopg2-binary==2.9.9    # Driver PostgreSQL
pydantic==2.5.0           # Validação de dados
python-dotenv==1.0.0      # Gerenciamento de env
```

## 🔄 Migrações de Banco de Dados

Para criar migrações com Alembic:

```bash
# Criar migration inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

## 🐛 Solução de Problemas

### Problema: PostgreSQL não está acessível
```bash
# Verificar se o container está rodando
docker ps

# Iniciar PostgreSQL
docker start lyceum_postgres

# Verificar logs
docker logs lyceum_postgres

# Testar conexão
docker exec -it lyceum_postgres psql -U postgres -d lyceum_db -c "\l"
```

### Problema: Erro de importação
```bash
# Verificar se está no ambiente virtual
pip list | grep fastapi

# Verificar estrutura de diretórios
ls -la src/

# Reinstalar dependências
pip install -r requirements.txt
```

### Problema: Erro de conexão com banco
```bash
# Verificar variáveis de ambiente
cat .env

# Testar conexão manualmente
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='postgres',
        database='lyceum_db'
    )
    print('Conexão OK')
    conn.close()
except Exception as e:
    print(f'Erro: {e}')
"
```

## 📈 Futuras Melhorias

- [ ] Autenticação JWT
- [ ] Cache com Redis
- [ ] Rate limiting
- [ ] Logs estruturados
- [ ] Métricas com Prometheus
- [ ] Integração com SQL Server
- [ ] Sistema de sincronização automática
- [ ] Testes automatizados
- [ ] CI/CD pipeline

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Leonardo Paiva** - [leonardo201800478](https://github.com/leonardo201800478)

## 🙏 Agradecimentos

- FastAPI por uma framework incrível
- PostgreSQL por ser robusto e confiável
- Docker por facilitar a containerização

---

## 📞 Suporte

Para suporte, abra uma issue no repositório ou entre em contato.

## 🔗 Links Úteis

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Documentação PostgreSQL](https://www.postgresql.org/docs/)
- [Documentação Docker](https://docs.docker.com/)
- [Documentação SQLAlchemy](https://docs.sqlalchemy.org/)

---

**Happy Coding!** 🚀