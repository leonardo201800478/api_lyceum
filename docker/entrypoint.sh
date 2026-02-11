#!/bin/sh
# docker/entrypoint.sh

set -e

echo "⏳ Aguardando PostgreSQL ficar disponível..."
while ! nc -z $POSTGRES_SERVER $POSTGRES_PORT; do
  sleep 0.5
done
echo "✅ PostgreSQL disponível!"

echo "🔄 Rodando migrations..."
alembic upgrade head

echo "🚀 Iniciando aplicação..."
exec "$@"