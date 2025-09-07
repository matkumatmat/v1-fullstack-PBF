# file: app/api/deps.py (SUDAH DIPERBAIKI)

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

# Impor nama yang benar (AsyncSessionLocal) dan beri alias sebagai SessionLocal
from app.database import AsyncSessionLocal as SessionLocal

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
    # Sekarang SessionLocal merujuk ke AsyncSessionLocal yang benar
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            # `async with` sudah menangani commit, rollback, dan close,
            # jadi blok ini adalah jaring pengaman.
            await session.close()