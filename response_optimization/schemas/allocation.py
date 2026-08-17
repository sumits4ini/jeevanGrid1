"""
Pydantic Schemas for Resource Allocation and Shortage Analysis
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from response_optimization.schemas.incident_priority import IncidentItem, PriorityLevelEnum


class ResourceRequirement(BaseModel):
    resource_type: str = Field(..., description="E.g. RESCUE_BOAT, AMBULANCE, NDRF_TEAM, MOBILE_GENERATOR")
    quantity_needed: int = Field(..., ge=1)
    urgency: str = Field(default="IMMEDIATE")
    target_sector: str = Field(default="Incident Zone")


class ResourceAssignment(BaseModel):
    assignment_id: str
    incident_id: str
    incident_name: str
    resource_id: str
    resource_name: str
    resource_type: str
    resource_code: str
    allocated_quantity: int = Field(..., ge=1)
    priority_level: PriorityLevelEnum
    distance_km: float = Field(..., ge=0.0)
    estimated_travel_time_minutes: int = Field(..., ge=0)
    is_travel_time_estimated: bool = True
    suitability_score: float = Field(..., ge=0.0, le=1.0)
    reason: str
    task_assignment: str


class ResourceShortage(BaseModel):
    incident_id: str
    incident_name: str
    resource_type: str
    quantity_demanded: int = Field(..., ge=1)
    quantity_allocated: int = Field(..., ge=0)
    shortage_count: int = Field(..., ge=1)
    urgency: str
    impact_explanation: str
    recommended_mitigation: str


class ResourceAllocationRequest(BaseModel):
    incidents: List[IncidentItem] = Field(..., min_length=1)
    available_resources: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Optional list of resource units. If None, queries live GIS resource layer."
    )
    max_search_radius_km: float = Field(default=50.0, ge=1.0, le=500.0)
    enforce_strict_capacity: bool = Field(default=True)


class ResourceAllocationResponse(BaseModel):
    allocation_id: str
    total_assignments: int
    total_shortages: int
    assignments: List[ResourceAssignment]
    shortages: List[ResourceShortage]
    allocation_summary: Dict[str, Any]
    generated_at: str
