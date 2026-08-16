"""
Disaster Schemas for API Request/Response Validation
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import Field
from backend.app.schemas.common import BaseSchema


class DisasterTypeEnum(str, Enum):
    FLOOD = "FLOOD"
    CYCLONE = "CYCLONE"
    LANDSLIDE = "LANDSLIDE"
    EARTHQUAKE = "EARTHQUAKE"
    URBAN_FIRE = "URBAN_FIRE"
    OTHER = "OTHER"


class DisasterStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    CONTAINED = "CONTAINED"
    RESOLVED = "RESOLVED"
    SIMULATED = "SIMULATED"


class DisasterBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=150, json_schema_extra={"example": "Assam Brahmaputra Flood 2026"})
    disaster_type: DisasterTypeEnum = Field(..., json_schema_extra={"example": DisasterTypeEnum.FLOOD})
    severity_level: int = Field(..., ge=1, le=5, json_schema_extra={"example": 4}, description="Severity rating 1 (Lowest) to 5 (Catastrophic)")
    status: DisasterStatusEnum = Field(default=DisasterStatusEnum.ACTIVE)
    description: Optional[str] = Field(None, max_length=1000)
    latitude: float = Field(..., ge=-90.0, le=90.0, json_schema_extra={"example": 26.3216})
    longitude: float = Field(..., ge=-180.0, le=180.0, json_schema_extra={"example": 91.0063})


class DisasterCreate(DisasterBase):
    pass


class DisasterUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    disaster_type: Optional[DisasterTypeEnum] = None
    severity_level: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[DisasterStatusEnum] = None
    description: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)


class DisasterResponse(DisasterBase):
    id: UUID = Field(default_factory=uuid4)
    affected_population_estimate: Optional[int] = Field(0, description="Estimated population in affected radius")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DisasterSummary(BaseSchema):
    total_active_disasters: int
    critical_alerts_count: int
    total_affected_population: int
    active_rescue_units: int
    disasters: List[DisasterResponse] = Field(default_factory=list)
