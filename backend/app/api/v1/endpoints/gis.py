"""
GIS & Geospatial Layer Endpoints (Phase 5 GIS Engine Integration)
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.core.exceptions import EntityNotFoundException, SpatialOperationException
from backend.app.schemas.common import ApiResponse
from gis_engine.geometry.validation import validate_coordinates_wgs84, validate_geojson_dict
from gis_engine.schemas.geometry import (
    BoundingBox,
    GeoJSONFeatureCollection,
)
from gis_engine.schemas.layer import (
    LayerMetadata,
    LayerSummary,
    NearbyQueryResponse,
    SpatialIntersectionRequest,
    SpatialIntersectionResponse,
)
from gis_engine.services.gis_service import gis_service

router = APIRouter(prefix="/gis", tags=["GIS & Spatial Engine"])


@router.get(
    "/layers",
    response_model=ApiResponse[LayerSummary],
    status_code=status.HTTP_200_OK,
    summary="List Registered GIS Operational Layers",
    description="Returns metadata, geometry types, and feature counts for all active GIS layers.",
)
async def list_gis_layers() -> ApiResponse[LayerSummary]:
    """Retrieves all registered GIS operational layers."""
    summary = gis_service.list_layers()
    return ApiResponse(
        success=True,
        message=f"Retrieved {summary.total_layers} registered GIS layers.",
        data=summary,
    )


@router.get(
    "/layers/{layer_name}",
    response_model=ApiResponse[GeoJSONFeatureCollection],
    status_code=status.HTTP_200_OK,
    summary="Get GIS Layer GeoJSON FeatureCollection",
    description="Returns full GeoJSON FeatureCollection for a specific layer with optional bounding-box spatial filter.",
)
async def get_gis_layer_features(
    layer_name: str,
    min_lng: Optional[float] = Query(None, ge=-180.0, le=180.0, description="Bounding box minimum longitude"),
    min_lat: Optional[float] = Query(None, ge=-90.0, le=90.0, description="Bounding box minimum latitude"),
    max_lng: Optional[float] = Query(None, ge=-180.0, le=180.0, description="Bounding box maximum longitude"),
    max_lat: Optional[float] = Query(None, ge=-90.0, le=90.0, description="Bounding box maximum latitude"),
) -> ApiResponse[GeoJSONFeatureCollection]:
    """Retrieves GeoJSON features for a specified layer."""
    bbox: Optional[BoundingBox] = None
    if all(v is not None for v in [min_lng, min_lat, max_lng, max_lat]):
        try:
            bbox = BoundingBox(
                min_lng=min_lng,  # type: ignore[arg-type]
                min_lat=min_lat,  # type: ignore[arg-type]
                max_lng=max_lng,  # type: ignore[arg-type]
                max_lat=max_lat,  # type: ignore[arg-type]
            )
        except ValueError as exc:
            raise SpatialOperationException(message=f"Invalid bounding box coordinates: {str(exc)}")

    fc = gis_service.get_layer_feature_collection(layer_id=layer_name, bbox=bbox)
    if fc is None:
        raise EntityNotFoundException(entity_name="GIS Layer", entity_id=layer_name)

    return ApiResponse(
        success=True,
        message=f"Retrieved {len(fc.features)} features for layer '{layer_name}'.",
        data=fc,
    )


@router.get(
    "/features",
    response_model=ApiResponse[GeoJSONFeatureCollection],
    status_code=status.HTTP_200_OK,
    summary="Query Geospatial Features Across Layers",
    description="Multi-layer spatial query with optional bounding box and layer name filters.",
)
async def query_features(
    layers: Optional[List[str]] = Query(None, description="List of layer IDs to include (e.g. ?layers=infrastructure&layers=hazard_zones)"),
    min_lng: Optional[float] = Query(None, ge=-180.0, le=180.0),
    min_lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
    max_lng: Optional[float] = Query(None, ge=-180.0, le=180.0),
    max_lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
) -> ApiResponse[GeoJSONFeatureCollection]:
    """Queries features across multiple GIS layers."""
    bbox: Optional[BoundingBox] = None
    if all(v is not None for v in [min_lng, min_lat, max_lng, max_lat]):
        try:
            bbox = BoundingBox(
                min_lng=min_lng,  # type: ignore[arg-type]
                min_lat=min_lat,  # type: ignore[arg-type]
                max_lng=max_lng,  # type: ignore[arg-type]
                max_lat=max_lat,  # type: ignore[arg-type]
            )
        except ValueError as exc:
            raise SpatialOperationException(message=f"Invalid bounding box: {str(exc)}")

    fc = gis_service.query_multi_layer_features(layer_ids=layers, bbox=bbox)
    return ApiResponse(
        success=True,
        message=f"Query matched {len(fc.features)} features across layers.",
        data=fc,
    )


@router.get(
    "/nearby",
    response_model=ApiResponse[NearbyQueryResponse],
    status_code=status.HTTP_200_OK,
    summary="Proximity Search / Nearby Facilities & Assets",
    description="Finds critical facilities, response units, and hazard zones within radius (meters) of a location.",
)
async def get_nearby_features(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Center latitude"),
    lng: float = Query(..., ge=-180.0, le=180.0, description="Center longitude"),
    radius: float = Query(5000.0, ge=10.0, le=200000.0, description="Search radius in meters"),
    layers: Optional[List[str]] = Query(None, description="Filter by layer names"),
    limit: int = Query(50, ge=1, le=500),
) -> ApiResponse[NearbyQueryResponse]:
    """Finds nearby features ranked by distance in meters."""
    valid, msg = validate_coordinates_wgs84(lng=lng, lat=lat)
    if not valid:
        raise SpatialOperationException(message=msg)

    nearby_resp = gis_service.find_nearby_features(
        latitude=lat,
        longitude=lng,
        radius_meters=radius,
        layer_names=layers,
        limit=limit,
    )
    return ApiResponse(
        success=True,
        message=f"Found {nearby_resp.total_found} features within {radius}m radius.",
        data=nearby_resp,
    )


@router.post(
    "/intersections",
    response_model=ApiResponse[SpatialIntersectionResponse],
    status_code=status.HTTP_200_OK,
    summary="Compute Spatial Intersections Against Polygon",
    description="Evaluates which infrastructure assets and units intersect with a given hazard polygon (with optional buffer).",
)
async def compute_spatial_intersections(
    payload: SpatialIntersectionRequest,
) -> ApiResponse[SpatialIntersectionResponse]:
    """Evaluates spatial intersection for a given polygon geometry."""
    geom_dict = payload.target_geometry if isinstance(payload.target_geometry, dict) else payload.target_geometry.model_dump()
    
    valid, msg = validate_geojson_dict(geom_dict)
    if not valid:
        raise SpatialOperationException(message=f"Invalid target polygon geometry: {msg}")

    result = gis_service.compute_intersections(
        target_geometry=geom_dict,
        intersect_layers=payload.intersect_layers,
        buffer_meters=payload.buffer_meters,
    )
    return ApiResponse(
        success=True,
        message=f"Intersection analysis matched {result.total_intersected_features} features.",
        data=result,
    )


# ==============================================================================
# Backward-Compatibility Routes for Phase 2/3 clients
# ==============================================================================

@router.get(
    "/hazard-zones",
    response_model=ApiResponse[GeoJSONFeatureCollection],
    status_code=status.HTTP_200_OK,
    summary="Get Active Hazard Inundation Polygons (GeoJSON)",
)
async def get_hazard_zones_compat() -> ApiResponse[GeoJSONFeatureCollection]:
    """Backward-compatible route returning hazard zones feature collection."""
    fc = gis_service.get_layer_feature_collection("hazard_zones")
    if fc is None:
        fc = GeoJSONFeatureCollection(features=[])
    return ApiResponse(
        success=True,
        message="Active hazard zones retrieved.",
        data=fc,
    )


@router.post(
    "/query-bbox",
    response_model=ApiResponse[GeoJSONFeatureCollection],
    status_code=status.HTTP_200_OK,
    summary="Spatial Query by Bounding Box (Compat)",
)
async def query_by_bbox_compat(payload: Dict[str, float]) -> ApiResponse[GeoJSONFeatureCollection]:
    """Backward-compatible bbox query."""
    bbox = BoundingBox(
        min_lng=payload.get("min_lng", -180.0),
        min_lat=payload.get("min_lat", -90.0),
        max_lng=payload.get("max_lng", 180.0),
        max_lat=payload.get("max_lat", 90.0),
    )
    fc = gis_service.query_multi_layer_features(bbox=bbox)
    return ApiResponse(
        success=True,
        message="Spatial query executed.",
        data=fc,
    )


@router.post(
    "/buffer-check",
    response_model=ApiResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Spatial Proximity & Buffer Check (Compat)",
)
async def check_spatial_buffer_compat(payload: Dict[str, Any]) -> ApiResponse[Dict[str, Any]]:
    """Backward-compatible buffer check."""
    lat = float(payload.get("latitude", 0.0))
    lng = float(payload.get("longitude", 0.0))
    radius = float(payload.get("radius_meters", 5000.0))

    nearby_resp = gis_service.find_nearby_features(
        latitude=lat,
        longitude=lng,
        radius_meters=radius,
    )
    return ApiResponse(
        success=True,
        message="Buffer proximity check completed.",
        data={
            "center": {"lat": lat, "lng": lng},
            "radius_meters": radius,
            "assets_within_buffer_count": nearby_resp.total_found,
            "assets": [f.model_dump() for f in nearby_resp.features],
        },
    )
