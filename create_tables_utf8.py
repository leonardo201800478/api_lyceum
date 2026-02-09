# create_tables_utf8.py
#!/usr/bin/env python3
"""
Cria tabelas com suporte a UTF-8
"""
import sys
import os
import io

# FORÇA UTF-8
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

# Windows específico
if sys.platform == "win32":
    import win32api
    import win32con
    
    # Configura code page para UTF-8
    os.system("chcp 65001 > nul")
    
    # Configura stdout/stderr
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

# Patch para sys.stdout no Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("🗄️ Criando tabelas com suporte UTF-8...")

try:
    # Adiciona path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Tenta ler o arquivo database.py com encoding explícito
    database_path = os.path.join("app", "core", "database.py")
    
    with open(database_path, 'r', encoding='utf-8', errors='replace') as f:
        database_code = f.read()
    
    # Executa o código em um namespace separado
    database_globals = {}
    exec(database_code, database_globals)
    
    # Obtém Base e sync_engine
    Base = database_globals['Base']
    sync_engine = database_globals['sync_engine']
    
    # Cria tabelas
    Base.metadata.create_all(bind=sync_engine)
    
    print("✅ Tabelas criadas com sucesso! (UTF-8)")
    
    # Verifica encoding do banco
    from sqlalchemy import text
    with sync_engine.connect() as conn:
        result = conn.execute(text("SHOW client_encoding"))
        encoding = result.scalar()
        print(f"📊 Encoding do banco: {encoding}")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    
    # Tenta criar via SQL direto
    print("\n🔄 Criando via SQL direto...")
    try:
        import subprocess
        
        # SQL para criar tabela com UTF-8
        sql = """
        CREATE DATABASE lyceum_db 
        WITH ENCODING = 'UTF8' 
        LC_COLLATE = 'Portuguese_Brazil.1252' 
        LC_CTYPE = 'Portuguese_Brazil.1252';
        
        CREATE TABLE IF NOT EXISTS ly_aluno (
            aluno VARCHAR(50) PRIMARY KEY,
            nome_compl VARCHAR(200),
            curso VARCHAR(100),
            serie INTEGER,
            e_mail_interno VARCHAR(200),
            data_sincronizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sincronizado BOOLEAN DEFAULT FALSE
        ) WITH (OIDS = FALSE) TABLESPACE pg_default;
        
        ALTER TABLE ly_aluno OWNER TO postgres;
        """
        
        # Executa SQL
        cmd = [
            "docker", "exec", "lyceum-db",
            "psql", "-U", "postgres", 
            "-c", "CREATE DATABASE lyceum_db ENCODING 'UTF8' LC_COLLATE 'Portuguese_Brazil.1252' LC_CTYPE 'Portuguese_Brazil.1252';"
        ]
        
        subprocess.run(cmd, capture_output=True, text=True)
        print("✅ Banco criado com UTF-8")
        
    except Exception as e2:
        print(f"❌ Erro SQL: {e2}")