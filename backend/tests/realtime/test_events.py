"""
Unit Tests for Operational Event Ingestion & Automated Rule Dispatch
"""

import pytest
from realtime_operations.schemas.events import (
    EventTypeEnum,
    OperationalEventCreate,
)
from realtime_operations.services.alert_engine import alert_engine
from realtime_operations.services.event_service import event_service


@pytest.mark.asyncio
async def test_ingest_event_basic():
    """Verifies operational event ingestion and persistence."""
    event_in = OperationalEventCreate(
        event_type=EventTypeEnum.DISASTER_CREATED,
        entity_type="disaster",
        entity_id="dis-test-01",
        severity="HIGH",
        source="GIS_ENGINE",
        latitude=26.3216,
        longitude=91.0063,
        payload={"incident_name": "Test Flash Flood"},
    )
    result = await event_service.ingest_event(event_in)
    assert result.event_id.startswith("evt-")
    assert result.event_type == EventTypeEnum.DISASTER_CREATED
    assert result.entity_id == "dis-test-01"


@pytest.mark.asyncio
async def test_ingest_critical_risk_triggers_automated_alert():
    """Verifies that high/critical risk events automatically trigger a tactical alert."""
    initial_alerts_count = len(alert_engine.list_alerts())

    event_in = OperationalEventCreate(
        event_type=EventTypeEnum.RISK_LEVEL_CHANGED,
        entity_type="disaster",
        entity_id="dis-test-escalation-99",
        severity="CRITICAL",
        source="AI_SERVICES",
        latitude=26.3216,
        longitude=91.0063,
        payload={"risk_score": 0.95, "risk_level": "CRITICAL"},
    )
    await event_service.ingest_event(event_in)

    new_alerts_count = len(alert_engine.list_alerts())
    assert new_alerts_count >= initial_alerts_count + 1
