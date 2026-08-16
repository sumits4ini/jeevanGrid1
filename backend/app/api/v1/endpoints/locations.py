"""
Locations and Critical Infrastructure Endpoints (Foundation / Router Layer)
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query, status
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.schemas.common import ApiResponse
from backend.app.schemas.location import (
    CriticalInfrastructureCreate,
    CriticalInfrastructureResponse,
    FacilityTypeEnum,
    OperationalStatusEnum,
)

router = APIRouter(prefix="/locations", tags=["Locations & Infrastructure"])


@router.get(
    "/infrastructure",
    response_model=ApiResponse[List[CriticalInfrastructureResponse]],
    status_code=status.HTTP_200_OK,
    summary="List Critical Infrastructure Facilities",
    description="Retrieve hospitals, power stations, shelters, and water plants.",
)
async def list_infrastructure(
    facility_type: Optional[FacilityTypeEnum] = Query(None, description="Filter by facility type"),
    operational_status: Optional[OperationalStatusEnum] = Query(None, description="Filter by status"),
) -> ApiResponse[List[CriticalInfrastructureResponse]]:
    """Lists registered critical infrastructure facilities."""
    return ApiResponse(
        success=True,
        message="Critical infrastructure assets retrieved successfully.",
        data=[],
    )


@router.get(
    "/infrastructure/{facility_id}",
    response_model=ApiResponse[CriticalInfrastructureResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Infrastructure Facility by ID",
)
async def get_infrastructure(facility_id: UUID) -> ApiResponse[CriticalInfrastructureResponse]:
    """Retrieves specific facility details."""
    raise EntityNotFoundException(entity_name="CriticalInfrastructure", entity_id=facility_id)


@router.post(
    "/infrastructure",
    response_model=ApiResponse[CriticalInfrastructureResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register New Infrastructure Asset",
)
async def create_infrastructure(
    payload: CriticalInfrastructureCreate,
) -> ApiResponse[CriticalInfrastructureResponse]:
    """Registers a new critical infrastructure facility."""
    created_facility = CriticalInfrastructureResponse(
        name=payload.name,
        facility_type=payload.facility_type,
        operational_status=payload.operational_status,
        latitude=payload.latitude,
        longitude=payload.longitude,
        max_capacity=payload.max_capacity,
        current_occupancy=payload.current_occupancy,
        backup_power_hours=payload.backup_power_hours,
        contact_phone=payload.contact_phone,
        is_threatened=False,
    )
    return ApiResponse(
        success=True,
        message="Critical infrastructure asset registered successfully.",
        data=created_facility,
    )
