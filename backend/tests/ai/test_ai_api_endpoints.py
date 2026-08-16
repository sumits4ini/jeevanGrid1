"""
Integration Tests for FastAPI /api/v1/ai Endpoints
"""

from fastapi.testclient import TestClient


def test_get_ai_status(client: TestClient):
    """Verifies GET /api/v1/ai/status endpoint."""
    response = client.get("/api/v1/ai/status")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ready"


def test_post_ai_risk_analysis(client: TestClient):
    """Verifies POST /api/v1/ai/risk-analysis endpoint."""
    payload = {
        "disaster_name": "Assam Brahmaputra Inundation 2026",
        "disaster_type": "FLOOD",
        "severity_level": 4,
        "latitude": 26.3216,
        "longitude": 91.0063,
        "affected_population_estimate": 85400,
        "inundation_depth_m": 1.25,
    }
    response = client.post("/api/v1/ai/risk-analysis", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert "risk_score" in data
    assert data["risk_level"] in ["HIGH", "CRITICAL"]
    assert len(data["risk_factors"]) > 0


def test_post_ai_resource_priority(client: TestClient):
    """Verifies POST /api/v1/ai/resource-priority endpoint."""
    payload = {
        "target_latitude": 26.3216,
        "target_longitude": 91.0063,
        "disaster_type": "FLOOD",
        "severity_level": 4,
        "max_search_radius_km": 50.0,
        "limit": 10,
    }
    response = client.post("/api/v1/ai/resource-priority", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert "prioritized_resources" in data
    assert len(data["prioritized_resources"]) > 0


def test_post_ai_recommendations(client: TestClient):
    """Verifies POST /api/v1/ai/recommendations endpoint."""
    payload = {
        "disaster_type": "FLOOD",
        "severity_level": 4,
        "latitude": 26.3216,
        "longitude": 91.0063,
    }
    response = client.post("/api/v1/ai/recommendations", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0


def test_post_ai_risk_analysis_invalid_severity(client: TestClient):
    """Verifies validation error on invalid severity level (> 5)."""
    payload = {
        "disaster_type": "FLOOD",
        "severity_level": 10,  # Invalid
        "latitude": 26.3216,
        "longitude": 91.0063,
    }
    response = client.post("/api/v1/ai/risk-analysis", json=payload)
    assert response.status_code == 422
