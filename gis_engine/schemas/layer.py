"""
GIS Layer and Spatial Operation Schemas
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from gis_engine.schemas.geometry import BoundingBox, GeoJSONFeatureCollection, GeoJSONPolygon, GeoJSONMultiPolygon


class LayerMetadata(BaseModel):
    """Metadata describing a registered GIS operational layer."""

    layer_id: str
    name: str
    description: str
    geometry_type: str  # Point, Polygon, MultiPolygon, LineString
    srid: int = 4326
    feature_count: int = 0
    bounding_box: Optional[BoundingBox] = None
    properties_schema: Dict[str, str] = Field(default_factory=dict)
    is_live: bool = True


class LayerSummary(BaseModel):
    """Summary of all available GIS layers."""

    total_layers: int
    layers: List[LayerMetadata]


class NearbyQueryRequest(BaseModel):
    """Parameters for finding facilities/units within a radius of a coordinate point."""

    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    radius_meters: float = Field(default=5000.0, ge=10.0, le=200000.0, description="Search radius in meters")
    layer_names: Optional[List[str]] = Field(
        default=None,
        description="Optional list of specific layer IDs to filter (e.g. ['infrastructure', 'response_units'])"
    )
    limit: int = Field(default=50, ge=1, le=500)


class NearbyFeatureItem(BaseModel):
    """Feature returned from a proximity/nearby query with calculated distance."""

    id: str
    layer_id: str
    name: str
    distance_meters: float
    latitude: float
    longitude: float
    properties: Dict[str, Any] = Field(default_factory=dict)


class NearbyQueryResponse(BaseModel):
    center: Dict[str, float]
    radius_meters: float
    total_found: int
    features: List[NearbyFeatureItem] = Field(default_factory=list)


class SpatialIntersectionRequest(BaseModel):
    """Parameters for computing spatial intersections against a target polygon geometry."""

    target_geometry: Union[GeoJSONPolygon, GeoJSONMultiPolygon, Dict[str, Any]]
    intersect_layers: Optional[List[str]] = Field(
        default=None,
        description="List of layers to test for intersection. Defaults to all active layers."
    )
    buffer_meters: float = Field(default=0.0, ge=0.0, le=50000.0)


class IntersectedLayerResult(BaseModel):
    layer_id: str
    intersected_count: int
    feature_collection: GeoJSONFeatureCollection


class SpatialIntersectionResponse(BaseModel):
    intersection_id: str
    buffer_applied_meters: float
    total_intersected_features: int
    results_by_layer: Dict[str, IntersectedLayerResult] = Field(default_factory=dict)
