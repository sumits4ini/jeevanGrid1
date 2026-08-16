"""
Tests for Coordinate Transformations and Metric Geodesic Calculations
"""

import pytest
import shapely
from gis_engine.geometry.transforms import (
    buffer_geometry_meters,
    calculate_haversine_distance_m,
    transform_to_epsg3857,
    transform_to_epsg4326,
)


def test_crs_transformation_roundtrip():
    """Verifies EPSG:4326 -> EPSG:3857 -> EPSG:4326 coordinate fidelity."""
    original_pt = shapely.Point(91.0063, 26.3216)
    pt_3857 = transform_to_epsg3857(original_pt)

    # In 3857, coordinates are in meters (x > 10,000,000, y > 3,000,000 for India)
    assert pt_3857.x > 10000000
    assert pt_3857.y > 3000000

    pt_4326 = transform_to_epsg4326(pt_3857)
    assert pytest.approx(pt_4326.x, rel=1e-5) == original_pt.x
    assert pytest.approx(pt_4326.y, rel=1e-5) == original_pt.y


def test_haversine_distance_calculation():
    """Verifies Haversine formula against known reference distance."""
    # Distance between Barpeta (91.0063, 26.3216) and Guwahati (91.7362, 26.1445) is ~75 km
    dist_m = calculate_haversine_distance_m(91.0063, 26.3216, 91.7362, 26.1445)
    dist_km = dist_m / 1000.0
    assert 70.0 <= dist_km <= 80.0


def test_buffer_geometry_meters():
    """Verifies that buffering a point produces a Polygon with expanded bounds."""
    pt = shapely.Point(91.0063, 26.3216)
    buffered = buffer_geometry_meters(pt, radius_meters=1000.0)  # 1 km buffer

    assert isinstance(buffered, shapely.Polygon)
    assert buffered.is_valid
    bounds = buffered.bounds
    # Check that bounding box extends in all directions
    assert bounds[0] < 91.0063 < bounds[2]
    assert bounds[1] < 26.3216 < bounds[3]
