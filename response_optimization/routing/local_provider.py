"""
Deterministic Local Routing Provider with Geodesic & Terrain Speed Modeling
"""

from typing import Optional
from gis_engine.geometry.transforms import calculate_haversine_distance_m
from response_optimization.routing.base import BaseRoutingProvider
from response_optimization.schemas.routing import RoutingRequest, RoutingResponse


class LocalRoutingProvider(BaseRoutingProvider):
    """
    Computes deterministic transit routes and travel time estimates using
    geodesic Haversine equations, urban detour curvature coefficients,
    and vehicle-specific speed models for disaster response environments.
    """

    @property
    def provider_name(self) -> str:
        return "local_geodesic_estimator"

    def calculate_route(self, request: RoutingRequest) -> RoutingResponse:
        # 1. Great-circle distance
        dist_meters = calculate_haversine_distance_m(
            request.origin.longitude,
            request.origin.latitude,
            request.destination.longitude,
            request.destination.latitude,
        )
        straight_km = round(dist_meters / 1000.0, 2)

        # 2. Realistic road/terrain detour factor (1.25x for direct corridors, 1.35x for flooded/urban grids)
        detour_factor = 1.30 if request.avoid_hazards else 1.20
        route_km = round(straight_km * detour_factor, 2)

        # 3. Vehicle speed profiles (km/h under active emergency conditions)
        default_speeds = {
            "RESCUE_BOAT": 18.0,       # Watercraft navigating debris and river currents
            "AMBULANCE": 35.0,         # Emergency road transit with siren priority
            "NDRF_TEAM": 30.0,         # Heavy tactical troop carrier
            "FOOD_WATER_TRUCK": 25.0,  # Logistics supply transport
            "MOBILE_GENERATOR": 20.0,  # Heavy towed generator trailer
        }

        speed_kmh = request.average_speed_kmh or default_speeds.get(
            request.vehicle_type.upper(), 30.0
        )

        # 4. Estimated duration in minutes (+ minimum 2 min staging/departure delay)
        travel_hours = route_km / max(5.0, speed_kmh)
        duration_mins = max(2, int(round(travel_hours * 60.0)) + 2)

        notes = (
            f"Calculated with {detour_factor:.2f}x network detour coefficient at {speed_kmh:.0f} km/h "
            f"({request.vehicle_type}). Straight-line: {straight_km} km."
        )

        return RoutingResponse(
            origin=request.origin,
            destination=request.destination,
            straight_line_distance_km=straight_km,
            estimated_route_distance_km=route_km,
            estimated_duration_minutes=duration_mins,
            is_estimated=True,
            provider_info=f"{self.provider_name} (WGS84 Geodesic / Terrain Modeling)",
            routing_notes=notes,
        )
