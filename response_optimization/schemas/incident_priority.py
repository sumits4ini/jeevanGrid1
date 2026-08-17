"""
Pydantic Schemas for Incident Prioritization
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PriorityLevelEnum(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ContributingFactors(BaseModel):
    severity_score: float = Field(..., ge=0.0, le=1.0)
    risk_score: float = Field(..., ge=0.0, le=1.0)
    urgency_score: float = Field(..., ge=0.0, le=1.0)
    population_impact_score: float = Field(..., ge=0.0, le=1.0)
    geographic_impact_score: float = Field(..., ge=0.0, le=1.0)
    resource_shortage_score: float = Field(..., ge=0.0, le=1.0)


class IncidentItem(BaseModel):
    id: str = Field(..., description="Unique incident identifier")
    name: str = Field(..., description="Incident descriptive title")
    disaster_type: str = Field(default="FLOOD", description="FLOOD, CYCLONE, EARTHQUAKE, LANDSLIDE")
    severity_level: int = Field(default=4, ge=1, le=5)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    affected_population: Optional[int] = Field(default=0, ge=0)
    risk_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    inundation_depth_m: Optional[float] = Field(default=0.0, ge=0.0)
    critical_facilities_at_risk: Optional[List[str]] = Field(default_factory=list)


class PrioritizedIncident(BaseModel):
    incident_id: str
    name: str
    disaster_type: str
    priority_rank: int = Field(..., ge=1)
    priority_score: float = Field(..., ge=0.0, le=1.0)
    priority_level: PriorityLevelEnum
    contributing_factors: ContributingFactors
    explanation: str


class IncidentPriorityRequest(BaseModel):
    incidents: List[IncidentItem] = Field(..., min_length=1)
    custom_weights: Optional[Dict[str, float]] = Field(
        default=None,
        description="Optional custom weights for scoring factors. Sum will be normalized."
    )


class IncidentPriorityResponse(BaseModel):
    total_incidents: int
    prioritized_incidents: List[PrioritizedIncident]
    scoring_methodology: str = "Multi-Criteria Decision Analysis (MCDA) with NDMA Tier Classification"
    generated_at: str
