"""
Unit Tests for SQLAlchemy / PostGIS Database Models
"""

import uuid
from backend.app.models.disaster import Disaster
from backend.app.models.location import CriticalInfrastructure
from backend.app.models.resource import ResponseUnit
from backend.app.models.risk_zone import HazardZone


def test_disaster_model_attributes():
    """Verifies Disaster model definition, table name, and columns."""
    assert Disaster.__tablename__ == "disasters"
    disaster_id = uuid.uuid4()
    disaster = Disaster(
        id=disaster_id,
        name="Assam Flash Flood 2026",
        disaster_type="FLOOD",
        severity_level=4,
        status="ACTIVE",
        location="POINT(91.0063 26.3216)",
        affected_population_estimate=45000,
    )
    assert disaster.id == disaster_id
    assert disaster.name == "Assam Flash Flood 2026"
    assert disaster.severity_level == 4
    assert disaster.status == "ACTIVE"


def test_critical_infrastructure_model_attributes():
    """Verifies CriticalInfrastructure model definition and columns."""
    assert CriticalInfrastructure.__tablename__ == "critical_infrastructure"
    facility = CriticalInfrastructure(
        name="Barpeta Civil Hospital",
        facility_type="HOSPITAL",
        operational_status="OPERATIONAL",
        location="POINT(91.0092 26.3245)",
        max_capacity=350,
        current_occupancy=120,
        backup_power_hours=24.0,
    )
    assert facility.name == "Barpeta Civil Hospital"
    assert facility.facility_type == "HOSPITAL"
    assert facility.max_capacity == 350


def test_response_unit_model_attributes():
    """Verifies ResponseUnit model definition, capacity payload, and columns."""
    assert ResponseUnit.__tablename__ == "response_units"
    unit = ResponseUnit(
        unit_code="NDRF-BN-01",
        unit_type="RESCUE_BOAT",
        status="AVAILABLE",
        location="POINT(91.0200 26.3100)",
        capacity_payload={"boat_capacity": 12, "medics": 2},
    )
    assert unit.unit_code == "NDRF-BN-01"
    assert unit.unit_type == "RESCUE_BOAT"
    assert unit.capacity_payload["boat_capacity"] == 12


def test_hazard_zone_model_attributes():
    """Verifies HazardZone model definition and foreign key relationship."""
    assert HazardZone.__tablename__ == "hazard_zones"
    disaster_id = uuid.uuid4()
    zone = HazardZone(
        disaster_id=disaster_id,
        name="Sector East Inundation Zone",
        polygon_geom="MULTIPOLYGON(((91.00 26.30, 91.05 26.30, 91.05 26.35, 91.00 26.35, 91.00 26.30)))",
        inundation_depth_m=1.25,
        hazard_intensity=0.85,
        risk_level="CRITICAL",
        is_active=True,
    )
    assert zone.disaster_id == disaster_id
    assert zone.inundation_depth_m == 1.25
    assert zone.risk_level == "CRITICAL"
    assert zone.is_active is True
