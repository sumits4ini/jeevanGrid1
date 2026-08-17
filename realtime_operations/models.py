"""
Real-Time Operations, Alerts & In-App Notification Entities with PostGIS Spatial Geometries
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, TimestampMixin


class OperationalEvent(Base, TimestampMixin):
    """Represents a discrete operational event (disaster update, fleet dispatch, risk escalation)."""

    __tablename__ = "operational_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        index=True,
    )
    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    entity_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    severity: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="INFO",
        index=True,
    )
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="SYSTEM",
        index=True,
    )

    # Optional PostGIS location of event
    location = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=True,
    )

    payload: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    def __repr__(self) -> str:
        return f"<OperationalEvent(id={self.id}, type='{self.event_type}', severity='{self.severity}')>"


class Alert(Base, TimestampMixin):
    """Represents an actionable tactical alert requiring EOC attention or field dispatch."""

    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    alert_code: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        index=True,
    )
    severity: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="WARNING",
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="ACTIVE",
        index=True,
    )
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="GENERAL",
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    entity_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    # Optional PostGIS spatial coordinates
    location = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=True,
    )

    recommended_action: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    deduplication_key: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )
    occurrence_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    resolution_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Alert(id={self.id}, code='{self.alert_code}', severity='{self.severity}', status='{self.status}')>"


class Notification(Base, TimestampMixin):
    """Represents a targeted in-app operational notification."""

    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    recipient_role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ALL",
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    severity: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="INFO",
        index=True,
    )
    related_alert_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
    )
    read_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, title='{self.title}', is_read={self.is_read})>"
