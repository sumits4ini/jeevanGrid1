"""
Intelligent Resource Prioritization Service
"""

from typing import Any, Dict, List, Optional
from backend.app.core.exceptions import AIValidationException
from backend.app.core.logging import logger
from backend.app.schemas.ai import (
    ResourcePrioritizationRequest,
    ResourcePrioritizationResponse,
)
from ai_services.providers.base import BaseAIProvider
from ai_services.providers.factory import get_ai_provider
from gis_engine.services.gis_service import gis_service


class ResourcePrioritizationService:
    """Evaluates emergency response unit availability, distance, and task allocations."""

    def __init__(self, provider: Optional[BaseAIProvider] = None):
        self.provider = provider or get_ai_provider()

    async def prioritize_resources(
        self,
        request: ResourcePrioritizationRequest,
    ) -> ResourcePrioritizationResponse:
        """Retrieves fleet from GIS layer and computes AI-prioritized rescue unit allocation."""
        if not (-90.0 <= request.target_latitude <= 90.0) or not (-180.0 <= request.target_longitude <= 180.0):
            raise AIValidationException(
                message=f"Invalid target coordinates ({request.target_latitude}, {request.target_longitude})."
            )

        logger.info(
            f"Executing AI Resource Prioritization for target ({request.target_latitude}, {request.target_longitude}) "
            f"Radius: {request.max_search_radius_km}km, Type: {request.disaster_type}"
        )

        # Retrieve available response units from GIS Engine Resource Layer
        response_units_layer = gis_service.registry.get_layer("response_units")
        raw_units: List[Dict[str, Any]] = []
        if response_units_layer:
            raw_units = response_units_layer.get_features()

        return await self.provider.prioritize_resources(
            request=request,
            available_units=raw_units,
        )
