#!/usr/bin/env python3
"""
Script para iniciar a API Lyceum Sync usando apenas .env
"""
import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

# FORÇA UTF-8 GLOBALMENTE
if sys.platform == "win32":
    os.system("chcp 65001 > nul")  # Windows - UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configura encoding padrão
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# Carrega variaveis do .env na raiz
load_dotenv()

def check_required_env_vars():
    """Verifica variaveis de ambiente obrigatorias"""
    required = [
        "LYCEUM_API_USERNAME",
        "LYCEUM_API_PASSWORD",
        "POSTGRES_PASSWORD"
    ]
    
    missing = []
    for var in required:
        value = os.getenv(var, "").strip()
        if not value:
            missing.append(var)
    
    if missing:
        print(f"❌ Variaveis de ambiente obrigatorias faltando: {', '.join(missing)}")
        print("   Configure-as no arquivo .env na raiz do projeto")
        return False
    
    return True

def start_postgres():
    """Inicia PostgreSQL usando variaveis do .env"""
    print("🐘 Iniciando PostgreSQL...")
    
    # Usa variaveis do .env
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "")
    db_name = os.getenv("POSTGRES_DB", "lyceum_db")
    
    if not db_password:
        print("❌ POSTGRES_PASSWORD nao configurado no .env")
        return False
    
    # Verifica se ja esta rodando
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=lyceum-db", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            check=False
        )
        if "lyceum-db" in result.stdout:
            print("✅ PostgreSQL ja esta rodando")
            return True
    except FileNotFoundError:
        print("⚠️ Docker nao encontrado. Certifique-se de que o Docker esta instalado e rodando.")
        return False
    
    # Inicia container usando variaveis do .env
    cmd = [
        "docker", "run", "-d", "--name", "lyceum-db",
        "-e", f"POSTGRES_USER={db_user}",
        "-e", f"POSTGRES_PASSWORD={db_password}",
        "-e", f"POSTGRES_DB={db_name}",
        "-p", "5432:5432",
        "--rm",
        "postgres:15-alpine"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ PostgreSQL iniciado")
        
        # Aguarda banco ficar pronto
        print("⏳ Aguardando banco (15 segundos)...")
        time.sleep(15)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar PostgreSQL: {e}")
        return False

def create_tables():
    """Cria tabelas no banco"""
    print("🗄️ Criando tabelas...")
    
    try:
        sys.path.append(str(Path(__file__).parent))
        from app.core.database import Base, sync_engine
        
        Base.metadata.create_all(bind=sync_engine)
        print("✅ Tabelas criadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"⚠️ Erro ao criar tabelas: {e}")
        print("⏳ Continuando...")
        return True

def start_fastapi():
    """Inicia o servidor FastAPI"""
    print("🚀 Iniciando FastAPI...")
    
    # Verifica credenciais
    lyceum_user = os.getenv("LYCEUM_API_USERNAME", "").strip()
    if not lyceum_user:
        print("❌ LYCEUM_API_USERNAME nao configurado no .env")
        return False
    
    lyceum_pass = os.getenv("LYCEUM_API_PASSWORD", "").strip()
    if not lyceum_pass:
        print("❌ LYCEUM_API_PASSWORD nao configurado no .env")
        return False
    
    print(f"✅ Usando credenciais Lyceum do .env: {lyceum_user}")
    
    # Inicia o servidor
    cmd = [
        "uvicorn", "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]
    
    print("\n" + "="*60)
    print("🎯 API LYCEUM SYNC INICIADA (USANDO .env)")
    print("="*60)
    print("🌐 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔄 Sincronizar: POST http://localhost:8000/api/v1/sync/alunos")
    print("🏥 Health: GET http://localhost:8000/api/v1/health")
    print("📊 Alunos: GET http://localhost:8000/api/v1/alunos")
    print("="*60 + "\n")
    
    try:
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        print("\n👋 Encerrando API...")
        return True
    except FileNotFoundError:
        print("❌ Uvicorn nao encontrado. Execute: pip install uvicorn[standard]")
        return False

def main():
    """Funcao principal"""
    print("🚀 INICIANDO API LYCEUM SYNC (TUDO DO .env)")
    print("="*60)
    
    # Verifica variaveis obrigatorias
    if not check_required_env_vars():
        return
    
    # Inicia PostgreSQL
    if not start_postgres():
        print("❌ Falha ao iniciar PostgreSQL")
        print("   Verifique POSTGRES_PASSWORD no .env")
        return
    
    # Cria tabelas
    create_tables()
    
    # Inicia FastAPI
    start_fastapi()

if __name__ == "__main__":
    main()