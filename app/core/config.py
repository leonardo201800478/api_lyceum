import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App
    APP_NAME: str = os.getenv("APP_NAME")
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SYNC_DATABASE_URL: str = os.getenv("SYNC_DATABASE_URL")

settings = Settings()
