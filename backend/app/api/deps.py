# file: app/api/deps.py (SUDAH DIPERBAIKI)

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

# Impor nama yang benar (AsyncSessionLocal) dan beri alias sebagai SessionLocal
from app.database import AsyncSessionLocal as SessionLocal

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            await session.begin()
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()