# fix_encoding.py
import os
import re
from pathlib import Path

# Lista de arquivos do SEU projeto (ignora venv)
project_files = [
    "app/api/deps.py",
    "app/api/v1/endpoints/health.py",
    "app/api/v1/endpoints/security.py",
    "app/api/v1/endpoints/sync.py",
    "app/api/v1/endpoints/alunos.py",
    "app/core/config.py",
    "app/core/database.py",
    "app/core/security.py",
    "app/core/__init__.py",
    "app/main.py",
    "app/middleware/security.py",
    "app/models/ly_aluno.py",
    "app/schemas/aluno.py",
    "app/schemas/__init__.py",
    "app/services/lyceum_api.py",
    "app/services/sync_service.py",
    "app/utils/pagination.py",
    "scripts/init_project.py",
    "start_api.py",
    "sync_manual.py",
    "tests/test_security.py",
]

# Mapeamento de correções
replacements = {
    "á": "a",
    "é": "e", 
    "í": "i",
    "ó": "o",
    "ú": "u",
    "ã": "a",
    "õ": "o",
    "ç": "c",
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "Ã": "A",
    "Õ": "O",
    "Ç": "C"
}

def fix_file(filepath):
    """Corrige acentos em um arquivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substitui acentos
        new_content = content
        for accent, replacement in replacements.items():
            new_content = new_content.replace(accent, replacement)
        
        # Se houve mudança, salva
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Corrigido: {filepath}")
            return True
        else:
            print(f"✓ OK: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Erro em {filepath}: {e}")
        return False

def main():
    print("🔧 CORRIGINDO ACENTOS NOS ARQUIVOS PYTHON")
    print("="*50)
    
    fixed_count = 0
    
    for filepath in project_files:
        if os.path.exists(filepath):
            if fix_file(filepath):
                fixed_count += 1
    
    print(f"\n📊 Resumo: {fixed_count} arquivos corrigidos")
    
    if fixed_count > 0:
        print("\n🎯 Agora crie as tabelas:")
        print("python fix_tables.py")
    else:
        print("\n✅ Nenhum arquivo precisou de correção")

if __name__ == "__main__":
    main()