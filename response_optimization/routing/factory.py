"""
Routing Provider Factory
"""

from typing import Optional
from response_optimization.routing.base import BaseRoutingProvider
from response_optimization.routing.local_provider import LocalRoutingProvider


def get_routing_provider(provider_name: Optional[str] = None) -> BaseRoutingProvider:
    """
    Returns an instance of the configured routing provider.
    Defaults to LocalRoutingProvider.
    """
    # Extensible for future OSRM, GraphHopper, or external routing APIs
    return LocalRoutingProvider()
