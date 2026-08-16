"""
Pure Geometric and Spatial Operations
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import shapely
from gis_engine.geometry.transforms import transform_to_epsg3857
from gis_engine.geometry.validation import safe_to_shapely, safe_to_geojson


def get_bounding_box(geometry: Union[shapely.Geometry, Dict[str, Any], str]) -> List[float]:
    """Returns the [min_lng, min_lat, max_lng, max_lat] bounding box of a geometry."""
    geom = safe_to_shapely(geometry)
    bounds = geom.bounds  # (minx, miny, maxx, maxy)
    return [float(bounds[0]), float(bounds[1]), float(bounds[2]), float(bounds[3])]


def get_centroid(geometry: Union[shapely.Geometry, Dict[str, Any], str]) -> Tuple[float, float]:
    """Returns the (longitude, latitude) centroid coordinate."""
    geom = safe_to_shapely(geometry)
    c = geom.centroid
    return float(c.x), float(c.y)


def calculate_area_sq_meters(geometry: Union[shapely.Geometry, Dict[str, Any], str]) -> float:
    """Computes accurate geodesic surface area in square meters."""
    geom_3857 = transform_to_epsg3857(geometry)
    return float(geom_3857.area)


def calculate_length_meters(geometry: Union[shapely.Geometry, Dict[str, Any], str]) -> float:
    """Computes accurate line length in meters."""
    geom_3857 = transform_to_epsg3857(geometry)
    return float(geom_3857.length)


def check_point_in_polygon(
    point: Union[Tuple[float, float], List[float], Dict[str, Any], shapely.Point],
    polygon: Union[Dict[str, Any], str, shapely.Polygon, shapely.MultiPolygon],
) -> bool:
    """Checks if a point (lng, lat) is within or on the boundary of a polygon."""
    if isinstance(point, (tuple, list)):
        pt_geom = shapely.Point(point[0], point[1])
    elif isinstance(point, dict) and "coordinates" in point:
        coords = point["coordinates"]
        pt_geom = shapely.Point(coords[0], coords[1])
    else:
        pt_geom = safe_to_shapely(point)

    poly_geom = safe_to_shapely(polygon)
    return bool(poly_geom.contains(pt_geom) or poly_geom.intersects(pt_geom))


def compute_intersection(
    geom1: Union[shapely.Geometry, Dict[str, Any], str],
    geom2: Union[shapely.Geometry, Dict[str, Any], str],
) -> Optional[Dict[str, Any]]:
    """Computes geometric intersection and returns GeoJSON dict or None if disjoint."""
    g1 = safe_to_shapely(geom1)
    g2 = safe_to_shapely(geom2)

    if not g1.intersects(g2):
        return None

    intersected = g1.intersection(g2)
    if intersected.is_empty:
        return None

    return safe_to_geojson(intersected)


def compute_union(
    geometries: List[Union[shapely.Geometry, Dict[str, Any], str]]
) -> Dict[str, Any]:
    """Computes unary union of a list of geometries and returns GeoJSON dict."""
    if not geometries:
        raise ValueError("Cannot compute union of an empty geometry list")
    
    shapely_geoms = [safe_to_shapely(g) for g in geometries]
    union_geom = shapely.unary_union(shapely_geoms)
    return safe_to_geojson(union_geom)
