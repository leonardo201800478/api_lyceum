from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Config
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API Lyceum"
    
    # Database
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "lyceum_db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # SQL Server Config (para futuro)
    SQL_SERVER_HOST: Optional[str] = None
    SQL_SERVER_DATABASE: Optional[str] = None
    SQL_SERVER_USERNAME: Optional[str] = None
    SQL_SERVER_PASSWORD: Optional[str] = None
    
    # Sync Config
    SYNC_INTERVAL_MINUTES: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()