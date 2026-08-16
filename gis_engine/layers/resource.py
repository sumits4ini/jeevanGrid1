"""
Emergency Response Units GIS Layer Implementation
"""

from typing import Any, Dict, List, Optional
from gis_engine.layers.base import BaseGISLayer
from gis_engine.schemas.geometry import BoundingBox


class ResourceLayer(BaseGISLayer):
    """GIS operational layer for mobile emergency rescue units and assets."""

    def __init__(self, data_source: Optional[List[Dict[str, Any]]] = None):
        super().__init__(
            layer_id="response_units",
            name="Emergency Response Units & Fleet",
            description="Real-time locations of NDRF teams, rescue boats, ambulances, and supply logistics.",
            geometry_type="Point",
            properties_schema={
                "unit_code": "string",
                "unit_type": "string (NDRF_TEAM, RESCUE_BOAT, AMBULANCE, FOOD_WATER_TRUCK)",
                "status": "string (AVAILABLE, DISPATCHED, ON_MISSION)",
                "capacity_payload": "object",
            },
        )
        self.data_source = data_source or self._get_default_scenario_data()

    def _get_default_scenario_data(self) -> List[Dict[str, Any]]:
        """Baseline emergency fleet telemetry."""
        return [
            {
                "id": "ru-boat-01",
                "layer_id": "response_units",
                "name": "NDRF Rescue Boat Alpha-1",
                "unit_code": "BOAT-NDRF-01",
                "unit_type": "RESCUE_BOAT",
                "status": "AVAILABLE",
                "latitude": 26.3120,
                "longitude": 91.0150,
                "geometry": {
                    "type": "Point",
                    "coordinates": [91.0150, 26.3120],
                },
                "capacity_payload": {"boat_capacity": 12, "medics": 2, "life_jackets": 24},
            },
            {
                "id": "ru-boat-02",
                "layer_id": "response_units",
                "name": "NDRF Rescue Boat Alpha-2",
                "unit_code": "BOAT-NDRF-02",
                "unit_type": "RESCUE_BOAT",
                "status": "AVAILABLE",
                "latitude": 26.3180,
                "longitude": 91.0220,
                "geometry": {
                    "type": "Point",
                    "coordinates": [91.0220, 26.3180],
                },
                "capacity_payload": {"boat_capacity": 12, "medics": 2, "life_jackets": 24},
            },
            {
                "id": "ru-amb-01",
                "layer_id": "response_units",
                "name": "ALS Ambulance Unit 108-A",
                "unit_code": "AMB-108-A",
                "unit_type": "AMBULANCE",
                "status": "AVAILABLE",
                "latitude": 26.3350,
                "longitude": 91.0300,
                "geometry": {
                    "type": "Point",
                    "coordinates": [91.0300, 26.3350],
                },
                "capacity_payload": {"stretchers": 2, "oxygen_cylinders": 4},
            },
        ]

    def get_features(
        self,
        bbox: Optional[BoundingBox] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        results = self.data_source

        if bbox:
            results = [
                item
                for item in results
                if bbox.min_lng <= item["longitude"] <= bbox.max_lng
                and bbox.min_lat <= item["latitude"] <= bbox.max_lat
            ]

        if filters:
            for k, v in filters.items():
                results = [item for item in results if item.get(k) == v]

        return results
