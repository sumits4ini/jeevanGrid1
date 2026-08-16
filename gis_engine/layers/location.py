"""
Critical Infrastructure and Location GIS Layer Implementation
"""

from typing import Any, Dict, List, Optional
from gis_engine.layers.base import BaseGISLayer
from gis_engine.schemas.geometry import BoundingBox


class LocationLayer(BaseGISLayer):
    """GIS operational layer for critical infrastructure assets (hospitals, power, shelters)."""

    def __init__(self, data_source: Optional[List[Dict[str, Any]]] = None):
        super().__init__(
            layer_id="infrastructure",
            name="Critical Infrastructure & Shelters",
            description="Hospitals, power substations, water treatment plants, bridges, and emergency shelters.",
            geometry_type="Point",
            properties_schema={
                "name": "string",
                "facility_type": "string (HOSPITAL, POWER_SUBSTATION, WATER_TREATMENT, BRIDGE, SHELTER)",
                "operational_status": "string (OPERATIONAL, DEGRADED, FAILED, CUT_OFF)",
                "max_capacity": "integer",
                "current_occupancy": "integer",
                "backup_power_hours": "float",
            },
        )
        self.data_source = data_source or self._get_default_scenario_data()

    def _get_default_scenario_data(self) -> List[Dict[str, Any]]:
        """Baseline critical infrastructure assets around Barpeta district."""
        return [
            {
                "id": "ci-hosp-01",
                "layer_id": "infrastructure",
                "name": "Barpeta Civil Hospital",
                "facility_type": "HOSPITAL",
                "operational_status": "OPERATIONAL",
                "latitude": 26.3245,
                "longitude": 91.0092,
                "geometry": {
                    "type": "Point",
                    "coordinates": [91.0092, 26.3245],
                },
                "max_capacity": 350,
                "current_occupancy": 120,
                "backup_power_hours": 6.0,
                "contact_phone": "+91-3665-252000",
            },
            {
                "id": "ci-bridge-12",
                "layer_id": "infrastructure",
                "name": "Bridge B-12 (NH-31 Link)",
                "facility_type": "BRIDGE",
                "operational_status": "CUT_OFF",
                "latitude": 26.3150,
                "longitude": 91.0020,
                "geometry": {
                    "type": "Point",
                    "coordinates": [91.0020, 26.3150],
                },
                "max_capacity": 0,
                "current_occupancy": 0,
                "backup_power_hours": 0.0,
            },
            {
                "id": "ci-power-04",
                "layer_id": "infrastructure",
                "name": "Barpeta East Power Substation #4",
                "facility_type": "POWER_SUBSTATION",
                "operational_status": "DEGRADED",
                "latitude": 26.3310,
                "longitude": 91.0180,
                "geometry": {
                    "type": "Point",
                    "coordinates": [91.0180, 26.3310],
                },
                "max_capacity": 0,
                "current_occupancy": 0,
                "backup_power_hours": 12.0,
            },
            {
                "id": "ci-shelter-03",
                "layer_id": "infrastructure",
                "name": "Sector 4 Relief Shelter (High School)",
                "facility_type": "SHELTER",
                "operational_status": "OPERATIONAL",
                "latitude": 26.3410,
                "longitude": 91.0250,
                "geometry": {
                    "type": "Point",
                    "coordinates": [91.0250, 26.3410],
                },
                "max_capacity": 1500,
                "current_occupancy": 1420,
                "backup_power_hours": 48.0,
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
