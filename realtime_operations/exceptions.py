"""
Domain Exceptions for Real-Time Operations, Alerts & Notification Center
"""

from typing import Any, Dict, Optional
from backend.app.core.exceptions import JeevanGridException


class RealtimeOperationsException(JeevanGridException):
    """Base exception for real-time operations and alert failures."""

    def __init__(
        self,
        message: str = "Real-time operations failure occurred.",
        status_code: int = 422,
        error_code: str = "REALTIME_OPERATIONS_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=status_code,
            error_code=error_code,
            details=details,
        )


class AlertNotFoundException(RealtimeOperationsException):
    """Raised when an alert ID cannot be found."""

    def __init__(
        self,
        alert_id: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=f"Tactical Alert '{alert_id}' was not found.",
            status_code=404,
            error_code="ALERT_NOT_FOUND",
            details=details or {"alert_id": alert_id},
        )


class NotificationNotFoundException(RealtimeOperationsException):
    """Raised when a notification ID cannot be found."""

    def __init__(
        self,
        notification_id: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=f"Notification '{notification_id}' was not found.",
            status_code=404,
            error_code="NOTIFICATION_NOT_FOUND",
            details=details or {"notification_id": notification_id},
        )


class AlertLifecycleException(RealtimeOperationsException):
    """Raised when an invalid alert state transition is attempted."""

    def __init__(
        self,
        alert_id: str,
        current_status: str,
        target_status: str,
        reason: str = "Invalid alert transition.",
    ):
        super().__init__(
            message=f"Cannot transition alert '{alert_id}' from '{current_status}' to '{target_status}': {reason}",
            status_code=400,
            error_code="ALERT_LIFECYCLE_ERROR",
            details={"alert_id": alert_id, "current_status": current_status, "target_status": target_status},
        )


class InvalidEventPayloadException(RealtimeOperationsException):
    """Raised when an operational event has an invalid schema or corrupted payload."""

    def __init__(
        self,
        event_type: str,
        reason: str = "Malformed event payload.",
    ):
        super().__init__(
            message=f"Invalid event payload for '{event_type}': {reason}",
            status_code=422,
            error_code="INVALID_EVENT_PAYLOAD",
            details={"event_type": event_type, "reason": reason},
        )
