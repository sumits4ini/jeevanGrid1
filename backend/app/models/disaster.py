"""
Disaster SQLAlchemy ORM Entity with PostGIS Spatial Point Geometry
"""

import uuid
from typing import TYPE_CHECKING, List, Optional
from geoalchemy2 import Geometry
from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.app.models.risk_zone import HazardZone


class Disaster(Base, TimestampMixin):
    """Represents a discrete disaster incident (flood, cyclone, earthquake, etc.)."""

    __tablename__ = "disasters"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )
    disaster_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    severity_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ACTIVE",
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # PostGIS Point geometry (WGS84 SRID 4326)
    location = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )

    affected_population_estimate: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # Relationships
    hazard_zones: Mapped[List["HazardZone"]] = relationship(
        "HazardZone",
        back_populates="disaster",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Disaster(id={self.id}, name='{self.name}', type='{self.disaster_type}', severity={self.severity_level})>"
