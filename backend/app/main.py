"""
JeevanGrid Main FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.endpoints.health import router as health_router
from backend.app.api.v1.router import api_v1_router
from backend.app.core.config import settings
from backend.app.core.handlers import register_exception_handlers
from backend.app.core.logging import logger
from backend.app.schemas.common import ApiResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown routines."""
    logger.info("=" * 70)
    logger.info(f"Starting {settings.APP_NAME} (v{settings.APP_VERSION})")
    logger.info(f"Environment: {settings.APP_ENV} | Debug: {settings.DEBUG}")
    logger.info(f"Simulation Mode: {settings.ENABLE_DEMO_SIMULATION_MODE}")
    logger.info("=" * 70)
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")


def create_application() -> FastAPI:
    """Factory function to configure and initialize the FastAPI app instance."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Next-generation real-world disaster intelligence, spatial risk analytics, "
            "and emergency response optimization platform."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # 1. Register CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Register Centralized Exception Handlers
    register_exception_handlers(app)

    # 3. Mount Health Router at root level (/health)
    app.include_router(health_router)

    # 4. Mount API v1 Router (/api/v1)
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)

    # 5. Root status landing endpoint
    @app.get(
        "/",
        response_model=ApiResponse[dict],
        status_code=status.HTTP_200_OK,
        tags=["Root"],
        summary="API Root Information",
    )
    async def root_info() -> ApiResponse[dict]:
        """Provides high-level system metadata and links to docs and health checks."""
        return ApiResponse(
            success=True,
            message="JeevanGrid API Gateway is online.",
            data={
                "app_name": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "docs_url": "/docs",
                "health_check": "/health",
                "api_v1": settings.API_V1_STR,
            },
        )

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
    )
