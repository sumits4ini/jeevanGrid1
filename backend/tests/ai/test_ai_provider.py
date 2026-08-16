"""
Unit Tests for AI Intelligence Providers
"""

import pytest
from ai_services.providers.factory import get_ai_provider
from ai_services.providers.mock_provider import MockAIProvider
from backend.app.schemas.ai import (
    RecommendationRequest,
    ResourcePrioritizationRequest,
    ResourceUrgencyEnum,
    RiskAnalysisRequest,
    RiskLevelEnum,
)


@pytest.mark.asyncio
async def test_mock_ai_provider_health_check():
    """Verifies AI provider health telemetry."""
    provider = MockAIProvider()
    health = await provider.health_check()
    assert health["status"] == "ready"
    assert health["provider"] == "mock_intelligence"


@pytest.mark.asyncio
async def test_mock_ai_provider_risk_analysis():
    """Verifies risk analysis calculation and categorization."""
    provider = MockAIProvider()
    req = RiskAnalysisRequest(
        disaster_name="Assam Brahmaputra Inundation",
        disaster_type="FLOOD",
        severity_level=5,
        latitude=26.3216,
        longitude=91.0063,
        affected_population_estimate=85000,
        inundation_depth_m=1.8,
    )
    res = await provider.analyze_disaster_risk(req)
    assert res.risk_score >= 0.75
    assert res.risk_level == RiskLevelEnum.CRITICAL
    assert len(res.risk_factors) >= 3
    assert len(res.possible_consequences) > 0
    assert len(res.recommended_actions) > 0
    assert "RESCUE_BOAT" in res.resource_requirements


@pytest.mark.asyncio
async def test_mock_ai_provider_resource_prioritization():
    """Verifies resource ranking based on proximity and vehicle type."""
    provider = MockAIProvider()
    req = ResourcePrioritizationRequest(
        target_latitude=26.3216,
        target_longitude=91.0063,
        disaster_type="FLOOD",
        severity_level=4,
        max_search_radius_km=50.0,
    )
    sample_units = [
        {
            "id": "u1",
            "name": "NDRF Boat Alpha-1",
            "unit_type": "RESCUE_BOAT",
            "unit_code": "BOAT-01",
            "latitude": 26.3240,
            "longitude": 91.0080,
            "status": "AVAILABLE",
        },
        {
            "id": "u2",
            "name": "Ambulance Unit 108",
            "unit_type": "AMBULANCE",
            "unit_code": "AMB-108",
            "latitude": 26.4500,
            "longitude": 91.1500,
            "status": "AVAILABLE",
        },
    ]
    res = await provider.prioritize_resources(req, sample_units)
    assert res.total_units_evaluated == 2
    assert len(res.prioritized_resources) == 2
    # The closer rescue boat must be ranked higher
    assert res.prioritized_resources[0].unit_id == "u1"
    assert res.prioritized_resources[0].priority_rank == 1


@pytest.mark.asyncio
async def test_mock_ai_provider_recommendations():
    """Verifies structured recommendation outputs."""
    provider = MockAIProvider()
    req = RecommendationRequest(
        disaster_type="FLOOD",
        severity_level=4,
        latitude=26.3216,
        longitude=91.0063,
    )
    res = await provider.generate_recommendations(req)
    assert len(res.recommendations) >= 4
    categories = {r.category for r in res.recommendations}
    assert "IMMEDIATE_ACTION" in categories
    assert "RESOURCE_DEPLOYMENT" in categories
    assert res.disclaimer is not None


def test_ai_provider_factory_fallback():
    """Verifies that unknown or unconfigured providers safely fallback to MockAIProvider."""
    provider = get_ai_provider("unknown_provider")
    assert isinstance(provider, MockAIProvider)
