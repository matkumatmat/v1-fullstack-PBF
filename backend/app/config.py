from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Application settings are loaded from environment variables.
    A .env file is supported for local development.
    """
    # Database settings
    # The default value uses a local SQLite database for simplicity.
    # For PostgreSQL, this would be: "postgresql+asyncpg://user:password@host/dbname"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

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
