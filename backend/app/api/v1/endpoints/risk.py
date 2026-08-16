"""
Risk Assessment & MCDA Endpoints (Foundation / Router Layer)
"""

from typing import List
from fastapi import APIRouter, status
from backend.app.schemas.common import ApiResponse
from backend.app.schemas.risk import (
    RiskCategoryEnum,
    RiskEvaluationRequest,
    RiskEvaluationResponse,
)

router = APIRouter(prefix="/risk", tags=["Risk Analysis & MCDA"])


@router.get(
    "/categories",
    response_model=ApiResponse[List[str]],
    status_code=status.HTTP_200_OK,
    summary="Get Risk Severity Categories",
    description="Returns the standard UNDRR operational risk tiers used across JeevanGrid.",
)
async def get_risk_categories() -> ApiResponse[List[str]]:
    """Lists supported operational risk categories."""
    categories = [e.value for e in RiskCategoryEnum]
    return ApiResponse(
        success=True,
        message="Risk categories retrieved.",
        data=categories,
    )


@router.post(
    "/evaluate",
    response_model=ApiResponse[RiskEvaluationResponse],
    status_code=status.HTTP_200_OK,
    summary="Evaluate Regional Disaster Risk (Foundation Stub)",
    description="Calculates composite MCDA risk for the requested bounding box. Actual GIS/MCDA engine wires in Phase 7.",
)
async def evaluate_risk(payload: RiskEvaluationRequest) -> ApiResponse[RiskEvaluationResponse]:
    """Calculates risk matrix across requested spatial boundary."""
    evaluation_result = RiskEvaluationResponse(
        evaluated_hexagons_count=0,
        critical_risk_zones_count=0,
        estimated_exposed_population=0,
        top_risk_hexagons=[],
    )
    return ApiResponse(
        success=True,
        message="Risk evaluation completed successfully.",
        data=evaluation_result,
    )
