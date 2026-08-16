"""
Coordinate Reference System (CRS) Transformations and Geodesic Calculations
"""

import math
from typing import Any, Dict, Tuple, Union
import pyproj
import shapely
from shapely.ops import transform
from gis_engine.geometry.validation import safe_to_shapely

# Reusable Transformer instances
_WGS84_CRS = pyproj.CRS("EPSG:4326")
_WEB_MERCATOR_CRS = pyproj.CRS("EPSG:3857")

# Pyproj transformers: always_xy=True ensures (longitude, latitude) coordinate order
_to_3857_transformer = pyproj.Transformer.from_crs(_WGS84_CRS, _WEB_MERCATOR_CRS, always_xy=True)
_to_4326_transformer = pyproj.Transformer.from_crs(_WEB_MERCATOR_CRS, _WGS84_CRS, always_xy=True)


def transform_to_epsg3857(geometry: Union[shapely.Geometry, Dict[str, Any], str]) -> shapely.Geometry:
    """Transforms a geometry from WGS84 (EPSG:4326) to Web Mercator (EPSG:3857 meters)."""
    geom_obj = safe_to_shapely(geometry)
    return transform(_to_3857_transformer.transform, geom_obj)


def transform_to_epsg4326(geometry: Union[shapely.Geometry, Dict[str, Any], str]) -> shapely.Geometry:
    """Transforms a geometry from Web Mercator (EPSG:3857) to WGS84 (EPSG:4326 degrees)."""
    geom_obj = safe_to_shapely(geometry)
    return transform(_to_4326_transformer.transform, geom_obj)


def calculate_haversine_distance_m(lng1: float, lat1: float, lng2: float, lat2: float) -> float:
    """
    Computes great-circle geodesic distance between two points on Earth in meters.
    Formula: Haversine equation.
    """
    EARTH_RADIUS_M = 6371008.8  # Mean Earth radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_M * c


def buffer_geometry_meters(
    geometry: Union[shapely.Geometry, Dict[str, Any], str],
    radius_meters: float,
    quad_segs: int = 16,
) -> shapely.Geometry:
    """
    Applies an accurate metric buffer around a WGS84 (EPSG:4326) geometry.
    Projects to EPSG:3857, buffers in meters, and transforms back to EPSG:4326.
    """
    if radius_meters <= 0:
        return safe_to_shapely(geometry)

    geom_3857 = transform_to_epsg3857(geometry)
    buffered_3857 = geom_3857.buffer(radius_meters, quad_segs=quad_segs)
    return transform_to_epsg4326(buffered_3857)
