"""
Tests for Geometry Validation and Conversion Utilities
"""

import pytest
import shapely
from gis_engine.geometry.validation import (
    safe_to_geojson,
    safe_to_shapely,
    validate_coordinates_wgs84,
    validate_geojson_dict,
)


def test_validate_coordinates_wgs84_valid():
    """Verifies valid WGS84 coordinate pairs."""
    valid, msg = validate_coordinates_wgs84(91.0063, 26.3216)
    assert valid is True
    assert msg == "Valid"


def test_validate_coordinates_wgs84_invalid():
    """Verifies out-of-range coordinates are rejected."""
    valid_lng_err, msg1 = validate_coordinates_wgs84(185.0, 26.0)
    assert valid_lng_err is False
    assert "Longitude" in msg1

    valid_lat_err, msg2 = validate_coordinates_wgs84(90.0, -95.0)
    assert valid_lat_err is False
    assert "Latitude" in msg2


def test_validate_geojson_dict_valid_point():
    """Verifies valid GeoJSON Point structure."""
    geojson_point = {"type": "Point", "coordinates": [91.0063, 26.3216]}
    valid, msg = validate_geojson_dict(geojson_point)
    assert valid is True
    assert msg == "Valid"


def test_validate_geojson_dict_valid_polygon():
    """Verifies valid closed GeoJSON Polygon structure."""
    geojson_polygon = {
        "type": "Polygon",
        "coordinates": [
            [
                [90.98, 26.30],
                [91.02, 26.30],
                [91.02, 26.34],
                [90.98, 26.34],
                [90.98, 26.30],
            ]
        ],
    }
    valid, msg = validate_geojson_dict(geojson_polygon)
    assert valid is True


def test_validate_geojson_dict_invalid_type():
    """Verifies unsupported geometry types are caught."""
    invalid_geojson = {"type": "CircularString", "coordinates": [0, 0]}
    valid, msg = validate_geojson_dict(invalid_geojson)
    assert valid is False
    assert "Unsupported geometry type" in msg


def test_safe_to_shapely_and_geojson_roundtrip():
    """Verifies conversion between dict and Shapely object."""
    input_dict = {"type": "Point", "coordinates": [91.0063, 26.3216]}
    shapely_geom = safe_to_shapely(input_dict)
    assert isinstance(shapely_geom, shapely.Point)
    assert shapely_geom.x == 91.0063
    assert shapely_geom.y == 26.3216

    output_dict = safe_to_geojson(shapely_geom)
    assert output_dict["type"] == "Point"
    assert output_dict["coordinates"] == (91.0063, 26.3216)
