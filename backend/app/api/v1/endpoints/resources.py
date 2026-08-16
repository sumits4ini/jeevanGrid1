"""
Emergency Resources & Dispatch Optimization Endpoints (Foundation / Router Layer)
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query, status
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.schemas.common import ApiResponse
from backend.app.schemas.resource import (
    DispatchPlanRequest,
    DispatchPlanResponse,
    ResponseUnitCreate,
    ResponseUnitResponse,
    UnitStatusEnum,
    UnitTypeEnum,
)

router = APIRouter(prefix="/resources", tags=["Resources & Dispatch"])


@router.get(
    "/units",
    response_model=ApiResponse[List[ResponseUnitResponse]],
    status_code=status.HTTP_200_OK,
    summary="List Emergency Response Units",
    description="Retrieve all active NDRF, SDRF, ambulance, and logistics units with telemetry.",
)
async def list_response_units(
    unit_type: Optional[UnitTypeEnum] = Query(None, description="Filter by unit type"),
    unit_status: Optional[UnitStatusEnum] = Query(None, alias="status", description="Filter by operational status"),
) -> ApiResponse[List[ResponseUnitResponse]]:
    """Lists registered response units."""
    return ApiResponse(
        success=True,
        message="Emergency response units retrieved successfully.",
        data=[],
    )


@router.get(
    "/units/{unit_id}",
    response_model=ApiResponse[ResponseUnitResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Response Unit by ID",
)
async def get_response_unit(unit_id: UUID) -> ApiResponse[ResponseUnitResponse]:
    """Retrieves specific unit details."""
    raise EntityNotFoundException(entity_name="ResponseUnit", entity_id=unit_id)


@router.post(
    "/units",
    response_model=ApiResponse[ResponseUnitResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register New Response Unit",
)
async def create_response_unit(payload: ResponseUnitCreate) -> ApiResponse[ResponseUnitResponse]:
    """Registers an emergency vehicle or rescue battalion."""
    created_unit = ResponseUnitResponse(
        unit_code=payload.unit_code,
        unit_type=payload.unit_type,
        status=payload.status,
        latitude=payload.latitude,
        longitude=payload.longitude,
        capacity_payload=payload.capacity_payload,
    )
    return ApiResponse(
        success=True,
        message="Response unit registered successfully.",
        data=created_unit,
    )


@router.post(
    "/dispatch-plan",
    response_model=ApiResponse[DispatchPlanResponse],
    status_code=status.HTTP_200_OK,
    summary="Generate Optimal Dispatch Plan (Foundation Stub)",
    description="Calculates optimal resource allocation. Actual MILP solver is wired in Phase 9.",
)
async def generate_dispatch_plan(payload: DispatchPlanRequest) -> ApiResponse[DispatchPlanResponse]:
    """Provides the dispatch plan endpoint contract."""
    response_plan = DispatchPlanResponse(
        disaster_id=payload.disaster_id,
        total_units_allocated=0,
        estimated_lives_stabilized=0,
        allocations=[],
        solver_status="SOLVER_READY_PHASE_9",
        solver_execution_time_ms=0.0,
    )
    return ApiResponse(
        success=True,
        message="Dispatch plan generated.",
        data=response_plan,
    )
