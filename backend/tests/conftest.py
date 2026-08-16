"""
Pytest Test Configuration and Fixtures for JeevanGrid Backend
"""

import os
import pytest
from fastapi.testclient import TestClient
from backend.app.core.config import Settings, get_settings
from backend.app.main import create_application


@pytest.fixture(scope="session", autouse=True)
def set_test_environment():
    """Sets environment variables specifically for testing."""
    os.environ["APP_ENV"] = "testing"
    os.environ["DEBUG"] = "true"
    os.environ["ENABLE_DEMO_SIMULATION_MODE"] = "true"
    os.environ["SECRET_KEY"] = "test-secret-key-min-32-chars-for-testing-suite"


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Provides test-specific settings instance."""
    return get_settings()


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Provides a synchronous FastAPI TestClient instance."""
    app = create_application()
    with TestClient(app) as test_client:
        yield test_client
