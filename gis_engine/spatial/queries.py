"""
Reusable PostGIS Spatial Query Helpers and SQL Expressions
"""

from typing import Any, List, Optional
from geoalchemy2.functions import (
    ST_Contains,
    ST_Distance,
    ST_DWithin,
    ST_GeogFromWKB,
    ST_Intersects,
    ST_MakeEnvelope,
    ST_Within,
)
from sqlalchemy import BinaryExpression, func, select
from gis_engine.schemas.geometry import BoundingBox


def build_bbox_intersects_clause(
    geometry_column: Any,
    bbox: BoundingBox,
    srid: int = 4326,
) -> BinaryExpression:
    """
    Builds a PostGIS ST_Intersects clause with a bounding box envelope.
    Uses ST_MakeEnvelope(min_lng, min_lat, max_lng, max_lat, srid).
    """
    envelope = func.ST_MakeEnvelope(
        bbox.min_lng,
        bbox.min_lat,
        bbox.max_lng,
        bbox.max_lat,
        srid,
    )
    return func.ST_Intersects(geometry_column, envelope)


def build_point_radius_dwithin_clause(
    geometry_column: Any,
    center_lng: float,
    center_lat: float,
    radius_meters: float,
    srid: int = 4326,
) -> BinaryExpression:
    """
    Builds a PostGIS ST_DWithin query in meters using cast to geography.
    """
    center_point = func.ST_SetSRID(func.ST_MakePoint(center_lng, center_lat), srid)
    # Cast geometries to geography for accurate geodesic meter distance checks
    return func.ST_DWithin(
        func.cast(geometry_column, func.geography),
        func.cast(center_point, func.geography),
        radius_meters,
    )


def build_distance_expression(
    geometry_column: Any,
    center_lng: float,
    center_lat: float,
    srid: int = 4326,
) -> Any:
    """
    Returns an expression calculating distance in meters from a reference coordinate.
    """
    center_point = func.ST_SetSRID(func.ST_MakePoint(center_lng, center_lat), srid)
    return func.ST_Distance(
        func.cast(geometry_column, func.geography),
        func.cast(center_point, func.geography),
    )
