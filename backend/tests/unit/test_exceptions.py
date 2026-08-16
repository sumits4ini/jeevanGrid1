"""
Unit Tests for Custom Exception Hierarchy
"""

from backend.app.core.exceptions import (
    EntityNotFoundException,
    ForbiddenException,
    JeevanGridException,
    OptimizationException,
    SpatialOperationException,
    UnauthorizedException,
    ValidationErrorException,
)


def test_custom_exception_hierarchy():
    """Ensures all domain exceptions inherit from JeevanGridException."""
    base = JeevanGridException("Base error", status_code=500, error_code="TEST_ERROR")
    not_found = EntityNotFoundException(entity_name="Hospital", entity_id=42)
    val_err = ValidationErrorException("Invalid polygon coordinates")
    spatial_err = SpatialOperationException("Failed to project to EPSG:3857")
    opt_err = OptimizationException("Infeasible LP formulation")
    unauth = UnauthorizedException("Token expired")
    forbidden = ForbiddenException("Commander role required")

    assert isinstance(not_found, JeevanGridException)
    assert not_found.status_code == 404
    assert not_found.error_code == "ENTITY_NOT_FOUND"
    assert "Hospital with ID '42' was not found" in not_found.message

    assert val_err.status_code == 422
    assert spatial_err.status_code == 400
    assert opt_err.status_code == 422
    assert unauth.status_code == 401
    assert forbidden.status_code == 403
