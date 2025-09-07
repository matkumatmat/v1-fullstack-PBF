# file: app/api/deps.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

# Impor SessionLocal dari konfigurasi database Anda
from app.database import SessionLocal

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency FastAPI yang menyediakan sesi database (AsyncSession) per permintaan.

    DEVIL'S ADVOCATE NOTE:
    Nama `get_db_session` dipilih secara sengaja untuk menghindari ambiguitas.
    Fungsi ini TIDAK mengambil data. Ia menyediakan OBJEK SESI (`db`)
    yang kemudian Anda gunakan di service layer untuk MENGEKSEKUSI query,
    seperti `await db.execute(select(...))`.
    Ini selaras dengan keputusan arsitektur kita untuk menggunakan `select`
    secara konsisten demi fleksibilitas dan kekuatan.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            # `async with` sudah menangani commit, rollback, dan close,
            # jadi blok ini adalah jaring pengaman.
            await session.close()