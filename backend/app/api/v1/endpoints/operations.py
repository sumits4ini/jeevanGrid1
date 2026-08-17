"""
Real-Time Emergency Operations, Tactical Alerts & Telemetry WebSocket Endpoints (Phase 8)
"""

from typing import Any, Dict, List, Optional
from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
)

from backend.app.core.logging import logger
from backend.app.schemas.common import ApiResponse
from realtime_operations.schemas.alerts import (
    AlertAcknowledgeRequest,
    AlertCategoryEnum,
    AlertCreate,
    AlertResolveRequest,
    AlertResponse,
    AlertSeverityEnum,
    AlertStatusEnum,
)
from realtime_operations.schemas.events import (
    EventTypeEnum,
    OperationalEventCreate,
    OperationalEventResponse,
)
from realtime_operations.schemas.notifications import (
    NotificationListResponse,
    NotificationResponse,
)
from realtime_operations.schemas.operations_status import OperationsStatusResponse
from realtime_operations.services.alert_engine import alert_engine
from realtime_operations.services.event_service import event_service
from realtime_operations.services.notification_service import notification_service
from realtime_operations.services.operations_status_service import operations_status_service
from realtime_operations.websocket.connection_manager import connection_manager

router = APIRouter(tags=["Real-Time Emergency Operations"])


# -----------------------------------------------------------------------------
# Operations Status
# -----------------------------------------------------------------------------

@router.get(
    "/operations/status",
    response_model=ApiResponse[OperationsStatusResponse],
    status_code=status.HTTP_200_OK,
    summary="Unified Emergency Operations Status & Telemetry Overview",
)
async def get_operations_status() -> ApiResponse[OperationsStatusResponse]:
    """Provides aggregated incident counts, alert levels, response fleet metrics, and system readiness."""
    status_data = operations_status_service.get_status()
    return ApiResponse(
        success=True,
        message=f"Retrieved operational status ({status_data.system_readiness_status}).",
        data=status_data,
    )


# -----------------------------------------------------------------------------
# Operational Events
# -----------------------------------------------------------------------------

@router.get(
    "/events",
    response_model=ApiResponse[List[OperationalEventResponse]],
    status_code=status.HTTP_200_OK,
    summary="List Operational Lifecycle Events",
)
async def list_operational_events(
    event_type: Optional[EventTypeEnum] = None,
    severity: Optional[str] = None,
    entity_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
) -> ApiResponse[List[OperationalEventResponse]]:
    """Lists recent operational events with optional filtering."""
    events = event_service.list_events(
        event_type=event_type,
        severity=severity,
        entity_type=entity_type,
        limit=limit,
    )
    return ApiResponse(
        success=True,
        message=f"Retrieved {len(events)} operational events.",
        data=events,
    )


@router.post(
    "/events",
    response_model=ApiResponse[OperationalEventResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Ingest Operational Event & Trigger Alert Rules",
)
async def ingest_operational_event(
    payload: OperationalEventCreate,
) -> ApiResponse[OperationalEventResponse]:
    """Ingests an operational lifecycle event and evaluates alert rules."""
    result = await event_service.ingest_event(payload)
    return ApiResponse(
        success=True,
        message=f"Ingested event '{result.event_id}' [{result.event_type.value}].",
        data=result,
    )


# -----------------------------------------------------------------------------
# Tactical Alerts
# -----------------------------------------------------------------------------

@router.get(
    "/alerts",
    response_model=ApiResponse[List[AlertResponse]],
    status_code=status.HTTP_200_OK,
    summary="List Tactical Alerts with Deduplication",
)
async def list_tactical_alerts(
    alert_status: Optional[AlertStatusEnum] = Query(None, alias="status"),
    severity: Optional[AlertSeverityEnum] = None,
    category: Optional[AlertCategoryEnum] = None,
) -> ApiResponse[List[AlertResponse]]:
    """Returns active, acknowledged, or resolved tactical alerts."""
    alerts = alert_engine.list_alerts(
        status=alert_status,
        severity=severity,
        category=category,
    )
    return ApiResponse(
        success=True,
        message=f"Retrieved {len(alerts)} tactical alerts.",
        data=alerts,
    )


@router.post(
    "/alerts",
    response_model=ApiResponse[AlertResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create or Deduplicate Tactical Alert",
)
async def create_tactical_alert(
    payload: AlertCreate,
) -> ApiResponse[AlertResponse]:
    """Creates a new tactical alert or increments occurrence count if deduplicated."""
    alert = await alert_engine.create_alert(payload)
    return ApiResponse(
        success=True,
        message=f"Tactical alert '{alert.alert_id}' processed (Occurrences: {alert.occurrence_count}).",
        data=alert,
    )


@router.get(
    "/alerts/{alert_id}",
    response_model=ApiResponse[AlertResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Specific Tactical Alert Details",
)
async def get_tactical_alert(alert_id: str) -> ApiResponse[AlertResponse]:
    """Fetches details for a single tactical alert."""
    alert = alert_engine.get_alert(alert_id)
    return ApiResponse(
        success=True,
        message=f"Retrieved tactical alert '{alert_id}'.",
        data=alert,
    )


@router.post(
    "/alerts/{alert_id}/acknowledge",
    response_model=ApiResponse[AlertResponse],
    status_code=status.HTTP_200_OK,
    summary="Acknowledge Tactical Alert",
)
async def acknowledge_tactical_alert(
    alert_id: str,
    payload: AlertAcknowledgeRequest,
) -> ApiResponse[AlertResponse]:
    """Transitions a tactical alert to ACKNOWLEDGED status."""
    alert = await alert_engine.acknowledge_alert(alert_id, payload)
    return ApiResponse(
        success=True,
        message=f"Tactical alert '{alert_id}' acknowledged by '{payload.acknowledged_by}'.",
        data=alert,
    )


@router.post(
    "/alerts/{alert_id}/resolve",
    response_model=ApiResponse[AlertResponse],
    status_code=status.HTTP_200_OK,
    summary="Resolve Tactical Alert",
)
async def resolve_tactical_alert(
    alert_id: str,
    payload: AlertResolveRequest,
) -> ApiResponse[AlertResponse]:
    """Transitions a tactical alert to RESOLVED status with resolution notes."""
    alert = await alert_engine.resolve_alert(alert_id, payload)
    return ApiResponse(
        success=True,
        message=f"Tactical alert '{alert_id}' resolved by '{payload.resolved_by}'.",
        data=alert,
    )


# -----------------------------------------------------------------------------
# In-App Notifications
# -----------------------------------------------------------------------------

@router.get(
    "/notifications",
    response_model=ApiResponse[NotificationListResponse],
    status_code=status.HTTP_200_OK,
    summary="List In-App Notifications with Unread Count",
)
async def list_notifications(
    unread_only: bool = Query(False),
) -> ApiResponse[NotificationListResponse]:
    """Returns in-app incident command notifications."""
    result = notification_service.list_notifications(unread_only=unread_only)
    return ApiResponse(
        success=True,
        message=f"Retrieved {result.total_notifications} notifications ({result.unread_count} unread).",
        data=result,
    )


@router.post(
    "/notifications/{notification_id}/read",
    response_model=ApiResponse[NotificationResponse],
    status_code=status.HTTP_200_OK,
    summary="Mark Notification as Read",
)
async def mark_notification_read(notification_id: str) -> ApiResponse[NotificationResponse]:
    """Marks a single notification as read."""
    notif = notification_service.mark_as_read(notification_id)
    return ApiResponse(
        success=True,
        message=f"Notification '{notification_id}' marked as read.",
        data=notif,
    )


@router.post(
    "/notifications/mark-all-read",
    response_model=ApiResponse[Dict[str, int]],
    status_code=status.HTTP_200_OK,
    summary="Mark All Notifications as Read",
)
async def mark_all_notifications_read() -> ApiResponse[Dict[str, int]]:
    """Marks all unread in-app notifications as read."""
    count = notification_service.mark_all_as_read()
    return ApiResponse(
        success=True,
        message=f"Marked {count} notifications as read.",
        data={"marked_read_count": count},
    )


# -----------------------------------------------------------------------------
# WebSocket Telemetry Stream
# -----------------------------------------------------------------------------

@router.websocket("/ws/operations")
async def websocket_operations_endpoint(websocket: WebSocket) -> None:
    """
    Real-time bidirectional WebSocket stream for dashboard telemetry,
    live incident updates, risk escalations, and tactical alerts.
    """
    await connection_manager.connect(websocket)
    try:
        while True:
            # Receive client ping or heartbeat / command messages
            data = await websocket.receive_text()
            # Respond to client ping with pong heartbeat
            if "ping" in data.lower():
                await websocket.send_json({"type": "PONG", "status": "ALIVE"})
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket)
    except Exception as exc:
        logger.debug(f"WebSocket client error: {exc}")
        await connection_manager.disconnect(websocket)
