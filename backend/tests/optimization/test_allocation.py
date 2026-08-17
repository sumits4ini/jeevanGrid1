"""
Unit Tests for Capacitated Resource Allocation Engine
"""

from response_optimization.algorithms.allocation import allocate_resources_deterministically
from response_optimization.schemas.incident_priority import IncidentItem


def test_allocate_resources_single_incident():
    """Verifies allocation matches best available units to single incident."""
    incidents = [
        IncidentItem(
            id="inc-01",
            name="Barpeta Lowland Flood",
            disaster_type="FLOOD",
            severity_level=4,
            latitude=26.3216,
            longitude=91.0063,
            affected_population=50000,
        )
    ]
    sample_resources = [
        {
            "id": "boat-01",
            "name": "Rescue Boat 1",
            "unit_type": "RESCUE_BOAT",
            "unit_code": "RB-01",
            "status": "AVAILABLE",
            "latitude": 26.3200,
            "longitude": 91.0080,
        },
        {
            "id": "boat-02",
            "name": "Rescue Boat 2",
            "unit_type": "RESCUE_BOAT",
            "unit_code": "RB-02",
            "status": "AVAILABLE",
            "latitude": 26.3150,
            "longitude": 91.0120,
        },
        {
            "id": "amb-01",
            "name": "Ambulance 108",
            "unit_type": "AMBULANCE",
            "unit_code": "AMB-01",
            "status": "AVAILABLE",
            "latitude": 26.3300,
            "longitude": 91.0200,
        },
    ]

    res = allocate_resources_deterministically(incidents, sample_resources)
    assert res.total_assignments >= 2
    # Verify no unit is double allocated
    assigned_ids = [a.resource_id for a in res.assignments]
    assert len(assigned_ids) == len(set(assigned_ids))


def test_allocate_resources_identifies_shortage():
    """Verifies shortage detection when demand exceeds available fleet."""
    incidents = [
        IncidentItem(
            id="inc-catastrophic",
            name="Catastrophic Basin Breach",
            disaster_type="FLOOD",
            severity_level=5,  # Demands 4 boats, 2 NDRF teams, 2 ambulances
            latitude=26.3216,
            longitude=91.0063,
        )
    ]
    # Only 1 boat available
    sparse_resources = [
        {
            "id": "boat-only-one",
            "name": "Lone Boat",
            "unit_type": "RESCUE_BOAT",
            "unit_code": "RB-LONE",
            "status": "AVAILABLE",
            "latitude": 26.3200,
            "longitude": 91.0080,
        }
    ]

    res = allocate_resources_deterministically(incidents, sparse_resources)
    assert res.total_shortages > 0
    shortage_types = [s.resource_type for s in res.shortages]
    assert "RESCUE_BOAT" in shortage_types
    # Boat shortage count should be 4 - 1 = 3
    boat_shortage = next(s for s in res.shortages if s.resource_type == "RESCUE_BOAT")
    assert boat_shortage.shortage_count == 3
    assert boat_shortage.quantity_allocated == 1
    assert "mutual aid" in boat_shortage.recommended_mitigation
