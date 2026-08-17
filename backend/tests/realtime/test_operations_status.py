"""
Unit Tests for Unified Operations Status Aggregation
"""

from realtime_operations.services.operations_status_service import operations_status_service


def test_operations_status_aggregation():
    """Verifies that operations status returns non-negative counters and valid readiness status."""
    status_data = operations_status_service.get_status()
    assert status_data.active_incidents >= 1
    assert status_data.critical_incidents >= 0
    assert status_data.active_alerts >= 0
    assert status_data.total_response_units >= 1
    assert status_data.available_response_units >= 0
    assert status_data.system_readiness_status in [
        "OPERATIONAL_NORMAL",
        "ELEVATED_TACTICAL_ALERT",
        "CRITICAL_DEFCON_1",
    ]
    assert status_data.last_sync_timestamp is not None
