"""
Integration Tests for System Health Check Endpoints
"""

from fastapi.testclient import TestClient


def test_root_health_endpoint(client: TestClient):
    """Verifies that GET /health returns 200 OK with expected health payload."""
    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert "data" in body

    data = body["data"]
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "app_version" in data
    assert "services" in data
    assert "api_gateway" in data["services"]
    assert data["services"]["api_gateway"]["status"] == "healthy"


def test_v1_health_endpoint(client: TestClient):
    """Verifies that GET /api/v1/health returns identical 200 OK status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "healthy"


def test_root_landing_endpoint(client: TestClient):
    """Verifies GET / root documentation landing."""
    response = client.get("/")
    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["data"]["docs_url"] == "/docs"
    assert body["data"]["health_check"] == "/health"
