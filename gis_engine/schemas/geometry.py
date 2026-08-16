"""
Type-safe Pydantic Schemas for GeoJSON and Spatial Geometries
"""

from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from pydantic import BaseModel, Field, field_validator


class CoordinatesPoint(BaseModel):
    """Longitude, Latitude coordinate pair (WGS84)."""

    lng: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    lat: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")


class BoundingBox(BaseModel):
    """Geographic Bounding Box [min_lng, min_lat, max_lng, max_lat]."""

    min_lng: float = Field(..., ge=-180.0, le=180.0)
    min_lat: float = Field(..., ge=-90.0, le=90.0)
    max_lng: float = Field(..., ge=-180.0, le=180.0)
    max_lat: float = Field(..., ge=-90.0, le=90.0)

    @field_validator("max_lng")
    @classmethod
    def validate_lng_order(cls, v: float, info: Any) -> float:
        min_lng = info.data.get("min_lng")
        if min_lng is not None and v < min_lng:
            raise ValueError(f"max_lng ({v}) must be greater than or equal to min_lng ({min_lng})")
        return v

    @field_validator("max_lat")
    @classmethod
    def validate_lat_order(cls, v: float, info: Any) -> float:
        min_lat = info.data.get("min_lat")
        if min_lat is not None and v < min_lat:
            raise ValueError(f"max_lat ({v}) must be greater than or equal to min_lat ({min_lat})")
        return v

    def to_list(self) -> List[float]:
        return [self.min_lng, self.min_lat, self.max_lng, self.max_lat]


class GeoJSONPoint(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: List[float] = Field(..., min_length=2, max_length=3)

    @field_validator("coordinates")
    @classmethod
    def validate_point_coords(cls, v: List[float]) -> List[float]:
        lng, lat = v[0], v[1]
        if not (-180.0 <= lng <= 180.0):
            raise ValueError(f"Invalid longitude {lng}: must be between -180 and 180")
        if not (-90.0 <= lat <= 90.0):
            raise ValueError(f"Invalid latitude {lat}: must be between -90 and 90")
        return v


class GeoJSONLineString(BaseModel):
    type: Literal["LineString"] = "LineString"
    coordinates: List[List[float]] = Field(..., min_length=2)


class GeoJSONPolygon(BaseModel):
    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[List[float]]] = Field(..., min_length=1)


class GeoJSONMultiPoint(BaseModel):
    type: Literal["MultiPoint"] = "MultiPoint"
    coordinates: List[List[float]] = Field(..., min_length=1)


class GeoJSONMultiLineString(BaseModel):
    type: Literal["MultiLineString"] = "MultiLineString"
    coordinates: List[List[List[float]]] = Field(..., min_length=1)


class GeoJSONMultiPolygon(BaseModel):
    type: Literal["MultiPolygon"] = "MultiPolygon"
    coordinates: List[List[List[List[float]]]] = Field(..., min_length=1)


class GeoJSONGeometryCollection(BaseModel):
    type: Literal["GeometryCollection"] = "GeometryCollection"
    geometries: List[Union[
        GeoJSONPoint,
        GeoJSONLineString,
        GeoJSONPolygon,
        GeoJSONMultiPoint,
        GeoJSONMultiLineString,
        GeoJSONMultiPolygon
    ]] = Field(default_factory=list)


# Union of all valid GeoJSON geometry types
GeometryType = Union[
    GeoJSONPoint,
    GeoJSONLineString,
    GeoJSONPolygon,
    GeoJSONMultiPoint,
    GeoJSONMultiLineString,
    GeoJSONMultiPolygon,
    GeoJSONGeometryCollection
]


class GeoJSONFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    id: Optional[Union[str, int]] = None
    geometry: Union[GeometryType, Dict[str, Any]]
    properties: Dict[str, Any] = Field(default_factory=dict)


class GeoJSONFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[GeoJSONFeature] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
