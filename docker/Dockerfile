# docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema necessárias para psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas os arquivos de dependências primeiro (cache)
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .[dev]

# Copia o resto do código
COPY . .

# Torna o script de entrypoint executável
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]