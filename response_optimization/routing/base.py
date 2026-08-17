"""
Abstract Base Class for Routing Providers
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from response_optimization.schemas.routing import RoutingRequest, RoutingResponse


class BaseRoutingProvider(ABC):
    """Abstract interface for disaster transit routing providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the routing provider."""
        pass

    @abstractmethod
    def calculate_route(self, request: RoutingRequest) -> RoutingResponse:
        """Calculates distance, estimated transit time, and route metadata."""
        pass
