"""
Disasters GIS Layer Implementation
"""

from typing import Any, Dict, List, Optional
from gis_engine.layers.base import BaseGISLayer
from gis_engine.schemas.geometry import BoundingBox


class DisasterLayer(BaseGISLayer):
    """GIS operational layer for disaster incident centers and alerts."""

    def __init__(self, data_source: Optional[List[Dict[str, Any]]] = None):
        super().__init__(
            layer_id="disasters",
            name="Disaster Events & Epicenters",
            description="Active, simulated, and historical disaster event centers with severity ratings.",
            geometry_type="Point",
            properties_schema={
                "name": "string",
                "disaster_type": "string (FLOOD, CYCLONE, LANDSLIDE, EARTHQUAKE)",
                "severity_level": "integer (1-5)",
                "status": "string (ACTIVE, CONTAINED, RESOLVED)",
                "affected_population_estimate": "integer",
            },
        )
        self.data_source = data_source or self._get_default_scenario_data()

    def _get_default_scenario_data(self) -> List[Dict[str, Any]]:
        """Baseline high-fidelity disaster scenario dataset."""
        return [
            {
                "id": "d1-assam-flood-2026",
                "layer_id": "disasters",
                "name": "Assam Brahmaputra Flash Flood 2026",
                "disaster_type": "FLOOD",
                "severity_level": 4,
                "status": "ACTIVE",
                "description": "Severe river overflow and flood wave propagating through Barpeta lowlands.",
                "latitude": 26.3216,
                "longitude": 91.0063,
                "geometry": {
                    "type": "Point",
                    "coordinates": [91.0063, 26.3216],
                },
                "affected_population_estimate": 85400,
            },
            {
                "id": "d2-chennai-surge-2026",
                "layer_id": "disasters",
                "name": "Chennai Coastal Storm Surge Alert",
                "disaster_type": "CYCLONE",
                "severity_level": 3,
                "status": "ACTIVE",
                "description": "Storm surge advisory for low-lying coastal sectors.",
                "latitude": 13.0827,
                "longitude": 80.2707,
                "geometry": {
                    "type": "Point",
                    "coordinates": [80.2707, 13.0827],
                },
                "affected_population_estimate": 32000,
            },
        ]

    def get_features(
        self,
        bbox: Optional[BoundingBox] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        results = self.data_source

        # Apply Bbox filter if provided
        if bbox:
            results = [
                item
                for item in results
                if bbox.min_lng <= item["longitude"] <= bbox.max_lng
                and bbox.min_lat <= item["latitude"] <= bbox.max_lat
            ]

        # Apply property filters
        if filters:
            for k, v in filters.items():
                results = [item for item in results if item.get(k) == v]

        return results
