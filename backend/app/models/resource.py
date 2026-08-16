"""
Response Units and Emergency Assets SQLAlchemy ORM Entity with PostGIS Spatial Point
"""

import uuid
from typing import Any, Dict, Optional
from geoalchemy2 import Geometry
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, TimestampMixin


class ResponseUnit(Base, TimestampMixin):
    """Represents an emergency rescue asset or battalion (NDRF boats, ambulances, supply trucks)."""

    __tablename__ = "response_units"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    unit_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )
    unit_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="AVAILABLE",
        index=True,
    )

    # PostGIS Point geometry (WGS84 SRID 4326)
    location = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )

    capacity_payload: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    assigned_incident_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<ResponseUnit(id={self.id}, code='{self.unit_code}', type='{self.unit_type}', status='{self.status}')>"
