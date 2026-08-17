"""
Pydantic Schemas for In-App Notifications
"""

from typing import Optional
from pydantic import BaseModel, Field


class NotificationResponse(BaseModel):
    notification_id: str
    recipient_role: str = "ALL"
    title: str
    message: str
    severity: str = "INFO"
    related_alert_id: Optional[str] = None
    is_read: bool = False
    created_at: str
    read_at: Optional[str] = None


class NotificationListResponse(BaseModel):
    total_notifications: int
    unread_count: int
    notifications: list[NotificationResponse]
