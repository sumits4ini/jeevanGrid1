"""
Alembic Environment Configuration for JeevanGrid (PostGIS & SQLAlchemy 2.0)
"""

import sys
from logging.config import fileConfig
from pathlib import Path
from alembic import context
from sqlalchemy import engine_from_config, pool

# Add project root to sys.path
root_path = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root_path))

from backend.app.core.config import settings
from backend.app.db.base import Base
# Import all models to ensure they are registered with Base.metadata
import backend.app.models  # noqa: F401

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate' support
target_metadata = Base.metadata

# Inject the dynamic database URL from settings
config.set_main_option("sqlalchemy.url", settings.SYNC_DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
