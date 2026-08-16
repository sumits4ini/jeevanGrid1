"""
JeevanGrid Custom Exception Hierarchy
Provides typed domain exceptions for consistent API error handling.
"""

from typing import Any, Dict, Optional


class JeevanGridException(Exception):
    """Base exception class for all JeevanGrid domain errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_SERVER_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}


class EntityNotFoundException(JeevanGridException):
    """Raised when a requested resource or entity is not found."""

    def __init__(
        self,
        entity_name: str,
        entity_id: Any,
        details: Optional[Dict[str, Any]] = None,
    ):
        message = f"{entity_name} with ID '{entity_id}' was not found."
        super().__init__(
            message=message,
            status_code=404,
            error_code="ENTITY_NOT_FOUND",
            details=details or {"entity_name": entity_name, "entity_id": str(entity_id)},
        )


class ValidationErrorException(JeevanGridException):
    """Raised when request payload or business logic validation fails."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class SpatialOperationException(JeevanGridException):
    """Raised when a GIS geometry, projection, or spatial query fails."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=400,
            error_code="SPATIAL_OPERATION_ERROR",
            details=details,
        )


class OptimizationException(JeevanGridException):
    """Raised when the MILP solver encounters an infeasible or unbounded state."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=422,
            error_code="OPTIMIZATION_ERROR",
            details=details,
        )


class UnauthorizedException(JeevanGridException):
    """Raised when an action lacks valid authentication credentials."""

    def __init__(
        self,
        message: str = "Could not validate credentials.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=401,
            error_code="UNAUTHORIZED",
            details=details,
        )


class ForbiddenException(JeevanGridException):
    """Raised when an authenticated user lacks required role permissions."""

    def __init__(
        self,
        message: str = "You do not have permission to perform this operational action.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=403,
            error_code="FORBIDDEN",
            details=details,
        )


class AIProviderException(JeevanGridException):
    """Raised when an AI/LLM provider service encounters a network, rate limit, or inference error."""

    def __init__(
        self,
        message: str = "AI intelligence service is temporarily unavailable.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=502,
            error_code="AI_PROVIDER_ERROR",
            details=details,
        )


class AIValidationException(JeevanGridException):
    """Raised when AI input data or generated output fails schema validation."""

    def __init__(
        self,
        message: str = "Invalid input or output structure for AI reasoning pipeline.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=422,
            error_code="AI_VALIDATION_ERROR",
            details=details,
        )
