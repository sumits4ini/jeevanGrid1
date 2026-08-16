"""
Integration Tests for Database Connectivity and Live Health Reporting
"""

import pytest
from backend.app.db.session import check_db_connectivity


@pytest.mark.asyncio
async def test_database_connectivity_checker_resilience():
    """Verifies that check_db_connectivity executes gracefully without unhandled exceptions."""
    is_connected, latency_ms, message = await check_db_connectivity()
    assert isinstance(is_connected, bool)
    assert isinstance(latency_ms, float)
    assert isinstance(message, str)
    assert latency_ms >= 0.0
    if is_connected:
        assert "PostgreSQL online" in message
    else:
        assert "Database connection unavailable" in message or "offline" in message.lower()
