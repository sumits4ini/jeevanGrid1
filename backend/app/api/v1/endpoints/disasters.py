"""
Disaster Intelligence Endpoints (Foundation / Router Layer)
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query, status
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.schemas.common import ApiResponse
from backend.app.schemas.disaster import (
    DisasterCreate,
    DisasterResponse,
    DisasterStatusEnum,
    DisasterSummary,
    DisasterTypeEnum,
)

router = APIRouter(prefix="/disasters", tags=["Disasters"])


@router.get(
    "",
    response_model=ApiResponse[List[DisasterResponse]],
    status_code=status.HTTP_200_OK,
    summary="List Disasters",
    description="Retrieve a list of active and simulated disaster events with optional type and status filtering.",
)
async def list_disasters(
    disaster_type: Optional[DisasterTypeEnum] = Query(None, description="Filter by disaster type"),
    status_filter: Optional[DisasterStatusEnum] = Query(None, alias="status", description="Filter by status"),
) -> ApiResponse[List[DisasterResponse]]:
    """Lists registered disasters. (Foundation baseline - returns structured list)."""
    return ApiResponse(
        success=True,
        message="Disaster events retrieved successfully.",
        data=[],
    )


@router.get(
    "/summary/overview",
    response_model=ApiResponse[DisasterSummary],
    status_code=status.HTTP_200_OK,
    summary="Get Operational Disaster Summary",
    description="Returns aggregated metrics across all active disaster zones for the Common Operational Picture.",
)
async def get_disaster_summary() -> ApiResponse[DisasterSummary]:
    """Provides high-level disaster summary metrics for the COP dashboard."""
    summary_data = DisasterSummary(
        total_active_disasters=0,
        critical_alerts_count=0,
        total_affected_population=0,
        active_rescue_units=0,
        disasters=[],
    )
    return ApiResponse(
        success=True,
        message="Disaster summary overview calculated.",
        data=summary_data,
    )


@router.get(
    "/{disaster_id}",
    response_model=ApiResponse[DisasterResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Disaster by ID",
)
async def get_disaster(disaster_id: UUID) -> ApiResponse[DisasterResponse]:
    """Retrieves specific disaster details by ID."""
    raise EntityNotFoundException(entity_name="Disaster", entity_id=disaster_id)


@router.post(
    "",
    response_model=ApiResponse[DisasterResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create New Disaster Event",
)
async def create_disaster(payload: DisasterCreate) -> ApiResponse[DisasterResponse]:
    """Creates and registers a new disaster event."""
    created_disaster = DisasterResponse(
        name=payload.name,
        disaster_type=payload.disaster_type,
        severity_level=payload.severity_level,
        status=payload.status,
        description=payload.description,
        latitude=payload.latitude,
        longitude=payload.longitude,
        affected_population_estimate=0,
    )
    return ApiResponse(
        success=True,
        message="Disaster event registered successfully.",
        data=created_disaster,
    )
