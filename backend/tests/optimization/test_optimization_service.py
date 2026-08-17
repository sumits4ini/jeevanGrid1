"""
Unit Tests for Response Optimization Service and Plan Generation
"""

import pytest
from response_optimization.schemas.incident_priority import IncidentItem
from response_optimization.schemas.response_plan import ResponsePlanRequest
from response_optimization.services.optimization_service import optimization_service


@pytest.mark.asyncio
async def test_generate_response_plan_full_workflow():
    """Verifies end-to-end response plan generation with prioritized sequence and warnings."""
    request = ResponsePlanRequest(
        incidents=[
            IncidentItem(
                id="inc-barpeta-01",
                name="Barpeta Flash Flood",
                disaster_type="FLOOD",
                severity_level=4,
                latitude=26.3216,
                longitude=91.0063,
                affected_population=85400,
                inundation_depth_m=1.25,
            ),
            IncidentItem(
                id="inc-chennai-02",
                name="Chennai Coastal Storm Surge",
                disaster_type="CYCLONE",
                severity_level=3,
                latitude=13.0827,
                longitude=80.2707,
                affected_population=32000,
            ),
        ],
        max_search_radius_km=50.0,
        include_ai_advisory=True,
    )

    plan = await optimization_service.generate_response_plan(request)
    assert plan.plan_id.startswith("plan-")
    assert len(plan.incident_priorities) == 2
    assert len(plan.deployment_sequence) > 0
    # Deployment sequence must have 1-indexed orders (1, 2, 3...)
    orders = [d.deployment_order for d in plan.deployment_sequence]
    assert orders == list(range(1, len(plan.deployment_sequence) + 1))
    assert len(plan.recommended_actions) >= 2
    assert plan.disclaimer is not None
