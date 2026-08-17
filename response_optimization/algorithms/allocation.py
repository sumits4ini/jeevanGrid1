"""
Deterministic Capacitated Resource Allocation Engine
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid

from gis_engine.geometry.transforms import calculate_haversine_distance_m
from response_optimization.algorithms.priority import rank_and_prioritize_incidents
from response_optimization.algorithms.suitability import calculate_resource_suitability
from response_optimization.routing.local_provider import LocalRoutingProvider
from response_optimization.schemas.allocation import (
    ResourceAllocationResponse,
    ResourceAssignment,
    ResourceShortage,
)
from response_optimization.schemas.incident_priority import IncidentItem, PriorityLevelEnum
from response_optimization.schemas.routing import Coordinates, RoutingRequest

# Demand quotas based on severity level and disaster type
DEMAND_QUOTA_MATRIX = {
    "FLOOD": {
        5: {"RESCUE_BOAT": 4, "NDRF_TEAM": 2, "AMBULANCE": 2, "FOOD_WATER_TRUCK": 2},
        4: {"RESCUE_BOAT": 2, "NDRF_TEAM": 2, "AMBULANCE": 2, "FOOD_WATER_TRUCK": 1},
        3: {"RESCUE_BOAT": 2, "NDRF_TEAM": 1, "AMBULANCE": 1, "FOOD_WATER_TRUCK": 1},
        2: {"RESCUE_BOAT": 1, "AMBULANCE": 1},
        1: {"AMBULANCE": 1},
    },
    "CYCLONE": {
        5: {"NDRF_TEAM": 3, "AMBULANCE": 3, "FOOD_WATER_TRUCK": 2, "RESCUE_BOAT": 2},
        4: {"NDRF_TEAM": 2, "AMBULANCE": 2, "FOOD_WATER_TRUCK": 2, "RESCUE_BOAT": 1},
        3: {"NDRF_TEAM": 2, "AMBULANCE": 1, "FOOD_WATER_TRUCK": 1},
        2: {"NDRF_TEAM": 1, "AMBULANCE": 1},
        1: {"AMBULANCE": 1},
    },
    "EARTHQUAKE": {
        5: {"NDRF_TEAM": 4, "AMBULANCE": 4, "FOOD_WATER_TRUCK": 3, "MOBILE_GENERATOR": 2},
        4: {"NDRF_TEAM": 3, "AMBULANCE": 3, "FOOD_WATER_TRUCK": 2, "MOBILE_GENERATOR": 1},
        3: {"NDRF_TEAM": 2, "AMBULANCE": 2, "FOOD_WATER_TRUCK": 1},
        2: {"NDRF_TEAM": 1, "AMBULANCE": 1},
        1: {"AMBULANCE": 1},
    },
}


def allocate_resources_deterministically(
    incidents: List[IncidentItem],
    available_resources: List[Dict[str, Any]],
    max_search_radius_km: float = 50.0,
    enforce_strict_capacity: bool = True,
) -> ResourceAllocationResponse:
    """
    Executes a deterministic, explainable greedy-capacitated resource allocation
    across prioritized incidents while tracking allocations, constraints, and shortages.
    """
    # 1. Rank incidents by MCDA priority score
    prioritized_incidents = rank_and_prioritize_incidents(incidents)

    # 2. Track allocated resource unit IDs to prevent double-allocation
    allocated_resource_ids: Set[str] = set()
    assignments: List[ResourceAssignment] = []
    shortages: List[ResourceShortage] = []

    routing_engine = LocalRoutingProvider()

    for p_inc in prioritized_incidents:
        # Find original incident object
        inc = next((i for i in incidents if i.id == p_inc.incident_id), None)
        if not inc:
            continue

        disaster_key = inc.disaster_type.upper()
        type_quotas = DEMAND_QUOTA_MATRIX.get(disaster_key, DEMAND_QUOTA_MATRIX["FLOOD"])
        demand = type_quotas.get(inc.severity_level, type_quotas.get(3, {"NDRF_TEAM": 1, "AMBULANCE": 1}))

        # For each required resource type, select best suited available units
        for req_type, qty_needed in demand.items():
            qty_allocated = 0

            # Filter candidate units that match type and are not yet allocated
            candidates: List[Tuple[float, Dict[str, Any], float, int]] = []

            for res in available_resources:
                res_id = str(res.get("id", ""))
                res_type = str(res.get("unit_type", "")).upper()
                res_status = str(res.get("status", "AVAILABLE")).upper()

                if enforce_strict_capacity and res_id in allocated_resource_ids:
                    continue
                if res_status not in ["AVAILABLE", "STANDBY"]:
                    continue
                if res_type != req_type:
                    continue

                r_lat = float(res.get("latitude", inc.latitude))
                r_lng = float(res.get("longitude", inc.longitude))

                dist_m = calculate_haversine_distance_m(inc.longitude, inc.latitude, r_lng, r_lat)
                dist_km = round(dist_m / 1000.0, 2)

                if dist_km > max_search_radius_km:
                    continue

                # Compute suitability
                suit_score, _ = calculate_resource_suitability(
                    incident=inc,
                    resource=res,
                    distance_km=dist_km,
                    max_search_radius_km=max_search_radius_km,
                )

                # Compute estimated travel time via routing
                route_res = routing_engine.calculate_route(
                    RoutingRequest(
                        origin=Coordinates(latitude=r_lat, longitude=r_lng),
                        destination=Coordinates(latitude=inc.latitude, longitude=inc.longitude),
                        vehicle_type=res_type,
                    )
                )

                candidates.append((suit_score, res, dist_km, route_res.estimated_duration_minutes))

            # Sort candidates by suitability score descending
            candidates.sort(key=lambda item: item[0], reverse=True)

            # Allocate up to qty_needed
            for suit_score, res, dist_km, eta_mins in candidates:
                if qty_allocated >= qty_needed:
                    break

                res_id = str(res.get("id", ""))
                res_name = str(res.get("name", f"Unit {res_id}"))
                res_code = str(res.get("unit_code", res_id))

                allocated_resource_ids.add(res_id)
                qty_allocated += 1

                task = f"Deploy to {inc.name} ({inc.latitude:.3f}°, {inc.longitude:.3f}°) for life-saving operations."
                reason = (
                    f"Assigned to {p_inc.priority_level.value} incident '{inc.name}'. "
                    f"Distance: {dist_km}km, ETA: ~{eta_mins} mins, Suitability: {suit_score:.2f}."
                )

                assignments.append(
                    ResourceAssignment(
                        assignment_id=f"asgn-{uuid.uuid4().hex[:8]}",
                        incident_id=inc.id,
                        incident_name=inc.name,
                        resource_id=res_id,
                        resource_name=res_name,
                        resource_type=req_type,
                        resource_code=res_code,
                        allocated_quantity=1,
                        priority_level=p_inc.priority_level,
                        distance_km=dist_km,
                        estimated_travel_time_minutes=eta_mins,
                        is_travel_time_estimated=True,
                        suitability_score=suit_score,
                        reason=reason,
                        task_assignment=task,
                    )
                )

            # Check if there is unmet demand (shortage)
            if qty_allocated < qty_needed:
                shortage_qty = qty_needed - qty_allocated
                shortages.append(
                    ResourceShortage(
                        incident_id=inc.id,
                        incident_name=inc.name,
                        resource_type=req_type,
                        quantity_demanded=qty_needed,
                        quantity_allocated=qty_allocated,
                        shortage_count=shortage_qty,
                        urgency="IMMEDIATE" if p_inc.priority_level == PriorityLevelEnum.CRITICAL else "HIGH",
                        impact_explanation=(
                            f"Deficit of {shortage_qty} {req_type}(s) at {inc.name}. "
                            f"All {len(allocated_resource_ids)} depot assets within {max_search_radius_km}km are committed."
                        ),
                        recommended_mitigation=(
                            f"Request inter-district mutual aid or mobilize NDRF state reserve battalions for {req_type}."
                        ),
                    )
                )

    allocation_summary = {
        "total_incidents_processed": len(incidents),
        "total_resources_evaluated": len(available_resources),
        "total_resources_assigned": len(assignments),
        "total_shortages_identified": len(shortages),
        "unmet_demand_count": sum(s.shortage_count for s in shortages),
    }

    return ResourceAllocationResponse(
        allocation_id=f"alloc-{uuid.uuid4().hex[:8]}",
        total_assignments=len(assignments),
        total_shortages=len(shortages),
        assignments=assignments,
        shortages=shortages,
        allocation_summary=allocation_summary,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
