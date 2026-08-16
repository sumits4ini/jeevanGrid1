"""
Pydantic Schemas for AI Intelligence & Decision Support
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class RiskLevelEnum(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ResourceUrgencyEnum(str, Enum):
    IMMEDIATE = "IMMEDIATE"
    URGENT = "URGENT"
    STANDARD = "STANDARD"
    STANDBY = "STANDBY"


class ActionCategoryEnum(str, Enum):
    IMMEDIATE_ACTION = "IMMEDIATE_ACTION"
    RESOURCE_DEPLOYMENT = "RESOURCE_DEPLOYMENT"
    EVACUATION_CONSIDERATION = "EVACUATION_CONSIDERATION"
    INFRASTRUCTURE_SAFEGUARD = "INFRASTRUCTURE_SAFEGUARD"
    MONITORING_FOLLOWUP = "MONITORING_FOLLOWUP"


# ==============================================================================
# 1. Disaster Risk Analysis Schemas
# ==============================================================================

class RiskFactor(BaseModel):
    category: str = Field(..., description="E.g. Hydrological, Infrastructure, Demographic, Topographical")
    factor_name: str
    severity_score: float = Field(..., ge=0.0, le=1.0, description="Normalized factor severity")
    description: str
    mitigation_hint: Optional[str] = None


class RiskAnalysisRequest(BaseModel):
    disaster_id: Optional[str] = None
    disaster_name: Optional[str] = "Active Incident"
    disaster_type: str = Field(default="FLOOD", description="FLOOD, CYCLONE, LANDSLIDE, EARTHQUAKE")
    severity_level: int = Field(default=4, ge=1, le=5)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    affected_population_estimate: Optional[int] = Field(default=50000, ge=0)
    inundation_depth_m: Optional[float] = Field(default=1.2, ge=0.0)
    monitored_zones: Optional[List[str]] = Field(default_factory=list)
    weather_conditions: Optional[Dict[str, Any]] = Field(
        default_factory=lambda: {"rainfall_rate_mm_hr": 45.0, "wind_speed_kmh": 35.0}
    )


class RiskAnalysisResponse(BaseModel):
    analysis_id: str
    disaster_name: str
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Composite AI Risk Score (0.0 to 1.0)")
    risk_level: RiskLevelEnum
    confidence_score: float = Field(default=0.92, ge=0.0, le=1.0)
    priority_level: str = "HIGH"
    affected_area_summary: str
    risk_factors: List[RiskFactor]
    possible_consequences: List[str]
    recommended_actions: List[str]
    resource_requirements: Dict[str, int]
    generated_at: str


# ==============================================================================
# 2. Resource Prioritization Schemas
# ==============================================================================

class ResourcePriorityItem(BaseModel):
    unit_id: str
    unit_name: str
    unit_type: str
    unit_code: str
    priority_score: float = Field(..., ge=0.0, le=1.0)
    priority_rank: int = Field(..., ge=1)
    urgency: ResourceUrgencyEnum
    distance_km: float = Field(..., ge=0.0)
    estimated_transit_minutes: int = Field(..., ge=0)
    status: str
    reason: str
    recommended_task: str


class ResourcePrioritizationRequest(BaseModel):
    disaster_id: Optional[str] = None
    target_latitude: float = Field(..., ge=-90.0, le=90.0)
    target_longitude: float = Field(..., ge=-180.0, le=180.0)
    disaster_type: str = Field(default="FLOOD")
    severity_level: int = Field(default=4, ge=1, le=5)
    required_unit_types: Optional[List[str]] = None
    max_search_radius_km: float = Field(default=50.0, ge=1.0, le=500.0)
    limit: int = Field(default=20, ge=1, le=100)


class ResourcePrioritizationResponse(BaseModel):
    plan_id: str
    target_location: Dict[str, float]
    total_units_evaluated: int
    prioritized_resources: List[ResourcePriorityItem]
    allocation_summary: Dict[str, Any]
    generated_at: str


# ==============================================================================
# 3. AI Recommendation Engine Schemas
# ==============================================================================

class RecommendationItem(BaseModel):
    id: str
    category: ActionCategoryEnum
    title: str
    description: str
    priority_level: RiskLevelEnum
    target_sector: str
    actionable_steps: List[str]
    timeframe: str


class RecommendationRequest(BaseModel):
    disaster_id: Optional[str] = None
    disaster_type: str = Field(default="FLOOD")
    severity_level: int = Field(default=4, ge=1, le=5)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    risk_level: Optional[RiskLevelEnum] = RiskLevelEnum.HIGH
    current_observations: Optional[List[str]] = Field(default_factory=list)
    operational_constraints: Optional[Dict[str, Any]] = Field(default_factory=dict)


class RecommendationResponse(BaseModel):
    recommendation_id: str
    disaster_context: str
    overall_strategy: str
    recommendations: List[RecommendationItem]
    disclaimer: str = (
        "AI-generated decision support advisory. Operational actions must be verified by the "
        "Incident Commander / District Disaster Management Authority (DDMA)."
    )
    generated_at: str
