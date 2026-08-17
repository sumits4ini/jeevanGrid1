"""
Pydantic Schemas for Routing and Transit Estimation
"""

from typing import Optional
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


class RoutingRequest(BaseModel):
    origin: Coordinates
    destination: Coordinates
    vehicle_type: str = Field(default="RESCUE_BOAT", description="RESCUE_BOAT, AMBULANCE, NDRF_TEAM, TRUCK")
    avoid_hazards: bool = Field(default=True)
    average_speed_kmh: Optional[float] = Field(default=None, ge=5.0, le=150.0)


class RoutingResponse(BaseModel):
    origin: Coordinates
    destination: Coordinates
    straight_line_distance_km: float = Field(..., ge=0.0)
    estimated_route_distance_km: float = Field(..., ge=0.0)
    estimated_duration_minutes: int = Field(..., ge=0)
    is_estimated: bool = True
    provider_info: str
    routing_notes: Optional[str] = None
