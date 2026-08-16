"""
JeevanGrid Centralized Exception Handlers
Transforms application exceptions into standardized JSON ErrorResponse objects.
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.core.config import settings
from backend.app.core.exceptions import JeevanGridException
from backend.app.core.logging import logger
from backend.app.schemas.common import ErrorResponse


async def jeevangrid_exception_handler(request: Request, exc: JeevanGridException) -> JSONResponse:
    """Handles domain-specific JeevanGrid exceptions."""
    logger.warning(
        f"Domain exception on {request.method} {request.url.path}: [{exc.error_code}] {exc.message}"
    )
    error_payload = ErrorResponse(
        success=False,
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload.model_dump(mode="json"),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handles FastAPI Pydantic request validation errors."""
    logger.info(f"Validation error on {request.method} {request.url.path}: {exc.errors()}")
    error_payload = ErrorResponse(
        success=False,
        error_code="UNPROCESSABLE_ENTITY",
        message="Request validation failed. Please check your payload parameters.",
        details={"errors": exc.errors()},
    )
    return JSONResponse(
        status_code=422,
        content=error_payload.model_dump(mode="json"),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handles standard Starlette / FastAPI HTTPExceptions."""
    logger.info(f"HTTP {exc.status_code} on {request.method} {request.url.path}: {exc.detail}")
    error_payload = ErrorResponse(
        success=False,
        error_code=f"HTTP_{exc.status_code}",
        message=str(exc.detail),
        details={},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload.model_dump(mode="json"),
    )


async def global_unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected internal exceptions."""
    logger.error(
        f"Unhandled server error on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True,
    )
    message = str(exc) if settings.DEBUG else "An unexpected internal server error occurred."
    error_payload = ErrorResponse(
        success=False,
        error_code="INTERNAL_SERVER_ERROR",
        message=message,
        details={"path": request.url.path} if settings.DEBUG else {},
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_payload.model_dump(mode="json"),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registers all exception handlers with the FastAPI application instance."""
    app.add_exception_handler(JeevanGridException, jeevangrid_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, global_unhandled_exception_handler)
