import subprocess
import sys
import os

def check_docker():
    """Verificar se Docker está instalado e funcionando."""
    print("Verificando instalação do Docker...")
    
    try:
        # Verificar versão do Docker
        result = subprocess.run(["docker", "--version"], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✓ Docker instalado: {result.stdout.strip()}")
        else:
            print("✗ Docker não encontrado")
            return False
    except FileNotFoundError:
        print("✗ Docker não encontrado no PATH")
        return False
    
    try:
        # Verificar se Docker está rodando
        result = subprocess.run(["docker", "info"], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✓ Docker está rodando")
            return True
        else:
            print("✗ Docker não está rodando")
            print("  Erro:", result.stderr)
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar Docker: {e}")
        return False

def start_docker_service():
    """Tentar iniciar o serviço Docker."""
    print("\nTentando iniciar Docker Desktop...")
    
    # Tentar abrir Docker Desktop
    try:
        subprocess.run(["cmd", "/c", "start", "docker://"], shell=True)
        print("✓ Docker Desktop iniciado")
        return True
    except Exception as e:
        print(f"✗ Não foi possível iniciar Docker Desktop: {e}")
        return False

def test_docker():
    """Testar Docker com container simples."""
    print("\nTestando Docker com hello-world...")
    
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", "hello-world"],
            capture_output=True, text=True, shell=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✓ Docker testado com sucesso")
            return True
        else:
            print("✗ Falha no teste do Docker")
            print("  Saída:", result.stderr[:200])
            return False
    except subprocess.TimeoutExpired:
        print("✗ Timeout ao testar Docker")
        return False
    except Exception as e:
        print(f"✗ Erro ao testar Docker: {e}")
        return False

def start_postgres():
    """Iniciar PostgreSQL no Docker."""
    print("\nIniciando PostgreSQL no Docker...")
    
    # Parar container existente se houver
    subprocess.run(["docker", "stop", "lyceum_postgres"], 
                  capture_output=True, shell=True)
    subprocess.run(["docker", "rm", "lyceum_postgres"], 
                  capture_output=True, shell=True)
    
    # Iniciar novo container
    cmd = [
        "docker", "run", "-d",
        "--name", "lyceum_postgres",
        "-e", "POSTGRES_PASSWORD=postgres",
        "-e", "POSTGRES_DB=lyceum_db",
        "-p", "5432:5432",
        "--restart", "unless-stopped",
        "postgres:15-alpine"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print("✓ PostgreSQL iniciado no Docker")
            print("  Container ID:", result.stdout.strip())
            
            # Aguardar inicialização
            import time
            print("  Aguardando inicialização...")
            time.sleep(5)
            
            # Verificar se está saudável
            health_cmd = ["docker", "exec", "lyceum_postgres", "pg_isready", "-U", "postgres"]
            for _ in range(10):
                result = subprocess.run(health_cmd, capture_output=True, shell=True)
                if result.returncode == 0:
                    print("✓ PostgreSQL está pronto")
                    return True
                time.sleep(2)
            
            print("⚠ PostgreSQL iniciou mas pode não estar pronto")
            return True
        else:
            print("✗ Falha ao iniciar PostgreSQL")
            print("  Erro:", result.stderr)
            return False
    except Exception as e:
        print(f"✗ Erro ao iniciar PostgreSQL: {e}")
        return False

def main():
    print("=" * 50)
    print("Verificação e Configuração do Docker")
    print("=" * 50)
    
    # Verificar Docker
    if not check_docker():
        print("\nDocker não está disponível.")
        print("\nSoluções possíveis:")
        print("1. Execute Docker Desktop como Administrador")
        print("2. Verifique se a virtualização está habilitada na BIOS")
        print("3. Reinstale Docker Desktop")
        return
    
    # Testar Docker
    if not test_docker():
        print("\nTentando iniciar Docker Desktop...")
        if start_docker_service():
            print("Aguardando 10 segundos...")
            import time
            time.sleep(10)
            test_docker()
    
    # Perguntar se deseja iniciar PostgreSQL
    print("\n" + "=" * 50)
    choice = input("Deseja iniciar PostgreSQL no Docker? (s/n): ")
    
    if choice.lower() == 's':
        if start_postgres():
            print("\n" + "=" * 50)
            print("PostgreSQL configurado com sucesso!")
            print("Host: localhost")
            print("Porta: 5432")
            print("Usuário: postgres")
            print("Senha: postgres")
            print("Banco: lyceum_db")
            print("=" * 50)
            
            # Atualizar .env
            env_content = """# API Configuration
API_V1_STR=/
PROJECT_NAME=API Lyceum - Alunos

# Database Configuration (PostgreSQL Docker)
DB_TYPE=postgresql
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lyceum_db
"""
            
            with open(".env", "w") as f:
                f.write(env_content)
            
            print("\nArquivo .env atualizado!")
            print("Agora você pode executar: python scripts/init_db.py")
        else:
            print("\nNão foi possível configurar PostgreSQL.")
    else:
        print("\nPostgreSQL não será iniciado.")

if __name__ == "__main__":
    main()