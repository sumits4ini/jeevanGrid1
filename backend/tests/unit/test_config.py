"""
Unit Tests for Configuration and Settings Management
"""

from backend.app.core.config import Settings


def test_default_settings_instantiation():
    """Verifies that default settings load without error."""
    settings = Settings()
    assert settings.APP_NAME == "JeevanGrid Disaster Intelligence Platform"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.BACKEND_PORT == 8000
    assert len(settings.ALLOWED_CORS_ORIGINS) > 0


def test_cors_origins_parsing_from_csv():
    """Verifies that comma-separated CORS strings are properly parsed into lists."""
    test_origins = "http://example.com, https://jeevangrid.gov.in"
    settings = Settings(ALLOWED_CORS_ORIGINS=test_origins)
    assert len(settings.ALLOWED_CORS_ORIGINS) == 2
    assert "http://example.com" in settings.ALLOWED_CORS_ORIGINS
    assert "https://jeevangrid.gov.in" in settings.ALLOWED_CORS_ORIGINS
