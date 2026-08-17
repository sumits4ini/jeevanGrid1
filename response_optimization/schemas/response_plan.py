"""
Pydantic Schemas for Comprehensive Emergency Response Plans
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from response_optimization.schemas.allocation import ResourceAssignment, ResourceShortage
from response_optimization.schemas.incident_priority import IncidentItem, PrioritizedIncident, PriorityLevelEnum


class OperationalWarning(BaseModel):
    warning_code: str
    severity: str = Field(default="HIGH", description="CRITICAL, HIGH, WARNING, INFO")
    title: str
    message: str
    affected_incident_id: Optional[str] = None


class DeploymentOrderItem(BaseModel):
    deployment_order: int = Field(..., ge=1)
    incident_id: str
    incident_name: str
    priority_level: PriorityLevelEnum
    resource_id: str
    resource_name: str
    resource_type: str
    resource_code: str
    allocated_quantity: int = Field(..., ge=1)
    estimated_eta_minutes: int = Field(..., ge=0)
    is_eta_estimated: bool = True
    staging_point: str


class ResponsePlanRequest(BaseModel):
    incidents: List[IncidentItem] = Field(..., min_length=1)
    available_resources: Optional[List[Dict[str, Any]]] = None
    max_search_radius_km: float = Field(default=50.0, ge=1.0, le=500.0)
    include_ai_advisory: bool = Field(default=True)


class ResponsePlanResponse(BaseModel):
    plan_id: str
    generated_at: str
    incident_priorities: List[PrioritizedIncident]
    deployment_sequence: List[DeploymentOrderItem]
    allocations: List[ResourceAssignment]
    unresolved_shortages: List[ResourceShortage]
    operational_warnings: List[OperationalWarning]
    recommended_actions: List[str]
    plan_summary: Dict[str, Any]
    disclaimer: str = (
        "Deterministic Emergency Response Plan generated for decision-support. "
        "Estimated travel times are approximations based on urban disaster terrain factors. "
        "Incident Commander authorization required prior to executive field dispatch."
    )
