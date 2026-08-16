"""
Tests for Spatial Operations (Point-in-Polygon, Area, Length, Intersection)
"""

import pytest
import shapely
from gis_engine.geometry.operations import (
    calculate_area_sq_meters,
    calculate_length_meters,
    check_point_in_polygon,
    compute_intersection,
    compute_union,
    get_bounding_box,
    get_centroid,
)


def test_point_in_polygon():
    """Verifies point containment inside a polygon."""
    polygon = {
        "type": "Polygon",
        "coordinates": [
            [
                [90.0, 25.0],
                [92.0, 25.0],
                [92.0, 27.0],
                [90.0, 27.0],
                [90.0, 25.0],
            ]
        ],
    }

    inside_point = (91.0, 26.0)
    outside_point = (95.0, 30.0)

    assert check_point_in_polygon(inside_point, polygon) is True
    assert check_point_in_polygon(outside_point, polygon) is False


def test_bounding_box_and_centroid():
    """Verifies bounding box and centroid calculations."""
    pt = shapely.Point(91.0063, 26.3216)
    bbox = get_bounding_box(pt)
    assert bbox == [91.0063, 26.3216, 91.0063, 26.3216]

    cx, cy = get_centroid(pt)
    assert cx == 91.0063
    assert cy == 26.3216


def test_calculate_area_and_length():
    """Verifies geodesic area and length calculations."""
    poly = shapely.Polygon([
        (91.00, 26.00),
        (91.01, 26.00),
        (91.01, 26.01),
        (91.00, 26.01),
        (91.00, 26.00),
    ])
    area_sq_m = calculate_area_sq_meters(poly)
    assert area_sq_m > 500000  # Approx ~1.1 sq km

    line = shapely.LineString([(91.00, 26.00), (91.01, 26.00)])
    len_m = calculate_length_meters(line)
    assert 900.0 <= len_m <= 1200.0  # Approx ~1 km


def test_compute_intersection():
    """Verifies geometric intersection of two overlapping polygons."""
    poly1 = shapely.Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
    poly2 = shapely.Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])

    intersection = compute_intersection(poly1, poly2)
    assert intersection is not None
    assert intersection["type"] == "Polygon"


def test_compute_union():
    """Verifies geometric union of polygons."""
    poly1 = shapely.Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    poly2 = shapely.Polygon([(1, 0), (2, 0), (2, 1), (1, 1), (1, 0)])

    union = compute_union([poly1, poly2])
    assert union is not None
    assert union["type"] == "Polygon"
