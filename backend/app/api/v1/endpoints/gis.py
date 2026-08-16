"""
GIS & Geospatial Layer Endpoints (Foundation / Router Layer)
"""

from typing import Any, Dict
from fastapi import APIRouter, status
from backend.app.schemas.common import ApiResponse
from backend.app.schemas.gis import (
    GeoJSONFeatureCollection,
    SpatialBufferQuery,
    SpatialQueryBoundingBox,
)

router = APIRouter(prefix="/gis", tags=["GIS & Spatial Engine"])


@router.get(
    "/hazard-zones",
    response_model=ApiResponse[GeoJSONFeatureCollection],
    status_code=status.HTTP_200_OK,
    summary="Get Active Hazard Inundation Polygons (GeoJSON)",
    description="Returns GeoJSON FeatureCollection of active hazard zones for MapLibre rendering.",
)
async def get_hazard_zones() -> ApiResponse[GeoJSONFeatureCollection]:
    """Retrieves active hazard polygons as GeoJSON."""
    collection = GeoJSONFeatureCollection(features=[])
    return ApiResponse(
        success=True,
        message="Active hazard zones retrieved.",
        data=collection,
    )


@router.post(
    "/query-bbox",
    response_model=ApiResponse[GeoJSONFeatureCollection],
    status_code=status.HTTP_200_OK,
    summary="Spatial Query by Bounding Box",
    description="Filters geospatial layers intersecting the given bounding box coordinates.",
)
async def query_by_bbox(payload: SpatialQueryBoundingBox) -> ApiResponse[GeoJSONFeatureCollection]:
    """Spatial bounding box query."""
    collection = GeoJSONFeatureCollection(features=[])
    return ApiResponse(
        success=True,
        message=f"Spatial query executed for bbox [{payload.min_lng}, {payload.min_lat}, {payload.max_lng}, {payload.max_lat}].",
        data=collection,
    )


@router.post(
    "/buffer-check",
    response_model=ApiResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Spatial Proximity & Buffer Check",
    description="Checks infrastructure assets within a given radius (meters) of a hazard point.",
)
async def check_spatial_buffer(payload: SpatialBufferQuery) -> ApiResponse[Dict[str, Any]]:
    """Proximity query around a geographic point."""
    result = {
        "center": {"lat": payload.latitude, "lng": payload.longitude},
        "radius_meters": payload.radius_meters,
        "assets_within_buffer_count": 0,
        "assets": [],
    }
    return ApiResponse(
        success=True,
        message="Buffer proximity check completed.",
        data=result,
    )
