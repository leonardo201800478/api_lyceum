
#!/usr/bin/env python3
"""
Script para inicializar o projeto
"""
import os
import subprocess
import sys
from pathlib import Path

def create_directories():
    """Cria a estrutura de diretórios do projeto"""
    directories = [
        "app/core",
        "app/api/v1/endpoints",
        "app/models",
        "app/schemas",
        "app/services",
        "app/crud",
        "app/utils",
        "tests",
        "migrations/versions",
        "docker",
        "scripts",
        "logs",
        "data",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Criado diretório: {directory}")
    
    # Criar arquivos __init__.py
    init_files = [
        "app/__init__.py",
        "app/core/__init__.py",
        "app/api/__init__.py",
        "app/api/v1/__init__.py",
        "app/api/v1/endpoints/__init__.py",
        "app/models/__init__.py",
        "app/schemas/__init__.py",
        "app/services/__init__.py",
        "app/crud/__init__.py",
        "app/utils/__init__.py",
        "tests/__init__.py",
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"✓ Criado: {init_file}")

def check_dependencies():
    """Verifica dependências do sistema"""
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        print("✓ Dependências Python OK")
    except ImportError as e:
        print(f"✗ Dependência faltando: {e}")
        return False
    
    # Verifica Docker
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        print("✓ Docker OK")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ Docker não encontrado (opcional para desenvolvimento local)")
    
    # Verifica Docker Compose
    try:
        subprocess.run(["docker-compose", "--version"], capture_output=True, check=True)
        print("✓ Docker Compose OK")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ Docker Compose não encontrado")
    
    return True

def setup_environment():
    """Configura ambiente do projeto"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_file.exists():
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print("✓ Criado arquivo .env a partir de .env.example")
        else:
            print("⚠ Arquivo .env.example não encontrado")
    else:
        print("✓ Arquivo .env já existe")
    
    # Cria diretório para banco de dados
    Path("data").mkdir(exist_ok=True)

def main():
    """Função principal"""
    print("🚀 Inicializando projeto API Lyceum FastAPI\n")
    
    # Cria estrutura de diretórios
    print("📁 Criando estrutura de diretórios...")
    create_directories()
    
    # Verifica dependências
    print("\n🔍 Verificando dependências...")
    if not check_dependencies():
        print("\n⚠ Algumas dependências estão faltando.")
        print("  Execute: pip install -r requirements.txt")
    
    # Configura ambiente
    print("\n⚙️ Configurando ambiente...")
    setup_environment()
    
    print("\n✨ Projeto inicializado com sucesso!")
    print("\n📋 Próximos passos:")
    print("  1. Edite o arquivo .env com suas credenciais")
    print("  2. Execute: docker-compose -f docker/docker-compose.yml up --build")
    print("  3. Acesse: http://localhost:8000/docs")
    print("\n🎉 Boa codificação!")

if __name__ == "__main__":
    main()