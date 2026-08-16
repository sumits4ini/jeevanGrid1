"""
Integration Tests for API v1 Routers, Validation, and Exception Handlers
"""

from fastapi.testclient import TestClient


def test_disasters_router_list(client: TestClient):
    """Verifies GET /api/v1/disasters returns 200 OK and valid envelope."""
    response = client.get("/api/v1/disasters")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_disaster_summary_overview(client: TestClient):
    """Verifies GET /api/v1/disasters/summary/overview returns COP aggregate metrics."""
    response = client.get("/api/v1/disasters/summary/overview")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "total_active_disasters" in body["data"]


def test_disaster_not_found_exception(client: TestClient):
    """Verifies GET /api/v1/disasters/{id} returns 404 with structured error envelope."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/disasters/{fake_uuid}")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["error_code"] == "ENTITY_NOT_FOUND"
    assert "Disaster with ID" in body["message"]


def test_disaster_creation_validation_error(client: TestClient):
    """Verifies POST /api/v1/disasters fails with 422 on invalid payload."""
    invalid_payload = {
        "name": "",  # Min length violation
        "disaster_type": "INVALID_TYPE",
        "severity_level": 99,  # Must be between 1 and 5
        "latitude": 999.0,  # Must be <= 90.0
        "longitude": 999.0,
    }
    response = client.post("/api/v1/disasters", json=invalid_payload)
    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error_code"] == "UNPROCESSABLE_ENTITY"
    assert "errors" in body["details"]


def test_disaster_creation_success(client: TestClient):
    """Verifies POST /api/v1/disasters succeeds with valid payload."""
    valid_payload = {
        "name": "Barpeta Monsoon Flash Flood 2026",
        "disaster_type": "FLOOD",
        "severity_level": 4,
        "status": "ACTIVE",
        "description": "Severe Brahmaputra river overflow affecting low-lying wards.",
        "latitude": 26.3216,
        "longitude": 91.0063,
    }
    response = client.post("/api/v1/disasters", json=valid_payload)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Barpeta Monsoon Flash Flood 2026"
    assert body["data"]["severity_level"] == 4


def test_locations_infrastructure_list(client: TestClient):
    """Verifies GET /api/v1/locations/infrastructure returns 200 OK."""
    response = client.get("/api/v1/locations/infrastructure")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_resources_units_list(client: TestClient):
    """Verifies GET /api/v1/resources/units returns 200 OK."""
    response = client.get("/api/v1/resources/units")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_risk_categories(client: TestClient):
    """Verifies GET /api/v1/risk/categories returns expected UNDRR tiers."""
    response = client.get("/api/v1/risk/categories")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "CRITICAL" in body["data"]
    assert "HIGH" in body["data"]


def test_gis_hazard_zones(client: TestClient):
    """Verifies GET /api/v1/gis/hazard-zones returns GeoJSON FeatureCollection."""
    response = client.get("/api/v1/gis/hazard-zones")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["type"] == "FeatureCollection"
