import asyncio
import sys
import typer
import uvicorn
import os
import pkgutil
import importlib

# Import Alembic
from alembic.config import Config
from alembic import command

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set the event loop policy for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database import Base, async_engine

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

    # Dynamically import all model files to register them with Base
    models_package = "app.models"
    package = importlib.import_module(models_package)
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f".{name}"
        if full_module_name.endswith(".py"):
             full_module_name = full_module_name[:-3]
        
        # Import subpackages if they exist (like 'newmodels')
        module_path = os.path.join(package.__path__[0], name)
        if os.path.isdir(module_path):
            sub_package = importlib.import_module(f"{models_package}.{name}")
            for _, sub_name, _ in pkgutil.iter_modules(sub_package.__path__):
                 importlib.import_module(f".{sub_name}", sub_package.__name__)
                 typer.echo(f" - Registered models from: {name}.{sub_name}")
        else:
            importlib.import_module(full_module_name, package.__name__)
            typer.echo(f" - Registered models from: {name}")


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
    Upgrade the database to a later version.
    """
    typer.echo(f"Upgrading database to revision: {revision}...")
    command.upgrade(alembic_cfg, revision)
    typer.secho("✅ Database upgrade complete.", fg=typer.colors.GREEN)

@db_cli.command()
def downgrade(revision: str = typer.Argument("base", help="The revision to downgrade to.")):
    """
    Downgrade the database to a previous version.
    """
    typer.echo(f"Downgrading database to revision: {revision}...")
    command.downgrade(alembic_cfg, revision)
    typer.secho("✅ Database downgrade complete.", fg=typer.colors.GREEN)

@cli.command()
def run(
    host: str = typer.Option("127.0.0.1", help="The host to bind the server to."),
    port: int = typer.Option(5000, help="The port to run the server on."),
    reload: bool = typer.Option(True, help="Enable auto-reloading for development."),
):
    """
    Runs the development server.
    """
    typer.echo(f"🚀 Starting server on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    cli()
