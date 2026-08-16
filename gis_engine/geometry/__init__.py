"""
GIS Geometry Package Export
"""

from gis_engine.geometry.operations import (
    calculate_area_sq_meters,
    calculate_length_meters,
    check_point_in_polygon,
    compute_intersection,
    compute_union,
    get_bounding_box,
    get_centroid,
)
from gis_engine.geometry.transforms import (
    buffer_geometry_meters,
    calculate_haversine_distance_m,
    transform_to_epsg3857,
    transform_to_epsg4326,
)
from gis_engine.geometry.validation import (
    SUPPORTED_GEOMETRY_TYPES,
    safe_to_geojson,
    safe_to_shapely,
    validate_coordinates_wgs84,
    validate_geojson_dict,
)

__all__ = [
    "SUPPORTED_GEOMETRY_TYPES",
    "validate_coordinates_wgs84",
    "validate_geojson_dict",
    "safe_to_shapely",
    "safe_to_geojson",
    "transform_to_epsg3857",
    "transform_to_epsg4326",
    "calculate_haversine_distance_m",
    "buffer_geometry_meters",
    "get_bounding_box",
    "get_centroid",
    "calculate_area_sq_meters",
    "calculate_length_meters",
    "check_point_in_polygon",
    "compute_intersection",
    "compute_union",
]
