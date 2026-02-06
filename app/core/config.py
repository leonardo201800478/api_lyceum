from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "API Lyceum"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API Lyceum Sync"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "lyceum_user"
    POSTGRES_PASSWORD: str = "lyceum_password"
    POSTGRES_DB: str = "lyceum_db"
    POSTGRES_PORT: int = 5432
    
    DATABASE_URL: Optional[PostgresDsn] = None
    SYNC_DATABASE_URL: Optional[str] = None
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> str:
        if isinstance(v, str):
            return v
        
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT", 5432),
            path=values.get("POSTGRES_DB", ""),
        ).unicode_string()
    
    @field_validator("SYNC_DATABASE_URL", mode="before")
    @classmethod
    def assemble_sync_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> str:
        if isinstance(v, str):
            return v
        
        values = info.data
        return f"postgresql+psycopg2://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT', 5432)}/{values.get('POSTGRES_DB')}"
    
    # API Lyceum
    LYCEUM_API_BASE_URL: str = "https://api.lyceum.com.br"
    LYCEUM_API_USERNAME: str = ""
    LYCEUM_API_PASSWORD: str = ""
    LYCEUM_API_TIMEOUT: int = 30
    LYCEUM_API_PAGE_SIZE: int = 100
    LYCEUM_API_DELAY: float = 0.1
    
    # Redis
    REDIS_URL: Optional[RedisDsn] = None
    
    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Optional[str]:
        if isinstance(v, str):
            return v
        
        values = info.data
        if "REDIS_HOST" in values:
            return f"redis://{values.get('REDIS_HOST')}:{values.get('REDIS_PORT', 6379)}/0"
        return None
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100
    
    # Timezone
    TIMEZONE: str = "America/Sao_Paulo"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()