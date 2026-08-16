"""
Health Check and Readiness Endpoints
"""

from fastapi import APIRouter, status
from backend.app.core.config import settings
from backend.app.db.session import check_db_connectivity
from backend.app.schemas.common import ApiResponse, HealthResponse, HealthServiceStatus

router = APIRouter(tags=["Health & Diagnostics"])


@router.get(
    "/health",
    response_model=ApiResponse[HealthResponse],
    status_code=status.HTTP_200_OK,
    summary="System Health & Readiness Check",
    description="Returns the current operational status of the JeevanGrid backend and configured services.",
)
async def check_health() -> ApiResponse[HealthResponse]:
    """Health check endpoint returning system health, environment metadata, and subsystem readiness."""
    db_connected, db_latency, db_message = await check_db_connectivity()

    db_status = "healthy" if db_connected else "offline"
    overall_status = "healthy" if db_connected else "degraded"

    health_data = HealthResponse(
        status=overall_status,
        app_name=settings.APP_NAME,
        app_version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        simulation_mode=settings.ENABLE_DEMO_SIMULATION_MODE,
        services={
            "api_gateway": HealthServiceStatus(status="healthy", message="FastAPI gateway is operational"),
            "gis_engine": HealthServiceStatus(status="ready", message="Spatial core and coordinate transformers ready"),
            "risk_engine": HealthServiceStatus(status="ready", message="MCDA risk matrix initialized"),
            "optimizer": HealthServiceStatus(status="ready", message="MILP allocation solver engine ready"),
            "database": HealthServiceStatus(
                status=db_status,
                latency_ms=db_latency,
                message=db_message,
            ),
        },
    )
    return ApiResponse(
        success=True,
        message="JeevanGrid backend services health check completed.",
        data=health_data,
    )
