"""
Common Pydantic Schemas for Standardized API Envelopes
"""

from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common model configurations."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class ApiResponse(BaseSchema, Generic[T]):
    """Standard unified response wrapper for all API endpoints."""

    success: bool = True
    message: str = "Operation completed successfully."
    data: Optional[T] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ErrorResponse(BaseSchema):
    """Standard unified error response structure."""

    success: bool = False
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthServiceStatus(BaseSchema):
    """Individual service readiness status."""

    status: str = "healthy"
    latency_ms: Optional[float] = None
    message: Optional[str] = None


class HealthResponse(BaseSchema):
    """Comprehensive system health and readiness status."""

    status: str = "healthy"
    app_name: str
    app_version: str
    environment: str
    simulation_mode: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    services: Dict[str, HealthServiceStatus] = Field(default_factory=dict)


class PaginationMeta(BaseSchema):
    """Pagination metadata for list endpoints."""

    total_count: int
    page: int
    page_size: int
    total_pages: int


class PaginatedResponse(ApiResponse[List[T]], Generic[T]):
    """Paginated API response container."""

    pagination: Optional[PaginationMeta] = None
