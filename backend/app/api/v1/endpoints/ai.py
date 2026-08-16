"""
AI Intelligence & Decision Support Endpoints (Phase 6)
"""

from typing import Any, Dict
from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.ai import (
    RecommendationRequest,
    RecommendationResponse,
    ResourcePrioritizationRequest,
    ResourcePrioritizationResponse,
    RiskAnalysisRequest,
    RiskAnalysisResponse,
)
from backend.app.schemas.common import ApiResponse
from ai_services.services.ai_manager import ai_manager

router = APIRouter(prefix="/ai", tags=["AI Intelligence & Decision Support"])


@router.get(
    "/status",
    response_model=ApiResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="AI Intelligence Provider Telemetry & Health",
    description="Returns current operational status and active engine type of the AI intelligence layer.",
)
async def get_ai_status() -> ApiResponse[Dict[str, Any]]:
    """Checks the status and telemetry of the AI service provider."""
    health = await ai_manager.health_check()
    return ApiResponse(
        success=True,
        message="AI intelligence service is operational.",
        data=health,
    )


@router.post(
    "/risk-analysis",
    response_model=ApiResponse[RiskAnalysisResponse],
    status_code=status.HTTP_200_OK,
    summary="AI-Assisted Disaster Risk Intelligence Analysis",
    description="Evaluates multi-factor hazard intensity, inundation depths, and population exposure to generate structured risk levels.",
)
async def analyze_disaster_risk(
    payload: RiskAnalysisRequest,
) -> ApiResponse[RiskAnalysisResponse]:
    """Generates AI disaster risk assessment and consequence forecasts."""
    result = await ai_manager.analyze_risk(payload)
    return ApiResponse(
        success=True,
        message=f"Disaster risk assessment computed: Level {result.risk_level.value} (Score: {result.risk_score}).",
        data=result,
    )


@router.post(
    "/resource-priority",
    response_model=ApiResponse[ResourcePrioritizationResponse],
    status_code=status.HTTP_200_OK,
    summary="Intelligent Rescue Resource Prioritization",
    description="Ranks emergency response units by spatial proximity, vehicle type compatibility, and urgency.",
)
async def prioritize_resources(
    payload: ResourcePrioritizationRequest,
) -> ApiResponse[ResourcePrioritizationResponse]:
    """Computes urgency scores and prioritized allocation for rescue units."""
    result = await ai_manager.prioritize_resources(payload)
    return ApiResponse(
        success=True,
        message=f"Prioritized {len(result.prioritized_resources)} response units for incident dispatch.",
        data=result,
    )


@router.post(
    "/recommendations",
    response_model=ApiResponse[RecommendationResponse],
    status_code=status.HTTP_200_OK,
    summary="Actionable AI Incident Recommendations",
    description="Generates categorized tactical guidelines across immediate actions, deployment, and infrastructure safeguards.",
)
async def generate_recommendations(
    payload: RecommendationRequest,
) -> ApiResponse[RecommendationResponse]:
    """Generates structured operational guidelines for Incident Command."""
    result = await ai_manager.generate_recommendations(payload)
    return ApiResponse(
        success=True,
        message=f"Generated {len(result.recommendations)} tactical recommendations for Incident Command.",
        data=result,
    )
