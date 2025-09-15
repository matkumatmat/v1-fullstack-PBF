from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Database settings - Updated for PostgreSQL
    # The DATABASE_URL is constructed from environment variables.
    # Format: postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB_NAME
    DATABASE_URL: str = "postgresql+psycopg://postgres:kaayeeysides@localhost/pbfserver"
    SECRET_KEY: str = "kaayeey-sides-fullstack-pbf-app" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1000

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
