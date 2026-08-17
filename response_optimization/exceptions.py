"""
Domain Exceptions for Response Optimization & Resource Allocation
"""

from typing import Any, Dict, Optional
from backend.app.core.exceptions import JeevanGridException


class ResponseOptimizationException(JeevanGridException):
    """Base exception for all response optimization errors."""

    def __init__(
        self,
        message: str = "Emergency response optimization failed.",
        status_code: int = 422,
        error_code: str = "RESPONSE_OPTIMIZATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=status_code,
            error_code=error_code,
            details=details,
        )


# Alias for backward/naming flexibility
ResourceOptimizationException = ResponseOptimizationException


class ResourceUnavailableException(ResponseOptimizationException):
    """Raised when an allocation request targets an unavailable or depleted resource."""

    def __init__(
        self,
        resource_id: str,
        reason: str = "Resource is currently unavailable or assigned to another mission.",
        details: Optional[Dict[str, Any]] = None,
    ):
        message = f"Resource '{resource_id}' cannot be allocated: {reason}"
        super().__init__(
            message=message,
            status_code=409,
            error_code="RESOURCE_UNAVAILABLE",
            details=details or {"resource_id": resource_id, "reason": reason},
        )


class ResourceCapacityExceededException(ResponseOptimizationException):
    """Raised when an allocation attempts to exceed total unit capacity."""

    def __init__(
        self,
        resource_id: str,
        requested: int,
        available: int,
        details: Optional[Dict[str, Any]] = None,
    ):
        message = f"Resource '{resource_id}' capacity exceeded: requested {requested}, available {available}."
        super().__init__(
            message=message,
            status_code=422,
            error_code="CAPACITY_EXCEEDED",
            details=details or {"resource_id": resource_id, "requested": requested, "available": available},
        )


class RoutingProviderException(ResponseOptimizationException):
    """Raised when a routing provider fails to compute transit distance or duration."""

    def __init__(
        self,
        message: str = "Routing provider could not compute path.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=502,
            error_code="ROUTING_PROVIDER_ERROR",
            details=details,
        )


class InvalidIncidentDataException(ResponseOptimizationException):
    """Raised when incident parameters or coordinate data are invalid."""

    def __init__(
        self,
        message: str = "Invalid incident data supplied for response planning.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=422,
            error_code="INVALID_INCIDENT_DATA",
            details=details,
        )
