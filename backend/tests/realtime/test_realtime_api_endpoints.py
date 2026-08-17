"""
Integration Tests for FastAPI Real-Time Operations REST Endpoints
"""

from fastapi.testclient import TestClient


def test_get_operations_status_api(client: TestClient):
    """Verifies GET /api/v1/operations/status."""
    response = client.get("/api/v1/operations/status")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert "active_incidents" in data
    assert "system_readiness_status" in data


def test_get_events_api(client: TestClient):
    """Verifies GET /api/v1/events."""
    response = client.get("/api/v1/events")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_post_event_api(client: TestClient):
    """Verifies POST /api/v1/events."""
    payload = {
        "event_type": "RESOURCE_ALLOCATED",
        "entity_type": "resource",
        "entity_id": "ru-boat-test",
        "severity": "INFO",
        "source": "OPTIMIZATION_ENGINE",
        "payload": {"allocated_to": "dis-01"},
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["event_id"].startswith("evt-")


def test_get_alerts_api(client: TestClient):
    """Verifies GET /api/v1/alerts."""
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) >= 1


def test_alert_acknowledge_and_resolve_api(client: TestClient):
    """Verifies POST /api/v1/alerts/{id}/acknowledge and /api/v1/alerts/{id}/resolve."""
    # 1. Create alert
    create_payload = {
        "alert_code": "TEST_ALERT_API",
        "severity": "CRITICAL",
        "category": "HYDROLOGICAL",
        "title": "API Test Surge Alert",
        "message": "Water levels rising rapidly in API test zone.",
        "entity_type": "disaster",
        "entity_id": "dis-api-test",
    }
    create_res = client.post("/api/v1/alerts", json=create_payload)
    assert create_res.status_code == 201
    alert_id = create_res.json()["data"]["alert_id"]

    # 2. Acknowledge
    ack_res = client.post(
        f"/api/v1/alerts/{alert_id}/acknowledge",
        json={"acknowledged_by": "COMMANDER_X", "notes": "Dispatched units"},
    )
    assert ack_res.status_code == 200
    assert ack_res.json()["data"]["status"] == "ACKNOWLEDGED"

    # 3. Resolve
    resolve_res = client.post(
        f"/api/v1/alerts/{alert_id}/resolve",
        json={"resolved_by": "COMMANDER_X", "resolution_notes": "Surge contained"},
    )
    assert resolve_res.status_code == 200
    assert resolve_res.json()["data"]["status"] == "RESOLVED"


def test_notifications_api(client: TestClient):
    """Verifies GET /api/v1/notifications and mark-all-read."""
    get_res = client.get("/api/v1/notifications")
    assert get_res.status_code == 200
    body = get_res.json()
    assert body["success"] is True
    assert "notifications" in body["data"]

    # Mark all read
    read_res = client.post("/api/v1/notifications/mark-all-read")
    assert read_res.status_code == 200
    assert read_res.json()["success"] is True
