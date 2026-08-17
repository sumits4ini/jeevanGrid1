"""
Integration Tests for FastAPI /api/v1/optimization Endpoints
"""

from fastapi.testclient import TestClient


def test_post_prioritize_incidents_api(client: TestClient):
    """Verifies POST /api/v1/optimization/prioritize-incidents."""
    payload = {
        "incidents": [
            {
                "id": "inc-01",
                "name": "Barpeta Lowland Breach",
                "disaster_type": "FLOOD",
                "severity_level": 5,
                "latitude": 26.3216,
                "longitude": 91.0063,
                "affected_population": 85000,
                "inundation_depth_m": 1.5,
            },
            {
                "id": "inc-02",
                "name": "Guwahati Urban Drain Clog",
                "disaster_type": "FLOOD",
                "severity_level": 2,
                "latitude": 26.1445,
                "longitude": 91.7362,
                "affected_population": 2000,
            },
        ]
    }
    response = client.post("/api/v1/optimization/prioritize-incidents", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["total_incidents"] == 2
    assert data["prioritized_incidents"][0]["incident_id"] == "inc-01"


def test_post_allocate_resources_api(client: TestClient):
    """Verifies POST /api/v1/optimization/allocate-resources."""
    payload = {
        "incidents": [
            {
                "id": "inc-01",
                "name": "Sector Flood",
                "disaster_type": "FLOOD",
                "severity_level": 4,
                "latitude": 26.3216,
                "longitude": 91.0063,
                "affected_population": 50000,
            }
        ],
        "max_search_radius_km": 50.0,
    }
    response = client.post("/api/v1/optimization/allocate-resources", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "assignments" in body["data"]


def test_post_response_plan_api(client: TestClient):
    """Verifies POST /api/v1/optimization/response-plan."""
    payload = {
        "incidents": [
            {
                "id": "inc-01",
                "name": "Assam Flood Sector East",
                "disaster_type": "FLOOD",
                "severity_level": 4,
                "latitude": 26.3216,
                "longitude": 91.0063,
                "affected_population": 85000,
                "inundation_depth_m": 1.2,
            }
        ],
        "max_search_radius_km": 50.0,
        "include_ai_advisory": True,
    }
    response = client.post("/api/v1/optimization/response-plan", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert "deployment_sequence" in data
    assert "plan_summary" in data


def test_get_resource_status_api(client: TestClient):
    """Verifies GET /api/v1/optimization/resource-status."""
    response = client.get("/api/v1/optimization/resource-status")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert "total_units" in data
    assert "readiness_percentage" in data


def test_get_incidents_resources_api(client: TestClient):
    """Verifies GET /api/v1/optimization/incidents/{id}/resources."""
    response = client.get(
        "/api/v1/optimization/incidents/inc-01/resources",
        params={"lat": 26.3216, "lng": 91.0063, "radius_km": 25.0},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "resources" in body["data"]
