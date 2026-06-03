import os
from logging.config import fileConfig

from dotenv import load_dotenv
from alembic import context
from sqlalchemy import create_engine, pool

# --- load env vars early ---
load_dotenv()

# --- Alembic config ---
config = context.config

# --- set DB URL from env ---
database_url = os.getenv("ALEMBIC_DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# --- logging config ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- IMPORT MODELS (ONLY AFTER env setup) ---
from app.backend.db.models import Base

target_metadata = Base.metadata


# =========================
# OFFLINE MODE
# =========================
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# =========================
# ONLINE MODE
# =========================
def run_migrations_online() -> None:
    url = config.get_main_option("sqlalchemy.url")

    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# =========================
# ENTRY POINT
# =========================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()