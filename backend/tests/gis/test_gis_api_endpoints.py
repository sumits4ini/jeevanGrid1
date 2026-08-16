"""
Integration Tests for GIS API v1 Endpoints
"""

from fastapi.testclient import TestClient


def test_get_gis_layers(client: TestClient):
    """Verifies GET /api/v1/gis/layers returns registered layers."""
    response = client.get("/api/v1/gis/layers")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "layers" in body["data"]
    assert body["data"]["total_layers"] >= 4


def test_get_specific_gis_layer(client: TestClient):
    """Verifies GET /api/v1/gis/layers/infrastructure returns GeoJSON FeatureCollection."""
    response = client.get("/api/v1/gis/layers/infrastructure")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["type"] == "FeatureCollection"
    assert len(body["data"]["features"]) > 0


def test_get_nonexistent_gis_layer_returns_404(client: TestClient):
    """Verifies GET /api/v1/gis/layers/invalid_layer returns 404 Entity Not Found."""
    response = client.get("/api/v1/gis/layers/non_existent_satellite_feed")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["error_code"] == "ENTITY_NOT_FOUND"


def test_query_gis_features_with_bbox(client: TestClient):
    """Verifies GET /api/v1/gis/features with bounding box."""
    params = {
        "layers": ["infrastructure", "disasters"],
        "min_lng": 90.50,
        "min_lat": 26.00,
        "max_lng": 91.50,
        "max_lat": 26.80,
    }
    response = client.get("/api/v1/gis/features", params=params)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["type"] == "FeatureCollection"


def test_get_nearby_features(client: TestClient):
    """Verifies GET /api/v1/gis/nearby returns proximity-ranked items."""
    params = {
        "lat": 26.3216,
        "lng": 91.0063,
        "radius": 15000.0,
        "limit": 10,
    }
    response = client.get("/api/v1/gis/nearby", params=params)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["total_found"] > 0
    assert len(body["data"]["features"]) > 0


def test_get_nearby_features_invalid_coordinates(client: TestClient):
    """Verifies GET /api/v1/gis/nearby fails on invalid coordinate range."""
    params = {
        "lat": 150.0,  # Invalid latitude (> 90.0)
        "lng": 91.0063,
        "radius": 5000.0,
    }
    response = client.get("/api/v1/gis/nearby", params=params)
    assert response.status_code == 422


def test_compute_spatial_intersections(client: TestClient):
    """Verifies POST /api/v1/gis/intersections evaluates polygon intersections."""
    payload = {
        "target_geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [90.95, 26.30],
                    [91.05, 26.30],
                    [91.05, 26.35],
                    [90.95, 26.35],
                    [90.95, 26.30],
                ]
            ],
        },
        "intersect_layers": ["infrastructure", "response_units"],
        "buffer_meters": 500.0,
    }
    response = client.post("/api/v1/gis/intersections", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "results_by_layer" in body["data"]
    assert "infrastructure" in body["data"]["results_by_layer"]


def test_hazard_zones_compat_endpoint(client: TestClient):
    """Verifies GET /api/v1/gis/hazard-zones backward compatibility."""
    response = client.get("/api/v1/gis/hazard-zones")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["type"] == "FeatureCollection"
