"""
Risk Assessment & MCDA Schemas
"""

from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import Field
from backend.app.schemas.common import BaseSchema


class RiskCategoryEnum(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskEvaluationRequest(BaseSchema):
    disaster_id: Optional[UUID] = None
    bounding_box: Optional[List[float]] = Field(
        None,
        min_length=4,
        max_length=4,
        json_schema_extra={"example": [90.85, 26.15, 91.25, 26.50]},
        description="[min_lng, min_lat, max_lng, max_lat]"
    )
    inundation_threshold_m: float = Field(default=0.3, ge=0.0)


class MCDAScoreBreakdown(BaseSchema):
    hazard_intensity_score: float = Field(..., ge=0.0, le=1.0)
    exposure_score: float = Field(..., ge=0.0, le=1.0)
    vulnerability_score: float = Field(..., ge=0.0, le=1.0)
    coping_capacity_score: float = Field(..., ge=0.0, le=1.0)
    composite_risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_category: RiskCategoryEnum


class HexagonRiskFeature(BaseSchema):
    h3_index: str
    latitude: float
    longitude: float
    population_count: int
    mcda_breakdown: MCDAScoreBreakdown


class RiskEvaluationResponse(BaseSchema):
    evaluation_id: UUID = Field(default_factory=uuid4)
    evaluated_hexagons_count: int
    critical_risk_zones_count: int
    estimated_exposed_population: int
    top_risk_hexagons: List[HexagonRiskFeature] = Field(default_factory=list)
