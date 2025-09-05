from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Application settings are loaded from environment variables.
    A .env file is supported for local development.
    """
    # backend/app/config.py

    # Baris yang lama (untuk SQLite)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

    # JWT settings
    SECRET_KEY: str = "kaayeey-sides-fullstack-pbf-app"  # CHANGE THIS IN PRODUCTION
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1000

    class Config:
        # This tells pydantic-settings to load variables from a .env file
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single instance of the settings to be used throughout the application
settings = Settings()
