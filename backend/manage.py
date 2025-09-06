import asyncio
import sys
import typer
import uvicorn
import os
import pkgutil
import importlib

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set the event loop policy for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database import Base, async_engine

cli = typer.Typer(help="CLI for managing the WMS FastAPI application.")

@cli.command()
def init_db():
    """
    Initializes the database and creates all tables.
    This command dynamically imports all modules in the app.models package
    to ensure SQLAlchemy's Base metadata is populated before creating tables.
    """
    typer.echo("Initializing database...")

    # Dynamically import all model files
    models_package = "app.models"
    package = importlib.import_module(models_package)
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f".{name}", package.__name__)
        typer.echo(f" - Registered models from: {name}")

    async def create_tables():
        async with async_engine.begin() as conn:
            typer.echo("Dropping all existing tables...")
            await conn.run_sync(Base.metadata.drop_all)
            typer.echo("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
        typer.secho("✅ Database has been initialized successfully.", fg=typer.colors.GREEN)

    asyncio.run(create_tables())

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
    uvicorn.run("app:main", factory=True, host=host, port=port, reload=reload)


if __name__ == "__main__":
    cli()
