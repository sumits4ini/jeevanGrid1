"""
Resource Allocation Service
"""

from typing import Any, Dict, List, Optional
from gis_engine.services.gis_service import gis_service
from response_optimization.algorithms.allocation import allocate_resources_deterministically
from response_optimization.schemas.allocation import (
    ResourceAllocationRequest,
    ResourceAllocationResponse,
)


class ResourceAllocationService:
    """Coordinates fleet availability from GIS layer and executes capacitated allocation."""

    def allocate(
        self, request: ResourceAllocationRequest
    ) -> ResourceAllocationResponse:
        # Retrieve candidate units: from request or live GIS resource layer
        available_resources = request.available_resources
        if available_resources is None:
            layer = gis_service.registry.get_layer("response_units")
            available_resources = layer.get_features() if layer else []

        return allocate_resources_deterministically(
            incidents=request.incidents,
            available_resources=available_resources,
            max_search_radius_km=request.max_search_radius_km,
            enforce_strict_capacity=request.enforce_strict_capacity,
        )


# Global default instance
allocation_service = ResourceAllocationService()
