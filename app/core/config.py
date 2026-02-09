# app/core/config.py
import os
from typing import List


class Settings:
    """Configuracoes que lêem APENAS do .env"""
    
    # Application
    APP_NAME: str = os.getenv("APP_NAME", "API Lyceum Sync")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "API Lyceum Sync")
    
    # CORS (tratamento especial para lista)
    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        import json
        cors = os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:3000", "http://localhost:8000"]')
        try:
            return json.loads(cors.replace("'", '"'))
        except:
            return ["http://localhost:3000", "http://localhost:8000"]
    
    # Database (NENHUMA SENHA NO CODIGO - so no .env)
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "lyceum_db")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    
    @property
    def DATABASE_URL(self) -> str:
        """Constroi URL do banco SEM expor senha no codigo"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Constroi URL sincrona do banco SEM expor senha no codigo"""
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # API Lyceum (NENHUMA SENHA NO CODIGO - so no .env)
    LYCEUM_API_BASE_URL: str = os.getenv("LYCEUM_API_BASE_URL", "https://api.lyceum.com.br")
    LYCEUM_API_USERNAME: str = os.getenv("LYCEUM_API_USERNAME", "")
    LYCEUM_API_PASSWORD: str = os.getenv("LYCEUM_API_PASSWORD", "")
    LYCEUM_API_TIMEOUT: int = int(os.getenv("LYCEUM_API_TIMEOUT", "30"))
    LYCEUM_API_PAGE_SIZE: int = int(os.getenv("LYCEUM_API_PAGE_SIZE", "100"))
    LYCEUM_API_DELAY: float = float(os.getenv("LYCEUM_API_DELAY", "0.1"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE", "50"))
    MAX_PAGE_SIZE: int = int(os.getenv("MAX_PAGE_SIZE", "100"))
    
    # Timezone
    TIMEZONE: str = os.getenv("TZ", "America/Sao_Paulo")


settings = Settings()