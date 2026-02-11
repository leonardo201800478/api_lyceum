from app.core.database import Base, sync_engine

# IMPORTA TODOS OS MODELOS
from app.models import ly_aluno  # noqa

def init_db():
    print("🗄️ Criando tabelas no banco...")
    Base.metadata.create_all(bind=sync_engine)
    print("✅ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_db()

    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
