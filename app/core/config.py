# app/core/config.py
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "API Lyceum"
    app_env: str = "development"

    db_dialect: str = "postgres"

    # Postgres (Docker)
    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_db: str = "api_lyceum"
    postgres_user: str = "lyceum_user"
    postgres_password: str = "lyceum_pass"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()