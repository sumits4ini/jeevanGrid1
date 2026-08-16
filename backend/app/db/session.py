"""
SQLAlchemy Engine, Session Factories, and Database Connectivity Verification
"""

import time
from typing import AsyncGenerator, Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from backend.app.core.config import settings
from backend.app.core.logging import logger

# 1. Asynchronous Database Engine & Session Factory (Primary API engine)
async_engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG and settings.APP_ENV == "development",
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 2. Synchronous Database Engine & Session Factory (For Alembic migrations & sync scripts)
sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection generator yielding an active AsyncSession."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> Session:
    """Provides a synchronous database session."""
    db = SyncSessionLocal()
    try:
        return db
    finally:
        db.close()


async def check_db_connectivity() -> Tuple[bool, float, str]:
    """
    Asynchronously checks PostgreSQL connectivity and PostGIS extension status.
    Returns:
        (is_connected: bool, latency_ms: float, message: str)
    """
    start_time = time.perf_counter()
    try:
        async with async_engine.connect() as conn:
            # Query PostGIS version if available
            result = await conn.execute(text("SELECT postgis_version();"))
            row = result.fetchone()
            postgis_ver = row[0] if row else "unknown"
            latency = (time.perf_counter() - start_time) * 1000.0
            return True, round(latency, 2), f"PostgreSQL online with PostGIS v{postgis_ver}"
    except Exception as exc:
        latency = (time.perf_counter() - start_time) * 1000.0
        # If postgis_version() specifically failed but DB is reachable
        err_msg = str(exc)
        if "postgis_version" in err_msg.lower():
            return True, round(latency, 2), "PostgreSQL online (PostGIS extension not yet installed)"
        logger.debug(f"Database connectivity check failed: {err_msg}")
        return False, round(latency, 2), f"Database connection unavailable: {err_msg.splitlines()[0]}"
