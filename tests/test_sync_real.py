# test_sync_real.py
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

async def main():
    from app.core.database import AsyncSessionLocal
    from app.services.sync_aluno import sync_alunos

    print("=" * 60)
    print("🚀 TESTE DE INTEGRAÇÃO REAL COM API LYCEUM")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        print("\n🔄 Iniciando sincronização de alunos...")
        stats = await sync_alunos(db, incremental=False)

        print("\n✅ Sincronização concluída!")
        print(f"📊 Estatísticas:")
        print(f"   Total na API: {stats['total_api']}")
        print(f"   Inseridos:    {stats['inseridos']}")
        print(f"   Atualizados:  {stats['atualizados']}")
        print(f"   Ignorados:    {stats['ignorados']}")
        print(f"   Erros:        {stats['erros']}")
        print(f"   Duração:      {stats['duracao']:.2f} segundos")

        # Verifica quantos registros foram inseridos
        from sqlalchemy import func, select
        from app.models.ly_aluno import LYAluno
        count = await db.execute(select(func.count()).select_from(LYAluno))
        total = count.scalar()
        print(f"\n💾 Total de registros na tabela 'ly_aluno': {total}")

if __name__ == "__main__":
    asyncio.run(main())