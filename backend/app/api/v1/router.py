"""
API Version 1 Central Router Aggregator
Combines all v1 endpoint routers into a unified APIRouter instance.
"""

from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    ai,
    disasters,
    gis,
    health,
    locations,
    optimization,
    resources,
    risk,
)

api_v1_router = APIRouter()

# Include all modular sub-routers
api_v1_router.include_router(health.router)
api_v1_router.include_router(disasters.router)
api_v1_router.include_router(locations.router)
api_v1_router.include_router(resources.router)
api_v1_router.include_router(risk.router)
api_v1_router.include_router(gis.router)
api_v1_router.include_router(ai.router)
api_v1_router.include_router(optimization.router)
