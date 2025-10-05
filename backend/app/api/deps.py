# file: app/api/deps.py (VERSI BENER YANG ANTI-NGAMBANG)

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import AsyncSessionLocal

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency yang menyediakan session database dan mengelola siklus hidup transaksi.
    - Buka sesi.
    - Mulai transaksi.
    - Serahkan sesi ke endpoint.
    - Jika endpoint selesai tanpa error, COMMIT.
    - Jika endpoint melempar error, ROLLBACK.
    - Tutup sesi.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Mulai transaksi. Semua operasi di bawah ini ada di dalam satu blok transaksi.
            await session.begin()
            yield session
            # Jika `yield` selesai tanpa error, commit perubahan.
            await session.commit()
        except Exception:
            # Jika ada error di mana pun, batalkan semua perubahan.
            await session.rollback()
            # Lemparkan lagi errornya biar FastAPI bisa nangani.
            raise
        finally:
            # `async with` akan menutup sesi secara otomatis,
            # tapi ini untuk memastikan.
            await session.close()