"""
Location & Critical Infrastructure Schemas
"""

from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import Field
from backend.app.schemas.common import BaseSchema


class FacilityTypeEnum(str, Enum):
    HOSPITAL = "HOSPITAL"
    POWER_SUBSTATION = "POWER_SUBSTATION"
    WATER_TREATMENT = "WATER_TREATMENT"
    BRIDGE = "BRIDGE"
    COMM_TOWER = "COMM_TOWER"
    SHELTER = "SHELTER"
    FIRE_STATION = "FIRE_STATION"
    POLICE_STATION = "POLICE_STATION"


class OperationalStatusEnum(str, Enum):
    OPERATIONAL = "OPERATIONAL"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    CUT_OFF = "CUT_OFF"
    UNKNOWN = "UNKNOWN"


class CriticalInfrastructureBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=150, json_schema_extra={"example": "Barpeta Civil Hospital"})
    facility_type: FacilityTypeEnum = Field(..., json_schema_extra={"example": FacilityTypeEnum.HOSPITAL})
    operational_status: OperationalStatusEnum = Field(default=OperationalStatusEnum.OPERATIONAL)
    latitude: float = Field(..., ge=-90.0, le=90.0, json_schema_extra={"example": 26.3245})
    longitude: float = Field(..., ge=-180.0, le=180.0, json_schema_extra={"example": 91.0092})
    max_capacity: int = Field(default=0, ge=0, json_schema_extra={"example": 350})
    current_occupancy: int = Field(default=0, ge=0, json_schema_extra={"example": 120})
    backup_power_hours: float = Field(default=24.0, ge=0.0, json_schema_extra={"example": 12.0})
    contact_phone: Optional[str] = Field(None, json_schema_extra={"example": "+91-3665-252000"})


class CriticalInfrastructureCreate(CriticalInfrastructureBase):
    pass


class CriticalInfrastructureResponse(CriticalInfrastructureBase):
    id: UUID = Field(default_factory=uuid4)
    is_threatened: bool = Field(default=False, description="Flagged true if inside active hazard buffer")
    distance_to_nearest_hazard_m: Optional[float] = None
