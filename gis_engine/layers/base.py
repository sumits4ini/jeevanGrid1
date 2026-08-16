"""
Abstract Base Class for GIS Operational Layers
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from gis_engine.schemas.geometry import BoundingBox, GeoJSONFeature, GeoJSONFeatureCollection
from gis_engine.schemas.layer import LayerMetadata


class BaseGISLayer(ABC):
    """Abstract base class representing an operational GIS layer in JeevanGrid."""

    def __init__(
        self,
        layer_id: str,
        name: str,
        description: str,
        geometry_type: str,
        properties_schema: Optional[Dict[str, str]] = None,
    ):
        self.layer_id = layer_id
        self.name = name
        self.description = description
        self.geometry_type = geometry_type
        self.properties_schema = properties_schema or {}

    @abstractmethod
    def get_features(
        self,
        bbox: Optional[BoundingBox] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves raw or model records matching spatial bbox and attributes."""
        pass

    def to_geojson_features(self, raw_items: List[Dict[str, Any]]) -> List[GeoJSONFeature]:
        """Converts raw layer items to standard GeoJSON Features."""
        features: List[GeoJSONFeature] = []
        for item in raw_items:
            geom = item.get("geometry")
            if not geom and "latitude" in item and "longitude" in item:
                geom = {
                    "type": "Point",
                    "coordinates": [float(item["longitude"]), float(item["latitude"])],
                }

            if not geom:
                continue

            properties = {k: v for k, v in item.items() if k not in ["geometry"]}
            features.append(
                GeoJSONFeature(
                    type="Feature",
                    id=str(item.get("id", "")),
                    geometry=geom,
                    properties=properties,
                )
            )
        return features

    def get_feature_collection(
        self,
        bbox: Optional[BoundingBox] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> GeoJSONFeatureCollection:
        """Returns a standard GeoJSON FeatureCollection with layer metadata."""
        items = self.get_features(bbox=bbox, filters=filters)
        geojson_features = self.to_geojson_features(items)

        return GeoJSONFeatureCollection(
            type="FeatureCollection",
            features=geojson_features,
            metadata={
                "layer_id": self.layer_id,
                "layer_name": self.name,
                "feature_count": len(geojson_features),
                "geometry_type": self.geometry_type,
            },
        )

    def get_metadata(self, count: int = 0, bbox: Optional[BoundingBox] = None) -> LayerMetadata:
        """Returns standardized LayerMetadata descriptor."""
        return LayerMetadata(
            layer_id=self.layer_id,
            name=self.name,
            description=self.description,
            geometry_type=self.geometry_type,
            srid=4326,
            feature_count=count,
            bounding_box=bbox,
            properties_schema=self.properties_schema,
            is_live=True,
        )
