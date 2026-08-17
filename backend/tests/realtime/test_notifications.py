"""
Unit Tests for In-App Notification Service & Read-State Tracking
"""

import pytest
from realtime_operations.services.notification_service import notification_service


@pytest.mark.asyncio
async def test_create_and_read_notification():
    """Verifies notification creation and mark-as-read mutation."""
    notif = await notification_service.create_notification(
        title="Test Emergency Fleet Mobilization",
        message="5 rescue units dispatched to Eastern Sector.",
        severity="INFO",
    )
    assert notif.notification_id.startswith("notif-")
    assert notif.is_read is False

    # Mark as read
    updated = notification_service.mark_as_read(notif.notification_id)
    assert updated.is_read is True
    assert updated.read_at is not None


def test_mark_all_notifications_as_read():
    """Verifies bulk mark all as read functionality."""
    count = notification_service.mark_all_as_read()
    list_res = notification_service.list_notifications()
    assert list_res.unread_count == 0
