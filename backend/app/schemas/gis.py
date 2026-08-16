"""
GIS & GeoJSON Spatial Feature Schemas
"""

from typing import Any, Dict, List, Literal, Optional, Union
from uuid import UUID
from pydantic import Field
from backend.app.schemas.common import BaseSchema


class GeoJSONGeometryPoint(BaseSchema):
    type: Literal["Point"] = "Point"
    coordinates: List[float] = Field(..., min_length=2, max_length=3, json_schema_extra={"example": [91.0063, 26.3216]})


class GeoJSONGeometryPolygon(BaseSchema):
    type: Literal["Polygon", "MultiPolygon"] = "Polygon"
    coordinates: List[Any]


class GeoJSONFeature(BaseSchema):
    type: Literal["Feature"] = "Feature"
    id: Optional[Union[str, int]] = None
    geometry: Union[GeoJSONGeometryPoint, GeoJSONGeometryPolygon, Dict[str, Any]]
    properties: Dict[str, Any] = Field(default_factory=dict)


class GeoJSONFeatureCollection(BaseSchema):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[GeoJSONFeature] = Field(default_factory=list)


class SpatialQueryBoundingBox(BaseSchema):
    min_lng: float = Field(..., ge=-180.0, le=180.0)
    min_lat: float = Field(..., ge=-90.0, le=90.0)
    max_lng: float = Field(..., ge=-180.0, le=180.0)
    max_lat: float = Field(..., ge=-90.0, le=90.0)


class SpatialBufferQuery(BaseSchema):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    radius_meters: float = Field(..., ge=10.0, le=100000.0)
    target_facility_types: Optional[List[str]] = None
