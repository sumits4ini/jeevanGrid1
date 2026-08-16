"""
JeevanGrid GIS Engine & Geospatial Intelligence Core
"""

from gis_engine.geometry import (
    calculate_area_sq_meters,
    calculate_haversine_distance_m,
    calculate_length_meters,
    check_point_in_polygon,
    compute_intersection,
    compute_union,
    get_bounding_box,
    get_centroid,
    safe_to_geojson,
    safe_to_shapely,
    transform_to_epsg3857,
    transform_to_epsg4326,
    validate_coordinates_wgs84,
    validate_geojson_dict,
)
from gis_engine.layers import (
    BaseGISLayer,
    DisasterLayer,
    HazardZoneLayer,
    LayerRegistry,
    LocationLayer,
    ResourceLayer,
    layer_registry,
)
from gis_engine.schemas import (
    BoundingBox,
    CoordinatesPoint,
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    LayerMetadata,
    LayerSummary,
    NearbyFeatureItem,
    NearbyQueryRequest,
    NearbyQueryResponse,
    SpatialIntersectionRequest,
    SpatialIntersectionResponse,
)
from gis_engine.services import GISService, gis_service

__version__ = "0.1.0"

__all__ = [
    "validate_coordinates_wgs84",
    "validate_geojson_dict",
    "safe_to_shapely",
    "safe_to_geojson",
    "transform_to_epsg3857",
    "transform_to_epsg4326",
    "calculate_haversine_distance_m",
    "get_bounding_box",
    "get_centroid",
    "calculate_area_sq_meters",
    "calculate_length_meters",
    "check_point_in_polygon",
    "compute_intersection",
    "compute_union",
    "BoundingBox",
    "CoordinatesPoint",
    "GeoJSONFeature",
    "GeoJSONFeatureCollection",
    "LayerMetadata",
    "LayerSummary",
    "NearbyQueryRequest",
    "NearbyFeatureItem",
    "NearbyQueryResponse",
    "SpatialIntersectionRequest",
    "SpatialIntersectionResponse",
    "BaseGISLayer",
    "DisasterLayer",
    "HazardZoneLayer",
    "LocationLayer",
    "ResourceLayer",
    "LayerRegistry",
    "layer_registry",
    "GISService",
    "gis_service",
]
