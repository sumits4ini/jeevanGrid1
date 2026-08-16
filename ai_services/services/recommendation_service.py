"""
AI Incident Recommendation Engine Service
"""

from typing import Any, Dict, Optional
from backend.app.core.exceptions import AIValidationException
from backend.app.core.logging import logger
from backend.app.schemas.ai import RecommendationRequest, RecommendationResponse
from ai_services.providers.base import BaseAIProvider
from ai_services.providers.factory import get_ai_provider


class RecommendationService:
    """Generates structured tactical recommendations for emergency operations."""

    def __init__(self, provider: Optional[BaseAIProvider] = None):
        self.provider = provider or get_ai_provider()

    async def generate_recommendations(
        self,
        request: RecommendationRequest,
    ) -> RecommendationResponse:
        """Generates multi-category operational recommendations."""
        if not (-90.0 <= request.latitude <= 90.0) or not (-180.0 <= request.longitude <= 180.0):
            raise AIValidationException(
                message=f"Invalid incident location coordinates ({request.latitude}, {request.longitude})."
            )

        logger.info(
            f"Generating AI Incident Recommendations for {request.disaster_type} (Lv {request.severity_level}) "
            f"at ({request.latitude}, {request.longitude})"
        )

        return await self.provider.generate_recommendations(request=request)
