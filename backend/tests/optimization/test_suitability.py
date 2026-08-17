"""
Unit Tests for Resource Suitability Scoring Engine
"""

from response_optimization.algorithms.suitability import calculate_resource_suitability
from response_optimization.schemas.incident_priority import IncidentItem


def test_resource_suitability_boat_for_flood():
    """Verifies rescue boat has high suitability for flood incident."""
    incident = IncidentItem(
        id="inc-01",
        name="Sector Flood",
        disaster_type="FLOOD",
        severity_level=4,
        latitude=26.3216,
        longitude=91.0063,
    )
    boat_resource = {
        "id": "res-boat-01",
        "unit_name": "NDRF Rescue Boat Alpha",
        "unit_type": "RESCUE_BOAT",
        "status": "AVAILABLE",
    }
    score, reason = calculate_resource_suitability(
        incident=incident,
        resource=boat_resource,
        distance_km=2.5,
        max_search_radius_km=50.0,
    )
    assert score >= 0.85
    assert "RESCUE_BOAT" in reason
    assert "FLOOD" in reason


def test_resource_suitability_distance_decay():
    """Verifies that distant units have lower suitability score."""
    incident = IncidentItem(
        id="inc-01",
        name="Sector Flood",
        disaster_type="FLOOD",
        severity_level=4,
        latitude=26.3216,
        longitude=91.0063,
    )
    boat_resource = {
        "id": "res-boat-02",
        "unit_name": "NDRF Boat Distant",
        "unit_type": "RESCUE_BOAT",
        "status": "AVAILABLE",
    }
    score_near, _ = calculate_resource_suitability(incident, boat_resource, distance_km=2.0)
    score_far, _ = calculate_resource_suitability(incident, boat_resource, distance_km=45.0)

    assert score_near > score_far
