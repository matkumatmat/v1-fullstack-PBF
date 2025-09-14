import asyncio
import sys
import typer
import uvicorn
import os
import importlib
from sqlalchemy import text

current_path = os.path.dirname(os.path.abspath(__file__))
if current_path not in sys.path:
    sys.path.append(current_path)

from dotenv import load_dotenv
load_dotenv()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database import Base, async_engine
from alembic.config import Config
from alembic import command

cli = typer.Typer(help="CLI for managing FastAPI")
db_cli = typer.Typer(help="CLI for managaging db")
cli.add_typer(db_cli, name="db")

alembic_cfg = Config("alembic.ini")

@db_cli.command()
def init():
    typer.confirm(" Peringatan: Perintah ini akan MENGHAPUS SEMUA DATA di database. Anda yakin ingin melanjutkan?", abort=True)
    typer.echo("Menginisialisasi database...")
    try:
        importlib.import_module("app.models")
        typer.echo(" - Berhasil mendaftarkan semua model dari paket 'app.models'.")
    except Exception as e:
        typer.secho(f" Gagal mendaftarkan model: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    async def create_tables():
        async with async_engine.begin() as conn:
            typer.secho("Dropping all existing tables with CASCADE...", fg=typer.colors.YELLOW)
            await conn.execute(text("DROP SCHEMA public CASCADE;"))
            await conn.execute(text("CREATE SCHEMA public;"))
            typer.echo("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
        typer.secho(" Database berhasil diinisialisasi.", fg=typer.colors.GREEN)
    asyncio.run(create_tables())

@db_cli.command()
def revision(message: str = typer.Option(..., "-m", "--message", help="Pesan deskriptif untuk revisi migrasi.")):
    typer.echo(f"Membuat revisi migrasi baru dengan pesan: '{message}'...")
    try:
        command.revision(alembic_cfg, message=message, autogenerate=True)
        typer.secho(" File revisi migrasi berhasil dibuat di direktori 'alembic/versions/'.", fg=typer.colors.GREEN)
        typer.echo(" Langkah selanjutnya: Periksa file yang baru dibuat, lalu jalankan 'py manage.py db upgrade'")
    except Exception as e:
        typer.secho(f" Gagal membuat revisi: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@db_cli.command()
def upgrade(revision: str = typer.Argument("head", help="Revisi tujuan upgrade (default: 'head' untuk yang terbaru).")):
    typer.echo(f"Menerapkan upgrade database ke revisi: {revision}...")
    try:
        command.upgrade(alembic_cfg, revision)
        typer.secho(" Upgrade database selesai.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f" Gagal saat upgrade: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@db_cli.command()
def downgrade(revision: str = typer.Argument("-1", help="Revisi tujuan downgrade (default: '-1' untuk turun satu revisi).")):
    typer.echo(f"Mengembalikan database ke revisi: {revision}...")
    try:
        command.downgrade(alembic_cfg, revision)
        typer.secho(" Downgrade database selesai.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f" Gagal saat downgrade: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@cli.command()
def run(
    host: str = typer.Option("127.0.0.1", help="Host untuk server."),
    port: int = typer.Option(5000, help="Port untuk server."),
    reload: bool = typer.Option(True, help="Aktifkan auto-reload untuk development."),
):
    typer.echo(f"🚀 Memulai server di http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    cli()