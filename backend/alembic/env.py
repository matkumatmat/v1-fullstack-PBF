# file: alembic/env.py (REFAKTORED)

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- [BAGIAN 1: TAMBAHAN KRITIS] ---
# Tujuan: Memungkinkan Alembic menemukan model-model Anda.
import os
import sys

# 1. Tambahkan direktori root proyek Anda ke path Python.
#    `os.path.dirname(__file__)` -> direktori 'alembic' saat ini.
#    `'..'` -> naik satu level ke direktori root proyek.
#    Ini memastikan `from app.models...` dapat ditemukan.
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Impor BaseModel Anda.
#    Ini adalah objek pusat yang berisi `metadata` dari SEMUA model Anda.
from app.models.base import BaseModel

# 3. Impor semua modul model Anda.
#    Ini penting agar SQLAlchemy "mendaftarkan" semua tabel Anda ke dalam
#    metadata BaseModel sebelum Alembic membandingkannya.
from app.models import *
# --- [AKHIR BAGIAN 1] ---


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# --- [BAGIAN 2: PERUBAHAN KRITIS] ---
# Tujuan: Memberitahu Alembic skema database seperti apa yang Anda inginkan.
#         Alembic akan membandingkan `target_metadata` ini dengan skema
#         database yang sebenarnya untuk mendeteksi perubahan.
target_metadata = BaseModel.metadata
# --- [AKHIR BAGIAN 2] ---


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()