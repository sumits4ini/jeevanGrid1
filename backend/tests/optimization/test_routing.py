"""
Unit Tests for Routing Provider and Transit Estimation
"""

from response_optimization.routing.local_provider import LocalRoutingProvider
from response_optimization.schemas.routing import Coordinates, RoutingRequest


def test_local_routing_provider_calculation():
    """Verifies route distance and travel time calculation."""
    provider = LocalRoutingProvider()
    origin = Coordinates(latitude=26.3120, longitude=91.0150)
    dest = Coordinates(latitude=26.3216, longitude=91.0063)

    req = RoutingRequest(
        origin=origin,
        destination=dest,
        vehicle_type="RESCUE_BOAT",
        avoid_hazards=True,
    )
    res = provider.calculate_route(req)

    assert res.straight_line_distance_km > 0.0
    # Route distance must be >= straight line distance
    assert res.estimated_route_distance_km >= res.straight_line_distance_km
    assert res.estimated_duration_minutes >= 2
    assert res.is_estimated is True
    assert "WGS84 Geodesic" in res.provider_info
