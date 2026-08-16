"""
Abstract Base Class for AI/LLM Intelligence Providers
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from backend.app.schemas.ai import (
    RecommendationRequest,
    RecommendationResponse,
    ResourcePrioritizationRequest,
    ResourcePrioritizationResponse,
    RiskAnalysisRequest,
    RiskAnalysisResponse,
)


class BaseAIProvider(ABC):
    """Abstract interface for AI/LLM reasoning and decision support providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique identifier for the AI provider (e.g. 'mock', 'gemini', 'openai')."""
        pass

    @abstractmethod
    async def analyze_disaster_risk(self, request: RiskAnalysisRequest) -> RiskAnalysisResponse:
        """Generates structured disaster risk intelligence, factors, and consequences."""
        pass

    @abstractmethod
    async def prioritize_resources(
        self,
        request: ResourcePrioritizationRequest,
        available_units: List[Dict[str, Any]],
    ) -> ResourcePrioritizationResponse:
        """Computes intelligent urgency scores and optimal allocation ranks for rescue units."""
        pass

    @abstractmethod
    async def generate_recommendations(
        self,
        request: RecommendationRequest,
        context_data: Optional[Dict[str, Any]] = None,
    ) -> RecommendationResponse:
        """Produces categorized, actionable operational recommendations for Incident Command."""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Returns provider availability and operational readiness status."""
        pass
