"""
Hazard Inundation and Risk Zones GIS Layer Implementation
"""

from typing import Any, Dict, List, Optional
from gis_engine.geometry.operations import get_bounding_box
from gis_engine.layers.base import BaseGISLayer
from gis_engine.schemas.geometry import BoundingBox


class HazardZoneLayer(BaseGISLayer):
    """GIS operational layer for flood inundation perimeters and spatial risk zones."""

    def __init__(self, data_source: Optional[List[Dict[str, Any]]] = None):
        super().__init__(
            layer_id="hazard_zones",
            name="Hazard Inundation & Risk Zones",
            description="MultiPolygon boundaries of active flood inundation, storm surge, or fire perimeters.",
            geometry_type="MultiPolygon",
            properties_schema={
                "name": "string",
                "disaster_id": "string",
                "inundation_depth_m": "float (meters)",
                "hazard_intensity": "float (0.0 to 1.0)",
                "risk_level": "string (CRITICAL, HIGH, MODERATE, LOW)",
                "is_active": "boolean",
            },
        )
        self.data_source = data_source or self._get_default_scenario_data()

    def _get_default_scenario_data(self) -> List[Dict[str, Any]]:
        """Baseline high-fidelity hazard polygons (Barpeta District sector flood)."""
        return [
            {
                "id": "hz-sector-east-deep",
                "layer_id": "hazard_zones",
                "disaster_id": "d1-assam-flood-2026",
                "name": "Sector East Deep Inundation Zone (Wards 4 & 7)",
                "inundation_depth_m": 1.25,
                "hazard_intensity": 0.88,
                "risk_level": "CRITICAL",
                "is_active": True,
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [90.9850, 26.3100],
                                [91.0250, 26.3100],
                                [91.0350, 26.3380],
                                [90.9900, 26.3420],
                                [90.9850, 26.3100],
                            ]
                        ]
                    ],
                },
            },
            {
                "id": "hz-sector-west-moderate",
                "layer_id": "hazard_zones",
                "disaster_id": "d1-assam-flood-2026",
                "name": "Sector West Moderate Flood Buffer",
                "inundation_depth_m": 0.45,
                "hazard_intensity": 0.55,
                "risk_level": "HIGH",
                "is_active": True,
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [90.9400, 26.2950],
                                [90.9800, 26.2950],
                                [90.9800, 26.3250],
                                [90.9350, 26.3200],
                                [90.9400, 26.2950],
                            ]
                        ]
                    ],
                },
            },
        ]

    def get_features(
        self,
        bbox: Optional[BoundingBox] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        results = self.data_source

        # Filter by bbox intersection
        if bbox:
            filtered = []
            for item in results:
                geom = item.get("geometry", {})
                item_bbox = get_bounding_box(geom)
                # Check if item_bbox overlaps query bbox
                if not (
                    item_bbox[2] < bbox.min_lng
                    or item_bbox[0] > bbox.max_lng
                    or item_bbox[3] < bbox.min_lat
                    or item_bbox[1] > bbox.max_lat
                ):
                    filtered.append(item)
            results = filtered

        # Apply property filters
        if filters:
            for k, v in filters.items():
                results = [item for item in results if item.get(k) == v]

        return results
