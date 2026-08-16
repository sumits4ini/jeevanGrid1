"""
High-Level GIS Service for Spatial Data Queries and Layer Dispatch
"""

from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.logging import logger
from backend.app.models.disaster import Disaster
from backend.app.models.location import CriticalInfrastructure
from backend.app.models.resource import ResponseUnit
from backend.app.models.risk_zone import HazardZone
from gis_engine.layers.registry import LayerRegistry, layer_registry
from gis_engine.schemas.geometry import BoundingBox, GeoJSONFeatureCollection
from gis_engine.schemas.layer import (
    LayerMetadata,
    LayerSummary,
    NearbyQueryResponse,
    SpatialIntersectionResponse,
)
from gis_engine.spatial.queries import build_bbox_intersects_clause, build_point_radius_dwithin_clause


class GISService:
    """Coordinates GIS operations, database spatial SQL queries, and layer metadata."""

    def __init__(self, registry: Optional[LayerRegistry] = None):
        self.registry = registry or layer_registry

    def list_layers(self) -> LayerSummary:
        """Returns metadata for all available GIS layers."""
        return self.registry.list_layers()

    def get_layer_feature_collection(
        self,
        layer_id: str,
        bbox: Optional[BoundingBox] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Optional[GeoJSONFeatureCollection]:
        """Returns GeoJSON FeatureCollection for a specific layer."""
        layer = self.registry.get_layer(layer_id)
        if not layer:
            return None
        return layer.get_feature_collection(bbox=bbox, filters=filters)

    def query_multi_layer_features(
        self,
        layer_ids: Optional[List[str]] = None,
        bbox: Optional[BoundingBox] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> GeoJSONFeatureCollection:
        """Queries features across multiple GIS layers."""
        return self.registry.query_features(layer_ids=layer_ids, bbox=bbox, filters=filters)

    def find_nearby_features(
        self,
        latitude: float,
        longitude: float,
        radius_meters: float = 5000.0,
        layer_names: Optional[List[str]] = None,
        limit: int = 50,
    ) -> NearbyQueryResponse:
        """Finds features near a given coordinate point."""
        return self.registry.find_nearby(
            center_lat=latitude,
            center_lng=longitude,
            radius_meters=radius_meters,
            layer_names=layer_names,
            limit=limit,
        )

    def compute_intersections(
        self,
        target_geometry: Dict[str, Any],
        intersect_layers: Optional[List[str]] = None,
        buffer_meters: float = 0.0,
    ) -> SpatialIntersectionResponse:
        """Computes geometric intersections for a polygon against operational layers."""
        return self.registry.compute_intersections(
            target_geometry=target_geometry,
            intersect_layers=intersect_layers,
            buffer_meters=buffer_meters,
        )


# Global default GIS service instance
gis_service = GISService()
