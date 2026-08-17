"""
JeevanGrid Emergency Response Optimization & Resource Allocation Core
"""

from response_optimization.algorithms import (
    allocate_resources_deterministically,
    calculate_resource_suitability,
    compute_incident_priority,
    rank_and_prioritize_incidents,
)
from response_optimization.exceptions import (
    InvalidIncidentDataException,
    ResourceCapacityExceededException,
    ResourceOptimizationException,
    ResourceUnavailableException,
    RoutingProviderException,
)
from response_optimization.routing import (
    BaseRoutingProvider,
    LocalRoutingProvider,
    get_routing_provider,
)
from response_optimization.schemas import (
    ContributingFactors,
    Coordinates,
    DeploymentOrderItem,
    IncidentItem,
    IncidentPriorityRequest,
    IncidentPriorityResponse,
    OperationalWarning,
    PrioritizedIncident,
    PriorityLevelEnum,
    ResourceAllocationRequest,
    ResourceAllocationResponse,
    ResourceAssignment,
    ResourceRequirement,
    ResourceShortage,
    ResponsePlanRequest,
    ResponsePlanResponse,
    RoutingRequest,
    RoutingResponse,
)
from response_optimization.services import (
    ResourceAllocationService,
    ResponseOptimizationService,
    RoutingService,
    ScoringService,
    allocation_service,
    optimization_service,
    routing_service,
    scoring_service,
)

__version__ = "0.1.0"

__all__ = [
    "PriorityLevelEnum",
    "ContributingFactors",
    "IncidentItem",
    "PrioritizedIncident",
    "IncidentPriorityRequest",
    "IncidentPriorityResponse",
    "Coordinates",
    "RoutingRequest",
    "RoutingResponse",
    "ResourceRequirement",
    "ResourceAssignment",
    "ResourceShortage",
    "ResourceAllocationRequest",
    "ResourceAllocationResponse",
    "OperationalWarning",
    "DeploymentOrderItem",
    "ResponsePlanRequest",
    "ResponsePlanResponse",
    "BaseRoutingProvider",
    "LocalRoutingProvider",
    "get_routing_provider",
    "compute_incident_priority",
    "rank_and_prioritize_incidents",
    "calculate_resource_suitability",
    "allocate_resources_deterministically",
    "ScoringService",
    "scoring_service",
    "RoutingService",
    "routing_service",
    "ResourceAllocationService",
    "allocation_service",
    "ResponseOptimizationService",
    "optimization_service",
    "ResourceOptimizationException",
    "ResourceUnavailableException",
    "ResourceCapacityExceededException",
    "RoutingProviderException",
    "InvalidIncidentDataException",
]
