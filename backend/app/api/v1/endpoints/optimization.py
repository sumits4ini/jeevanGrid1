"""
Emergency Response Optimization & Resource Allocation Endpoints (Phase 7)
"""

from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.common import ApiResponse
from gis_engine.services.gis_service import gis_service
from response_optimization.schemas.allocation import (
    ResourceAllocationRequest,
    ResourceAllocationResponse,
)
from response_optimization.schemas.incident_priority import (
    IncidentPriorityRequest,
    IncidentPriorityResponse,
)
from response_optimization.schemas.response_plan import (
    ResponsePlanRequest,
    ResponsePlanResponse,
)
from response_optimization.services.allocation_service import allocation_service
from response_optimization.services.optimization_service import optimization_service
from response_optimization.services.scoring_service import scoring_service

router = APIRouter(prefix="/optimization", tags=["Emergency Response Optimization"])


@router.post(
    "/prioritize-incidents",
    response_model=ApiResponse[IncidentPriorityResponse],
    status_code=status.HTTP_200_OK,
    summary="MCDA Incident Prioritization Ranking",
    description="Evaluates disaster severity, risk score, population exposure, and urgency to produce deterministic priority ranks.",
)
async def prioritize_incidents(
    payload: IncidentPriorityRequest,
) -> ApiResponse[IncidentPriorityResponse]:
    """Computes MCDA priority ranks for submitted disaster incidents."""
    result = scoring_service.prioritize_incidents(payload)
    return ApiResponse(
        success=True,
        message=f"Successfully prioritized {result.total_incidents} incidents.",
        data=result,
    )


@router.post(
    "/allocate-resources",
    response_model=ApiResponse[ResourceAllocationResponse],
    status_code=status.HTTP_200_OK,
    summary="Capacitated Resource Allocation Engine",
    description="Matches available rescue units against prioritized incident demand while preventing over-allocation and identifying shortages.",
)
async def allocate_resources(
    payload: ResourceAllocationRequest,
) -> ApiResponse[ResourceAllocationResponse]:
    """Executes capacitated allocation of rescue fleet across disaster incidents."""
    result = allocation_service.allocate(payload)
    return ApiResponse(
        success=True,
        message=f"Allocated {result.total_assignments} units across {len(payload.incidents)} incidents ({result.total_shortages} shortages identified).",
        data=result,
    )


@router.post(
    "/response-plan",
    response_model=ApiResponse[ResponsePlanResponse],
    status_code=status.HTTP_200_OK,
    summary="Generate Comprehensive Emergency Response Plan",
    description="Produces an end-to-end response plan containing prioritized dispatch orders, travel times, warnings, and AI advisory recommendations.",
)
async def generate_response_plan(
    payload: ResponsePlanRequest,
) -> ApiResponse[ResponsePlanResponse]:
    """Generates an end-to-end tactical emergency response plan."""
    result = await optimization_service.generate_response_plan(payload)
    return ApiResponse(
        success=True,
        message=f"Generated Response Plan [{result.plan_id}] with {len(result.deployment_sequence)} deployment orders.",
        data=result,
    )


@router.get(
    "/resource-status",
    response_model=ApiResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Response Fleet Availability & Readiness Status",
    description="Returns live counts, readiness percentages, and unit breakdowns across available rescue fleet assets.",
)
async def get_resource_status() -> ApiResponse[Dict[str, Any]]:
    """Returns current emergency fleet readiness from GIS layers."""
    res_layer = gis_service.registry.get_layer("response_units")
    raw_units = res_layer.get_features() if res_layer else []

    total_units = len(raw_units)
    available_units = sum(1 for u in raw_units if str(u.get("status", "")).upper() in ["AVAILABLE", "STANDBY"])

    type_counts: Dict[str, Dict[str, int]] = {}
    for u in raw_units:
        utype = str(u.get("unit_type", "OTHER"))
        status = str(u.get("status", "AVAILABLE")).upper()
        if utype not in type_counts:
            type_counts[utype] = {"total": 0, "available": 0}
        type_counts[utype]["total"] += 1
        if status in ["AVAILABLE", "STANDBY"]:
            type_counts[utype]["available"] += 1

    return ApiResponse(
        success=True,
        message=f"Retrieved fleet readiness: {available_units}/{total_units} units available.",
        data={
            "total_units": total_units,
            "available_units": available_units,
            "readiness_percentage": round((available_units / max(1, total_units)) * 100, 1),
            "breakdown": type_counts,
            "units": raw_units,
        },
    )


@router.get(
    "/incidents/{incident_id}/resources",
    response_model=ApiResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Get Closest Suited Resources for Specific Incident",
    description="Finds available rescue assets within radius of a specific disaster epicenter ranked by proximity and suitability.",
)
async def get_resources_for_incident(
    incident_id: str,
    lat: float = Query(26.3216, ge=-90.0, le=90.0),
    lng: float = Query(91.0063, ge=-180.0, le=180.0),
    radius_km: float = Query(25.0, ge=1.0, le=200.0),
) -> ApiResponse[Dict[str, Any]]:
    """Queries closest suited response units for a specific incident location."""
    nearby_resp = gis_service.find_nearby_features(
        latitude=lat,
        longitude=lng,
        radius_meters=radius_km * 1000.0,
        layer_names=["response_units"],
        limit=20,
    )
    return ApiResponse(
        success=True,
        message=f"Found {nearby_resp.total_found} response units within {radius_km}km of incident '{incident_id}'.",
        data={
            "incident_id": incident_id,
            "center": {"latitude": lat, "longitude": lng},
            "radius_km": radius_km,
            "total_found": nearby_resp.total_found,
            "resources": [f.model_dump() for f in nearby_resp.features],
        },
    )
