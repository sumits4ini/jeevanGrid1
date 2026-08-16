"""
API Version 1 Central Router Aggregator
Combines all v1 endpoint routers into a unified APIRouter instance.
"""

from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    disasters,
    gis,
    health,
    locations,
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
