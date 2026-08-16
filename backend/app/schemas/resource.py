"""
Emergency Response Resource & Unit Schemas
"""

from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import Field
from backend.app.schemas.common import BaseSchema


class UnitTypeEnum(str, Enum):
    NDRF_TEAM = "NDRF_TEAM"
    SDRF_TEAM = "SDRF_TEAM"
    AMBULANCE = "AMBULANCE"
    RESCUE_BOAT = "RESCUE_BOAT"
    FOOD_WATER_TRUCK = "FOOD_WATER_TRUCK"
    MOBILE_GENERATOR = "MOBILE_GENERATOR"
    DRONE_SURVEILLANCE = "DRONE_SURVEILLANCE"


class UnitStatusEnum(str, Enum):
    AVAILABLE = "AVAILABLE"
    DISPATCHED = "DISPATCHED"
    ON_MISSION = "ON_MISSION"
    MAINTENANCE = "MAINTENANCE"
    OFFLINE = "OFFLINE"


class ResponseUnitBase(BaseSchema):
    unit_code: str = Field(..., json_schema_extra={"example": "NDRF-BN-01"})
    unit_type: UnitTypeEnum = Field(..., json_schema_extra={"example": UnitTypeEnum.RESCUE_BOAT})
    status: UnitStatusEnum = Field(default=UnitStatusEnum.AVAILABLE)
    latitude: float = Field(..., ge=-90.0, le=90.0, json_schema_extra={"example": 26.3100})
    longitude: float = Field(..., ge=-180.0, le=180.0, json_schema_extra={"example": 91.0200})
    capacity_payload: Dict[str, Any] = Field(
        default_factory=dict,
        json_schema_extra={"example": {"boat_capacity": 12, "medics": 2, "life_jackets": 20}}
    )


class ResponseUnitCreate(ResponseUnitBase):
    pass


class ResponseUnitResponse(ResponseUnitBase):
    id: UUID = Field(default_factory=uuid4)
    assigned_incident_id: Optional[UUID] = None


class DispatchPlanRequest(BaseSchema):
    disaster_id: UUID
    priority_level: Optional[str] = "ALL"
    max_eta_minutes: float = Field(default=60.0, ge=5.0, le=360.0)


class DispatchAllocationItem(BaseSchema):
    allocation_id: UUID = Field(default_factory=uuid4)
    unit_id: UUID
    unit_code: str
    unit_type: UnitTypeEnum
    target_zone_name: str
    target_latitude: float
    target_longitude: float
    estimated_travel_time_minutes: float
    recommended_route_summary: str


class DispatchPlanResponse(BaseSchema):
    plan_id: UUID = Field(default_factory=uuid4)
    disaster_id: UUID
    total_units_allocated: int
    estimated_lives_stabilized: int
    allocations: list[DispatchAllocationItem] = Field(default_factory=list)
    solver_status: str = "OPTIMAL_FOUND"
    solver_execution_time_ms: float = 0.0
