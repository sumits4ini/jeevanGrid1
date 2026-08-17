"""
Unit Tests for Tactical Alert Engine, Deduplication & Lifecycle Actions
"""

import pytest
from realtime_operations.exceptions import AlertLifecycleException, AlertNotFoundException
from realtime_operations.schemas.alerts import (
    AlertAcknowledgeRequest,
    AlertCategoryEnum,
    AlertCreate,
    AlertResolveRequest,
    AlertSeverityEnum,
    AlertStatusEnum,
)
from realtime_operations.services.alert_engine import alert_engine


@pytest.mark.asyncio
async def test_create_and_deduplicate_alert():
    """Verifies that identical alert bursts are deduplicated via occurrence count."""
    payload = AlertCreate(
        alert_code="TEST_BRIDGE_COLLAPSE",
        severity=AlertSeverityEnum.CRITICAL,
        category=AlertCategoryEnum.INFRASTRUCTURE,
        title="Test Bridge Submerged",
        message="Bridge B-99 submerged under 1.1m of flood water.",
        entity_type="location",
        entity_id="loc-brg-99",
        latitude=26.3150,
        longitude=91.0120,
    )

    alert1 = await alert_engine.create_alert(payload)
    assert alert1.alert_id.startswith("alert-")
    assert alert1.occurrence_count == 1
    assert alert1.status == AlertStatusEnum.ACTIVE

    # Submit second identical alert
    alert2 = await alert_engine.create_alert(payload)
    assert alert2.alert_id == alert1.alert_id  # Same alert ID
    assert alert2.occurrence_count >= 2


@pytest.mark.asyncio
async def test_alert_lifecycle_acknowledge_and_resolve():
    """Verifies state transitions ACTIVE -> ACKNOWLEDGED -> RESOLVED."""
    payload = AlertCreate(
        alert_code="TEST_HOSPITAL_POWER",
        severity=AlertSeverityEnum.HIGH,
        category=AlertCategoryEnum.INFRASTRUCTURE,
        title="Test Hospital Generator Alarm",
        message="Hospital power unit low fuel.",
        entity_type="location",
        entity_id="loc-hosp-99",
    )
    alert = await alert_engine.create_alert(payload)

    # 1. Acknowledge
    ack_res = await alert_engine.acknowledge_alert(
        alert.alert_id,
        AlertAcknowledgeRequest(acknowledged_by="EOC_OPERATOR_1", notes="Dispatching fuel truck"),
    )
    assert ack_res.status == AlertStatusEnum.ACKNOWLEDGED
    assert ack_res.acknowledged_at is not None

    # 2. Resolve
    resolve_res = await alert_engine.resolve_alert(
        alert.alert_id,
        AlertResolveRequest(resolved_by="INCIDENT_COMMANDER", resolution_notes="Fuel tanker arrived and filled generator"),
    )
    assert resolve_res.status == AlertStatusEnum.RESOLVED
    assert resolve_res.resolved_at is not None

    # 3. Invalid transition from RESOLVED to ACKNOWLEDGED must raise AlertLifecycleException
    with pytest.raises(AlertLifecycleException):
        await alert_engine.acknowledge_alert(
            alert.alert_id,
            AlertAcknowledgeRequest(acknowledged_by="OPERATOR_2"),
        )
