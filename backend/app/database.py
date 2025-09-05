from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
from typing import AsyncGenerator

# Create an asynchronous engine using the URL from settings
# `echo=True` is useful for debugging as it logs all SQL statements.
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True to see generated SQL statements
)

# Create a configured "Session" class
# This is the factory for new AsyncSession objects
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create a Base class for declarative class definitions
# Our SQLAlchemy models will inherit from this class.
Base = declarative_base()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get a database session.
    This will be used in API endpoints to interact with the database.
    It ensures that the session is always closed after the request is finished.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
