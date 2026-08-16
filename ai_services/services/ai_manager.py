"""
Central AI Intelligence Service Coordinator
"""

from typing import Any, Dict, Optional
from backend.app.schemas.ai import (
    RecommendationRequest,
    RecommendationResponse,
    ResourcePrioritizationRequest,
    ResourcePrioritizationResponse,
    RiskAnalysisRequest,
    RiskAnalysisResponse,
)
from ai_services.providers.base import BaseAIProvider
from ai_services.providers.factory import get_ai_provider
from ai_services.services.recommendation_service import RecommendationService
from ai_services.services.resource_service import ResourcePrioritizationService
from ai_services.services.risk_service import DisasterRiskService


class AIServiceManager:
    """Central manager providing unified access to all AI decision support capabilities."""

    def __init__(self, provider: Optional[BaseAIProvider] = None):
        self.provider = provider or get_ai_provider()
        self.risk_service = DisasterRiskService(self.provider)
        self.resource_service = ResourcePrioritizationService(self.provider)
        self.recommendation_service = RecommendationService(self.provider)

    async def analyze_risk(self, request: RiskAnalysisRequest) -> RiskAnalysisResponse:
        return await self.risk_service.analyze_risk(request)

    async def prioritize_resources(
        self, request: ResourcePrioritizationRequest
    ) -> ResourcePrioritizationResponse:
        return await self.resource_service.prioritize_resources(request)

    async def generate_recommendations(
        self, request: RecommendationRequest
    ) -> RecommendationResponse:
        return await self.recommendation_service.generate_recommendations(request)

    async def health_check(self) -> Dict[str, Any]:
        return await self.provider.health_check()


# Global default AI Service instance
ai_manager = AIServiceManager()
