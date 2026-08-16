"""
Disaster Risk Intelligence Service
"""

from typing import Any, Dict, Optional
from backend.app.core.exceptions import AIValidationException
from backend.app.core.logging import logger
from backend.app.schemas.ai import RiskAnalysisRequest, RiskAnalysisResponse
from ai_services.providers.base import BaseAIProvider
from ai_services.providers.factory import get_ai_provider
from gis_engine.services.gis_service import gis_service


class DisasterRiskService:
    """Orchestrates AI-assisted disaster risk assessment and spatial risk intelligence."""

    def __init__(self, provider: Optional[BaseAIProvider] = None):
        self.provider = provider or get_ai_provider()

    async def analyze_risk(self, request: RiskAnalysisRequest) -> RiskAnalysisResponse:
        """Enriches request with GIS hazard layers and computes AI risk assessment."""
        if not (-90.0 <= request.latitude <= 90.0) or not (-180.0 <= request.longitude <= 180.0):
            raise AIValidationException(
                message=f"Invalid coordinates ({request.latitude}, {request.longitude}) for risk analysis."
            )

        logger.info(
            f"Executing AI Disaster Risk Analysis for {request.disaster_name} "
            f"({request.disaster_type}, Lv {request.severity_level}) at ({request.latitude}, {request.longitude})"
        )

        # Query nearby critical infrastructure from GIS engine to enrich context
        try:
            nearby_resp = gis_service.find_nearby_features(
                latitude=request.latitude,
                longitude=request.longitude,
                radius_meters=10000.0,
                layer_names=["infrastructure", "hazard_zones"],
                limit=10,
            )
            if nearby_resp and nearby_resp.total_found > 0:
                monitored = [f"{f.name} ({f.distance_meters}m)" for f in nearby_resp.features[:5]]
                request.monitored_zones.extend(monitored)
        except Exception as exc:
            logger.warning(f"GIS enrichment for risk analysis encountered warning: {exc}")

        return await self.provider.analyze_disaster_risk(request)
