"""
Critical Infrastructure and Locations SQLAlchemy ORM Entity with PostGIS Spatial Point
"""

import uuid
from typing import Optional
from geoalchemy2 import Geometry
from sqlalchemy import Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, TimestampMixin


class CriticalInfrastructure(Base, TimestampMixin):
    """Represents key facilities such as hospitals, power substations, water plants, bridges, and shelters."""

    __tablename__ = "critical_infrastructure"

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
    facility_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    operational_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="OPERATIONAL",
        index=True,
    )

    # PostGIS Point geometry (WGS84 SRID 4326)
    location = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )

    max_capacity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    current_occupancy: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    backup_power_hours: Mapped[float] = mapped_column(
        Float,
        default=24.0,
        nullable=False,
    )
    contact_phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<CriticalInfrastructure(id={self.id}, name='{self.name}', type='{self.facility_type}', status='{self.operational_status}')>"
