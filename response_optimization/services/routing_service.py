"""
Routing and Transit Time Service
"""

from typing import Optional
from response_optimization.routing.base import BaseRoutingProvider
from response_optimization.routing.factory import get_routing_provider
from response_optimization.schemas.routing import RoutingRequest, RoutingResponse


class RoutingService:
    """Calculates route distances, travel time estimations, and provider failover."""

    def __init__(self, provider: Optional[BaseRoutingProvider] = None):
        self.provider = provider or get_routing_provider()

    def get_route(self, request: RoutingRequest) -> RoutingResponse:
        return self.provider.calculate_route(request)


# Global default instance
routing_service = RoutingService()
