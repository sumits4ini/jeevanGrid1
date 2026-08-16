"""
Central GIS Layer Registry and Multi-Layer Query Dispatcher
"""

from typing import Any, Dict, List, Optional, Union
from gis_engine.layers.base import BaseGISLayer
from gis_engine.layers.disaster import DisasterLayer
from gis_engine.layers.hazard_zone import HazardZoneLayer
from gis_engine.layers.location import LocationLayer
from gis_engine.layers.resource import ResourceLayer
from gis_engine.schemas.geometry import BoundingBox, GeoJSONFeature, GeoJSONFeatureCollection
from gis_engine.schemas.layer import (
    IntersectedLayerResult,
    LayerMetadata,
    LayerSummary,
    NearbyFeatureItem,
    NearbyQueryResponse,
    SpatialIntersectionResponse,
)
from gis_engine.spatial.intersections import evaluate_polygon_intersections
from gis_engine.spatial.proximity import filter_and_rank_nearby_features


class LayerRegistry:
    """Singleton registry managing operational GIS layers and spatial routing."""

    def __init__(self):
        self._layers: Dict[str, BaseGISLayer] = {}
        self._register_default_layers()

    def _register_default_layers(self) -> None:
        """Registers the 4 primary JeevanGrid disaster intelligence layers."""
        self.register_layer(DisasterLayer())
        self.register_layer(HazardZoneLayer())
        self.register_layer(LocationLayer())
        self.register_layer(ResourceLayer())

    def register_layer(self, layer: BaseGISLayer) -> None:
        """Registers or replaces a GIS layer."""
        self._layers[layer.layer_id] = layer

    def get_layer(self, layer_id: str) -> Optional[BaseGISLayer]:
        """Retrieves a layer by unique layer_id."""
        return self._layers.get(layer_id)

    def list_layers(self) -> LayerSummary:
        """Returns metadata descriptors for all registered layers."""
        metadata_list: List[LayerMetadata] = []
        for layer_id, layer in self._layers.items():
            items = layer.get_features()
            metadata_list.append(layer.get_metadata(count=len(items)))

        return LayerSummary(
            total_layers=len(metadata_list),
            layers=metadata_list,
        )

    def query_features(
        self,
        layer_ids: Optional[List[str]] = None,
        bbox: Optional[BoundingBox] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> GeoJSONFeatureCollection:
        """Queries GeoJSON features across multiple or all layers."""
        target_layers = layer_ids or list(self._layers.keys())
        all_features: List[GeoJSONFeature] = []

        for lid in target_layers:
            layer = self._layers.get(lid)
            if layer:
                items = layer.get_features(bbox=bbox, filters=filters)
                all_features.extend(layer.to_geojson_features(items))

        return GeoJSONFeatureCollection(
            type="FeatureCollection",
            features=all_features,
            metadata={
                "queried_layers": target_layers,
                "total_features": len(all_features),
                "bbox": bbox.to_list() if bbox else None,
            },
        )

    def find_nearby(
        self,
        center_lat: float,
        center_lng: float,
        radius_meters: float = 5000.0,
        layer_names: Optional[List[str]] = None,
        limit: int = 50,
    ) -> NearbyQueryResponse:
        """Finds nearby features across layers within a radius in meters."""
        target_layers = layer_names or list(self._layers.keys())
        candidates: List[Dict[str, Any]] = []

        for lid in target_layers:
            layer = self._layers.get(lid)
            if layer:
                candidates.extend(layer.get_features())

        nearby_items = filter_and_rank_nearby_features(
            features=candidates,
            center_lng=center_lng,
            center_lat=center_lat,
            radius_meters=radius_meters,
            limit=limit,
        )

        return NearbyQueryResponse(
            center={"lat": center_lat, "lng": center_lng},
            radius_meters=radius_meters,
            total_found=len(nearby_items),
            features=nearby_items,
        )

    def compute_intersections(
        self,
        target_geometry: Dict[str, Any],
        intersect_layers: Optional[List[str]] = None,
        buffer_meters: float = 0.0,
    ) -> SpatialIntersectionResponse:
        """Evaluates intersection of a target polygon against layers."""
        import uuid

        target_layer_ids = intersect_layers or ["infrastructure", "response_units", "hazard_zones"]
        results_by_layer: Dict[str, IntersectedLayerResult] = {}
        total_intersected = 0

        for lid in target_layer_ids:
            layer = self._layers.get(lid)
            if layer:
                candidates = layer.get_features()
                res = evaluate_polygon_intersections(
                    target_polygon=target_geometry,
                    candidate_features=candidates,
                    layer_id=lid,
                    buffer_meters=buffer_meters,
                )
                results_by_layer[lid] = res
                total_intersected += res.intersected_count

        return SpatialIntersectionResponse(
            intersection_id=str(uuid.uuid4()),
            buffer_applied_meters=buffer_meters,
            total_intersected_features=total_intersected,
            results_by_layer=results_by_layer,
        )


# Global default registry instance
layer_registry = LayerRegistry()
