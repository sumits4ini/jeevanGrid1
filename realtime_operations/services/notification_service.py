"""
Notification Service for In-App Incident Command Advisories
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from backend.app.core.logging import logger
from realtime_operations.exceptions import NotificationNotFoundException
from realtime_operations.schemas.notifications import (
    NotificationListResponse,
    NotificationResponse,
)
from realtime_operations.websocket.connection_manager import connection_manager


class NotificationService:
    """Manages in-app operational notifications with read-state tracking."""

    def __init__(self):
        self._notifications: Dict[str, Dict[str, Any]] = {}
        self._seed_default_notifications()

    def _seed_default_notifications(self) -> None:
        """Seeds initial operational notifications for dashboard readiness."""
        default_items = [
            {
                "notification_id": "notif-01",
                "recipient_role": "EOC_COMMANDER",
                "title": "Severe Flood Inundation Alert — Barpeta Sector East",
                "message": "Water levels exceeded 1.25m benchmark at Ward 4 residential cluster.",
                "severity": "CRITICAL",
                "related_alert_id": "alert-01",
                "is_read": False,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "read_at": None,
            },
            {
                "notification_id": "notif-02",
                "recipient_role": "DISPATCHER",
                "title": "NDRF Rescue Fleet Dispatched",
                "message": "Boats Alpha-1 and Alpha-2 mobilized to eastern riverine slipway.",
                "severity": "INFO",
                "related_alert_id": None,
                "is_read": False,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "read_at": None,
            },
            {
                "notification_id": "notif-03",
                "recipient_role": "ALL",
                "title": "Hospital Backup Power Reserve Alert",
                "message": "Civil Hospital primary substation on backup fuel reserves (6h remaining).",
                "severity": "HIGH",
                "related_alert_id": "alert-02",
                "is_read": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "read_at": datetime.now(timezone.utc).isoformat(),
            },
        ]
        for item in default_items:
            self._notifications[item["notification_id"]] = item

    async def create_notification(
        self,
        title: str,
        message: str,
        severity: str = "INFO",
        recipient_role: str = "ALL",
        related_alert_id: Optional[str] = None,
    ) -> NotificationResponse:
        notif_id = f"notif-{uuid.uuid4().hex[:8]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "notification_id": notif_id,
            "recipient_role": recipient_role,
            "title": title,
            "message": message,
            "severity": severity,
            "related_alert_id": related_alert_id,
            "is_read": False,
            "created_at": now_iso,
            "read_at": None,
        }
        self._notifications[notif_id] = record

        response = NotificationResponse(**record)
        # Broadcast over WebSocket
        await connection_manager.broadcast_notification(response.model_dump())
        logger.info(f"Created in-app notification '{notif_id}': {title}")
        return response

    def list_notifications(self, unread_only: bool = False) -> NotificationListResponse:
        items = list(self._notifications.values())
        if unread_only:
            items = [i for i in items if not i["is_read"]]

        # Sort descending by created_at
        items.sort(key=lambda x: x["created_at"], reverse=True)

        unread_count = sum(1 for i in self._notifications.values() if not i["is_read"])
        responses = [NotificationResponse(**i) for i in items]

        return NotificationListResponse(
            total_notifications=len(responses),
            unread_count=unread_count,
            notifications=responses,
        )

    def mark_as_read(self, notification_id: str) -> NotificationResponse:
        if notification_id not in self._notifications:
            raise NotificationNotFoundException(notification_id)

        record = self._notifications[notification_id]
        record["is_read"] = True
        record["read_at"] = datetime.now(timezone.utc).isoformat()
        return NotificationResponse(**record)

    def mark_all_as_read(self) -> int:
        now_iso = datetime.now(timezone.utc).isoformat()
        count = 0
        for record in self._notifications.values():
            if not record["is_read"]:
                record["is_read"] = True
                record["read_at"] = now_iso
                count += 1
        return count


# Global singleton instance
notification_service = NotificationService()
