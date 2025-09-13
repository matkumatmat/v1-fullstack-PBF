# file: manage.py (FINAL & COMPLETE)

import asyncio
import sys
import typer
import uvicorn
import os
import importlib

# --- [BLOK KODE KRUSIAL UNTUK ROBUSTNESS] ---
# Menambahkan direktori root proyek ke path Python.
# Ini memastikan impor absolut seperti `from app.database...` selalu berfungsi.
current_path = os.path.dirname(os.path.abspath(__file__))
if current_path not in sys.path:
    sys.path.append(current_path)
# --- [AKHIR BLOK KODE KRUSIAL] ---

# Load environment variables dari .env file
from dotenv import load_dotenv
load_dotenv()

# Set event loop policy untuk Windows jika diperlukan
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Impor dari 'app' sekarang dijamin berhasil
from app.database import Base, async_engine
from alembic.config import Config
from alembic import command

# --- [SETUP APLIKASI CLI] ---
cli = typer.Typer(help="CLI untuk mengelola aplikasi FastAPI.")
db_cli = typer.Typer(help="Perintah untuk manajemen database.")
cli.add_typer(db_cli, name="db")

# Konfigurasi Alembic
alembic_cfg = Config("alembic.ini")

# --- [PERINTAH-PERINTAH DATABASE] ---

@db_cli.command()
def init():
    """
    Menginisialisasi database: HAPUS SEMUA TABEL dan buat ulang dari awal.
    PERINGATAN: Semua data akan hilang. Gunakan hanya untuk setup awal.
    """
    typer.confirm("⚠️ Peringatan: Perintah ini akan MENGHAPUS SEMUA DATA di database. Anda yakin ingin melanjutkan?", abort=True)
    
    typer.echo("Menginisialisasi database...")
    try:
        # Memastikan semua model terdaftar di metadata SQLAlchemy
        importlib.import_module("app.models")
        typer.echo(" - Berhasil mendaftarkan semua model dari paket 'app.models'.")
    except Exception as e:
        typer.secho(f"❌ Gagal mendaftarkan model: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    async def create_tables():
        async with async_engine.begin() as conn:
            typer.secho("   - Menghapus semua tabel yang ada...", fg=typer.colors.YELLOW)
            await conn.run_sync(Base.metadata.drop_all)
            typer.echo("   - Membuat semua tabel baru...")
            await conn.run_sync(Base.metadata.create_all)
        typer.secho("✅ Database berhasil diinisialisasi.", fg=typer.colors.GREEN)

    asyncio.run(create_tables())

# ✅ ===================================================================
# ✅ PERINTAH BARU YANG HILANG: `revision`
# ✅ ===================================================================
@db_cli.command()
def revision(message: str = typer.Option(..., "-m", "--message", help="Pesan deskriptif untuk revisi migrasi.")):
    """
    Membuat file migrasi baru secara otomatis berdasarkan perubahan pada model.
    """
    typer.echo(f"Membuat revisi migrasi baru dengan pesan: '{message}'...")
    try:
        command.revision(alembic_cfg, message=message, autogenerate=True)
        typer.secho("✅ File revisi migrasi berhasil dibuat di direktori 'alembic/versions/'.", fg=typer.colors.GREEN)
        typer.echo("👉 Langkah selanjutnya: Periksa file yang baru dibuat, lalu jalankan 'py manage.py db upgrade'")
    except Exception as e:
        typer.secho(f"❌ Gagal membuat revisi: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
# ===================================================================

@db_cli.command()
def upgrade(revision: str = typer.Argument("head", help="Revisi tujuan upgrade (default: 'head' untuk yang terbaru).")):
    """
    Menerapkan migrasi ke database untuk membawanya ke versi yang lebih baru.
    """
    typer.echo(f"Menerapkan upgrade database ke revisi: {revision}...")
    try:
        command.upgrade(alembic_cfg, revision)
        typer.secho("✅ Upgrade database selesai.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"❌ Gagal saat upgrade: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@db_cli.command()
def downgrade(revision: str = typer.Argument("-1", help="Revisi tujuan downgrade (default: '-1' untuk turun satu revisi).")):
    """
    Mengembalikan migrasi database ke versi sebelumnya.
    """
    typer.echo(f"Mengembalikan database ke revisi: {revision}...")
    try:
        command.downgrade(alembic_cfg, revision)
        typer.secho("✅ Downgrade database selesai.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"❌ Gagal saat downgrade: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

# --- [PERINTAH SERVER] ---

@cli.command()
def run(
    host: str = typer.Option("127.0.0.1", help="Host untuk server."),
    port: int = typer.Option(5000, help="Port untuk server."),
    reload: bool = typer.Option(True, help="Aktifkan auto-reload untuk development."),
):
    """
    Menjalankan server development menggunakan Uvicorn.
    """
    typer.echo(f"🚀 Memulai server di http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    cli()