"""
Unit Tests for Database Engine & Session Configuration
"""

from backend.app.core.config import settings
from backend.app.db.session import async_engine, sync_engine


def test_database_url_configuration():
    """Verifies that database URLs are properly configured."""
    assert "postgresql" in settings.DATABASE_URL
    assert "asyncpg" in settings.DATABASE_URL
    assert "postgresql://" in settings.SYNC_DATABASE_URL
    assert settings.POSTGRES_DB == "jeevangrid_db"


def test_database_engine_instantiation():
    """Verifies that async and sync engines are instantiated with proper dialects."""
    assert async_engine is not None
    assert async_engine.dialect.name == "postgresql"
    assert sync_engine is not None
    assert sync_engine.dialect.name == "postgresql"
