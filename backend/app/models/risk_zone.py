"""
Hazard and Risk Zones SQLAlchemy ORM Entity with PostGIS MultiPolygon Geometry
"""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from geoalchemy2 import Geometry
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.app.models.disaster import Disaster


class HazardZone(Base, TimestampMixin):
    """Represents a spatial flood inundation polygon, fire perimeter, or landslide hazard zone."""

    __tablename__ = "hazard_zones"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    disaster_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("disasters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
    )

    # PostGIS MultiPolygon geometry (WGS84 SRID 4326)
    polygon_geom = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=True),
        nullable=False,
    )

    inundation_depth_m: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    hazard_intensity: Mapped[float] = mapped_column(
        Float,
        default=0.5,
        nullable=False,
    )
    risk_level: Mapped[str] = mapped_column(
        String(50),
        default="MODERATE",
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    disaster: Mapped["Disaster"] = relationship(
        "Disaster",
        back_populates="hazard_zones",
    )

    def __repr__(self) -> str:
        return f"<HazardZone(id={self.id}, disaster_id={self.disaster_id}, depth={self.inundation_depth_m}m, risk='{self.risk_level}')>"
