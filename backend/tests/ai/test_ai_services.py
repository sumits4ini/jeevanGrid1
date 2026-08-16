"""
Unit Tests for AI Domain Services and GIS Integration
"""

import pytest
from pydantic import ValidationError
from ai_services.services.ai_manager import ai_manager
from backend.app.core.exceptions import AIValidationException
from backend.app.schemas.ai import (
    RecommendationRequest,
    ResourcePrioritizationRequest,
    RiskAnalysisRequest,
)


@pytest.mark.asyncio
async def test_disaster_risk_service_with_gis():
    """Verifies DisasterRiskService executes and queries GIS layers."""
    req = RiskAnalysisRequest(
        disaster_name="Assam Brahmaputra Basin Inundation",
        disaster_type="FLOOD",
        severity_level=4,
        latitude=26.3216,
        longitude=91.0063,
        affected_population_estimate=85400,
        inundation_depth_m=1.25,
    )
    res = await ai_manager.analyze_risk(req)
    assert 0.0 <= res.risk_score <= 1.0
    assert res.risk_level.value in ["LOW", "MODERATE", "HIGH", "CRITICAL"]
    assert len(res.risk_factors) > 0


def test_disaster_risk_service_invalid_coords():
    """Verifies coordinate validation error on invalid latitude."""
    with pytest.raises(ValidationError):
        RiskAnalysisRequest(
            disaster_type="FLOOD",
            severity_level=3,
            latitude=95.0,  # Invalid latitude > 90
            longitude=91.0,
        )


@pytest.mark.asyncio
async def test_resource_prioritization_service_integration():
    """Verifies ResourcePrioritizationService retrieves GIS response fleet and prioritizes."""
    req = ResourcePrioritizationRequest(
        target_latitude=26.3216,
        target_longitude=91.0063,
        disaster_type="FLOOD",
        severity_level=4,
        max_search_radius_km=25.0,
    )
    res = await ai_manager.prioritize_resources(req)
    assert res.total_units_evaluated >= 3
    assert len(res.prioritized_resources) > 0
    assert res.prioritized_resources[0].priority_rank == 1


@pytest.mark.asyncio
async def test_recommendation_service_execution():
    """Verifies RecommendationService produces actionable Incident Command outputs."""
    req = RecommendationRequest(
        disaster_type="FLOOD",
        severity_level=4,
        latitude=26.3216,
        longitude=91.0063,
    )
    res = await ai_manager.generate_recommendations(req)
    assert len(res.recommendations) >= 3
    assert "Incident" in res.disaster_context
