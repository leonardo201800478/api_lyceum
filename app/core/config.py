# app/core/config.py
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # App
    APP_NAME: str = "API Lyceum Sync"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API Lyceum Sync"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database (PostgreSQL) - usado para construir URLs
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "lyceum_api_user"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "lyceum_production_db"
    POSTGRES_PORT: int = 5432

    # Override direto das URLs (prioridade máxima)
    # Se definidas (via .env ou atribuição), substituem as URLs computadas
    DATABASE_URL: Optional[str] = None
    SYNC_DATABASE_URL: Optional[str] = None

    # API Lyceum
    LYCEUM_API_BASE_URL: str = "https://api.lyceum.com.br"
    LYCEUM_API_USERNAME: str = ""
    LYCEUM_API_PASSWORD: str = ""
    LYCEUM_API_TIMEOUT: int = 30
    LYCEUM_API_PAGE_SIZE: int = 100
    LYCEUM_API_DELAY: float = 0.1

    # Redis (opcional)
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    # ------------------------------------------------------------
    # URLs Computadas (usadas apenas se as diretas não forem fornecidas)
    # ------------------------------------------------------------
    @property
    def _computed_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def _computed_sync_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DATABASE_URL(self) -> str:
        """URL assíncrona – retorna o valor direto ou computa."""
        return self.__dict__.get('DATABASE_URL') or self._computed_database_url

    @DATABASE_URL.setter
    def DATABASE_URL(self, value: str):
        """Permite atribuição direta (ex: nos testes)."""
        self.__dict__['DATABASE_URL'] = value

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """URL síncrona – retorna o valor direto ou computa."""
        return self.__dict__.get('SYNC_DATABASE_URL') or self._computed_sync_database_url

    @SYNC_DATABASE_URL.setter
    def SYNC_DATABASE_URL(self, value: str):
        self.__dict__['SYNC_DATABASE_URL'] = value

settings = Settings()