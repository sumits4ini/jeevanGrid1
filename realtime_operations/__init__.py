"""
JeevanGrid Real-Time Emergency Operations, Alerts & Command Center Core
"""

from realtime_operations.exceptions import (
    AlertLifecycleException,
    AlertNotFoundException,
    InvalidEventPayloadException,
    NotificationNotFoundException,
    RealtimeOperationsException,
)
from realtime_operations.models import Alert, Notification, OperationalEvent
from realtime_operations.schemas import (
    AlertAcknowledgeRequest,
    AlertCategoryEnum,
    AlertCreate,
    AlertResolveRequest,
    AlertResponse,
    AlertSeverityEnum,
    AlertStatusEnum,
    EventTypeEnum,
    NotificationListResponse,
    NotificationResponse,
    OperationalEventCreate,
    OperationalEventResponse,
    OperationsStatusResponse,
)
from realtime_operations.services import (
    AlertEngine,
    NotificationService,
    OperationalEventService,
    OperationsStatusService,
    alert_engine,
    event_service,
    notification_service,
    operations_status_service,
)
from realtime_operations.websocket import ConnectionManager, connection_manager

__version__ = "0.1.0"

__all__ = [
    "OperationalEvent",
    "Alert",
    "Notification",
    "EventTypeEnum",
    "OperationalEventCreate",
    "OperationalEventResponse",
    "AlertSeverityEnum",
    "AlertStatusEnum",
    "AlertCategoryEnum",
    "AlertCreate",
    "AlertAcknowledgeRequest",
    "AlertResolveRequest",
    "AlertResponse",
    "NotificationResponse",
    "NotificationListResponse",
    "OperationsStatusResponse",
    "RealtimeOperationsException",
    "AlertNotFoundException",
    "NotificationNotFoundException",
    "AlertLifecycleException",
    "InvalidEventPayloadException",
    "ConnectionManager",
    "connection_manager",
    "AlertEngine",
    "alert_engine",
    "OperationalEventService",
    "event_service",
    "NotificationService",
    "notification_service",
    "OperationsStatusService",
    "operations_status_service",
]
