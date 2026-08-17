"""
Resource Suitability Scoring Engine
"""

from typing import Any, Dict, Tuple
from response_optimization.schemas.incident_priority import IncidentItem

# Type match matrix between disaster types and resource assets
DISASTER_RESOURCE_MATCH_MATRIX = {
    "FLOOD": {
        "RESCUE_BOAT": 1.00,
        "NDRF_TEAM": 0.90,
        "AMBULANCE": 0.85,
        "FOOD_WATER_TRUCK": 0.75,
        "MOBILE_GENERATOR": 0.70,
    },
    "CYCLONE": {
        "NDRF_TEAM": 1.00,
        "AMBULANCE": 0.90,
        "RESCUE_BOAT": 0.80,
        "FOOD_WATER_TRUCK": 0.80,
        "MOBILE_GENERATOR": 0.85,
    },
    "EARTHQUAKE": {
        "AMBULANCE": 1.00,
        "NDRF_TEAM": 0.95,
        "FOOD_WATER_TRUCK": 0.80,
        "MOBILE_GENERATOR": 0.80,
        "RESCUE_BOAT": 0.10,
    },
    "LANDSLIDE": {
        "NDRF_TEAM": 1.00,
        "AMBULANCE": 0.90,
        "FOOD_WATER_TRUCK": 0.75,
        "MOBILE_GENERATOR": 0.70,
        "RESCUE_BOAT": 0.10,
    },
}


def calculate_resource_suitability(
    incident: IncidentItem,
    resource: Dict[str, Any],
    distance_km: float,
    max_search_radius_km: float = 50.0,
) -> Tuple[float, str]:
    """
    Computes a deterministic, explainable suitability score (0.0 to 1.0)
    for assigning a resource unit to a specific disaster incident.
    """
    unit_type = str(resource.get("unit_type", "NDRF_TEAM")).upper()
    status = str(resource.get("status", "AVAILABLE")).upper()

    # 1. Type Match Score
    disaster_type = incident.disaster_type.upper()
    type_matches = DISASTER_RESOURCE_MATCH_MATRIX.get(
        disaster_type, DISASTER_RESOURCE_MATCH_MATRIX["FLOOD"]
    )
    match_score = type_matches.get(unit_type, 0.50)

    # 2. Proximity Score (Closer = Higher Score)
    prox_score = max(0.05, 1.0 - (distance_km / max(1.0, max_search_radius_km)))

    # 3. Availability Score
    if status == "AVAILABLE":
        avail_score = 1.00
    elif status in ["STANDBY", "ASSIGNED"]:
        avail_score = 0.50
    else:
        avail_score = 0.00  # Offline / Inactive

    # 4. Urgency Fit (Higher severity demands higher type match)
    urgency_fit = 1.00 if incident.severity_level >= 4 and match_score >= 0.85 else 0.80

    # Composite Suitability Formula (Documented weights)
    # Match: 40%, Proximity: 35%, Availability: 15%, Urgency Fit: 10%
    composite = (
        (0.40 * match_score)
        + (0.35 * prox_score)
        + (0.15 * avail_score)
        + (0.10 * urgency_fit)
    )

    final_score = round(min(1.0, max(0.0, composite)), 2)

    reason = (
        f"{unit_type} suitability {final_score:.2f}: Type relevance for {disaster_type} ({match_score * 100:.0f}%), "
        f"distance {distance_km:.1f}km ({prox_score * 100:.0f}%), status '{status}'."
    )

    return final_score, reason
