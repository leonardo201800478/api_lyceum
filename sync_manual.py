#!/usr/bin/env python3
"""
Sincronizacao manual usando apenas .env
"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env da raiz
load_dotenv()

# Configura path
sys.path.append(str(Path(__file__).parent))

async def sync_alunos():
    """Sincroniza alunos usando credenciais do .env"""
    print("🔄 Iniciando sincronizacao manual...")
    
    try:
        from app.core.database import AsyncSessionLocal
        from app.services.sync_service import SyncService
        
        # Verifica se as credenciais estao configuradas
        username = os.getenv("LYCEUM_API_USERNAME", "").strip()
        password = os.getenv("LYCEUM_API_PASSWORD", "").strip()
        
        if not username or not password:
            print("❌ Credenciais Lyceum nao configuradas no .env")
            return
        
        print(f"🔍 Usando credenciais do .env: {username}")
        
        async with AsyncSessionLocal() as db:
            # Cria servico
            service = SyncService(db)
            
            # Verifica saude da API Lyceum
            print("🔍 Verificando API Lyceum...")
            health = await service.check_api_health()
            print(f"   Status: {health.get('status', 'unknown')}")
            print(f"   Mensagem: {health.get('message', 'N/A')}")
            
            if health.get('status') != 'online':
                print("❌ API Lyceum offline. Abortando.")
                return
            
            # Executa sincronizacao
            print("🔄 Sincronizando alunos...")
            result = await service.sync_alunos(incremental=False)
            
            print("\n✅ Sincronizacao concluida!")
            print(f"   Total API: {result.get('total_api', 0)}")
            print(f"   Inseridos: {result.get('inseridos', 0)}")
            print(f"   Atualizados: {result.get('atualizados', 0)}")
            print(f"   Ignorados: {result.get('ignorados', 0)}")
            print(f"   Erros: {result.get('erros', 0)}")
            print(f"   Duracao: {result.get('duracao', 0):.2f} segundos")
            
            # Conta total no banco
            from app.crud.aluno import aluno
            total = await aluno.count(db)
            print(f"   Total no banco: {total}")
            
    except Exception as e:
        print(f"❌ Erro na sincronizacao: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Funcao principal"""
    print("🎯 SINCRONIZACAO MANUAL (TUDO DO .env)")
    print("="*60)
    
    # Executa sincronizacao
    asyncio.run(sync_alunos())

if __name__ == "__main__":
    main()