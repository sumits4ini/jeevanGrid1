"""
Geometry Validation and GeoJSON Parsing Utilities
"""

from typing import Any, Dict, List, Tuple, Union
import shapely
from shapely.geometry import shape, mapping
from shapely.validation import explain_validity

SUPPORTED_GEOMETRY_TYPES = {
    "Point",
    "LineString",
    "Polygon",
    "MultiPoint",
    "MultiLineString",
    "MultiPolygon",
    "GeometryCollection",
}


def validate_coordinates_wgs84(lng: float, lat: float) -> Tuple[bool, str]:
    """Validates WGS84 longitude and latitude bounds."""
    if not isinstance(lng, (int, float)) or not isinstance(lat, (int, float)):
        return False, f"Coordinates must be numeric, got lng={type(lng).__name__}, lat={type(lat).__name__}"
    if not (-180.0 <= lng <= 180.0):
        return False, f"Longitude {lng} out of range [-180.0, 180.0]"
    if not (-90.0 <= lat <= 90.0):
        return False, f"Latitude {lat} out of range [-90.0, 90.0]"
    return True, "Valid"


def validate_geojson_dict(geojson: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates structure and geometry type of a GeoJSON dictionary."""
    if not isinstance(geojson, dict):
        return False, "GeoJSON must be a dictionary"
    
    geom_type = geojson.get("type")
    if not geom_type or geom_type not in SUPPORTED_GEOMETRY_TYPES:
        return False, f"Unsupported geometry type: '{geom_type}'. Supported: {sorted(SUPPORTED_GEOMETRY_TYPES)}"

    if geom_type == "GeometryCollection":
        geometries = geojson.get("geometries")
        if not isinstance(geometries, list):
            return False, "GeometryCollection must have a 'geometries' list"
        for sub_geom in geometries:
            valid, msg = validate_geojson_dict(sub_geom)
            if not valid:
                return False, f"Invalid sub-geometry in GeometryCollection: {msg}"
        return True, "Valid"

    coords = geojson.get("coordinates")
    if coords is None:
        return False, f"Geometry type '{geom_type}' requires 'coordinates'"

    try:
        geom_obj = shape(geojson)
        if not geom_obj.is_valid:
            reason = explain_validity(geom_obj)
            return False, f"Invalid topological geometry: {reason}"
        return True, "Valid"
    except Exception as exc:
        return False, f"Failed to parse geometry: {str(exc)}"


def safe_to_shapely(geometry: Union[Dict[str, Any], str, shapely.Geometry]) -> shapely.Geometry:
    """Safely parses a GeoJSON dict, WKT string, or Shapely geometry into a valid Shapely object."""
    if isinstance(geometry, shapely.Geometry):
        if not geometry.is_valid:
            return shapely.make_valid(geometry)
        return geometry

    if isinstance(geometry, str):
        try:
            geom = shapely.from_wkt(geometry)
            if not geom.is_valid:
                return shapely.make_valid(geom)
            return geom
        except Exception as exc:
            raise ValueError(f"Invalid WKT geometry: {str(exc)}")

    if isinstance(geometry, dict):
        # Check if it is a Feature object
        if geometry.get("type") == "Feature" and "geometry" in geometry:
            geometry = geometry["geometry"]
        try:
            geom = shape(geometry)
            if not geom.is_valid:
                return shapely.make_valid(geom)
            return geom
        except Exception as exc:
            raise ValueError(f"Invalid GeoJSON geometry: {str(exc)}")

    raise TypeError(f"Cannot convert type '{type(geometry).__name__}' to Shapely geometry")


def safe_to_geojson(geometry: Union[shapely.Geometry, str, Dict[str, Any]]) -> Dict[str, Any]:
    """Converts a Shapely geometry, WKT string, or dict to standard GeoJSON geometry dict."""
    if isinstance(geometry, dict):
        if geometry.get("type") == "Feature":
            return geometry.get("geometry", {})
        return geometry

    if isinstance(geometry, str):
        geom_obj = shapely.from_wkt(geometry)
        return mapping(geom_obj)

    if isinstance(geometry, shapely.Geometry):
        return mapping(geometry)

    raise TypeError(f"Cannot convert type '{type(geometry).__name__}' to GeoJSON")
