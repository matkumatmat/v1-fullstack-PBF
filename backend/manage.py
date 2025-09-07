# file: manage.py (REFAKTORED & ROBUST)

import asyncio
import sys
import typer
import uvicorn
import os
import pkgutil
import importlib

# --- [BLOK KODE KRITIS UNTUK ROBUSTNESS] ---
# DEVIL'S ADVOCATE NOTE:
# Ini adalah bagian terpenting untuk membuat skrip ini tangguh.
# Kita secara manual menambahkan direktori root proyek ke path Python.
# Ini memastikan bahwa impor absolut seperti `from app.database...` akan
# selalu berfungsi, tidak peduli dari direktori mana Anda menjalankan `py manage.py`.
# Ini menyelesaikan `ModuleNotFoundError`.

# Dapatkan path absolut dari file `manage.py` ini
current_path = os.path.dirname(os.path.abspath(__file__))
# Tambahkan path ini ke sys.path jika belum ada
if current_path not in sys.path:
    sys.path.append(current_path)
# --- [AKHIR BLOK KODE KRITIS] ---


# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set the event loop policy for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Sekarang impor dari `app` dijamin berhasil
from app.database import Base, async_engine
from alembic.config import Config
from alembic import command

cli = typer.Typer(help="CLI for managing the WMS FastAPI application.")
db_cli = typer.Typer(help="Commands for database management.")
cli.add_typer(db_cli, name="db")

# Alembic config
alembic_cfg = Config("alembic.ini")

@db_cli.command()
def init():
    """
    Initializes the database and creates all tables.
    WARNING: This will drop all existing tables.
    """
    typer.echo("Initializing database...")

    # DEVIL'S ADVOCATE NOTE:
    # Logika impor dinamis ini canggih, tetapi bisa disederhanakan.
    # Dengan `__init__.py` yang baik di `app/models`, kita hanya perlu
    # mengimpor paketnya untuk mendaftarkan semua model.
    try:
        importlib.import_module("app.models")
        typer.echo(" - Registered all models from 'app.models' package.")
    except Exception as e:
        typer.secho(f"Error registering models: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    async def create_tables():
        async with async_engine.begin() as conn:
            typer.secho("Dropping all existing tables...", fg=typer.colors.YELLOW)
            await conn.run_sync(Base.metadata.drop_all)
            typer.echo("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
        typer.secho("✅ Database has been initialized successfully.", fg=typer.colors.GREEN)

    asyncio.run(create_tables())


@db_cli.command()
def upgrade(revision: str = typer.Argument("head", help="The revision to upgrade to.")):
    """
    Upgrade the database to a later version using Alembic.
    """
    typer.echo(f"Upgrading database to revision: {revision}...")
    try:
        command.upgrade(alembic_cfg, revision)
        typer.secho("✅ Database upgrade complete.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error during upgrade: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@db_cli.command()
def downgrade(revision: str = typer.Argument("base", help="The revision to downgrade to.")):
    """
    Downgrade the database to a previous version using Alembic.
    """
    typer.echo(f"Downgrading database to revision: {revision}...")
    try:
        command.downgrade(alembic_cfg, revision)
        typer.secho("✅ Database downgrade complete.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error during downgrade: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@cli.command()
def run(
    host: str = typer.Option("127.0.0.1", help="The host to bind the server to."),
    port: int = typer.Option(5000, help="The port to run the server on."),
    reload: bool = typer.Option(True, help="Enable auto-reloading for development."),
):
    """
    Runs the development server using Uvicorn.
    """
    typer.echo(f"🚀 Starting server on http://{host}:{port}")
    # Menggunakan path string ke aplikasi untuk mendukung `reload` dengan benar.
    uvicorn.run("main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    cli()