"""
Multi-Criteria Incident Prioritization Algorithm
"""

import math
from typing import Dict, List, Optional
from response_optimization.schemas.incident_priority import (
    ContributingFactors,
    IncidentItem,
    PrioritizedIncident,
    PriorityLevelEnum,
)

DEFAULT_FACTOR_WEIGHTS = {
    "severity": 0.25,
    "risk": 0.25,
    "population": 0.20,
    "geographic": 0.15,
    "urgency": 0.10,
    "shortage": 0.05,
}


def compute_incident_priority(
    incident: IncidentItem,
    custom_weights: Optional[Dict[str, float]] = None,
) -> PrioritizedIncident:
    """
    Computes a deterministic, explainable priority score (0.0 to 1.0) and tier
    for an emergency incident using Multi-Criteria Decision Analysis (MCDA).
    """
    weights = DEFAULT_FACTOR_WEIGHTS.copy()
    if custom_weights:
        total_w = sum(custom_weights.values())
        if total_w > 0:
            weights = {k: v / total_w for k, v in custom_weights.items()}

    # 1. Severity Score (1-5 normalized to 0.2 - 1.0)
    sev_score = min(1.0, max(0.1, incident.severity_level / 5.0))

    # 2. Risk Score (Use explicit risk_score or fallback to severity heuristic)
    if incident.risk_score is not None:
        risk_score = min(1.0, max(0.0, incident.risk_score))
    else:
        risk_score = sev_score

    # 3. Population Impact Score (Logarithmic scaling)
    pop = incident.affected_population or 0
    pop_score = min(1.0, math.log10(max(10, pop)) / 6.0)

    # 4. Geographic Inundation / Area Impact Score
    depth = incident.inundation_depth_m or 0.0
    geo_score = min(1.0, depth / 2.5) if incident.disaster_type.upper() == "FLOOD" else sev_score * 0.8

    # 5. Urgency Score (High severity or high-risk incidents demand faster response)
    urgency_score = 0.95 if incident.severity_level >= 4 else (0.70 if incident.severity_level >= 3 else 0.40)

    # 6. Resource Shortage Vulnerability Score
    shortage_score = 0.85 if incident.severity_level >= 4 else 0.50

    # Composite Normalized Score
    raw_composite = (
        (weights.get("severity", 0.25) * sev_score)
        + (weights.get("risk", 0.25) * risk_score)
        + (weights.get("population", 0.20) * pop_score)
        + (weights.get("geographic", 0.15) * geo_score)
        + (weights.get("urgency", 0.10) * urgency_score)
        + (weights.get("shortage", 0.05) * shortage_score)
    )
    final_score = round(min(1.0, max(0.05, raw_composite)), 2)

    # Classify Priority Tier
    if final_score >= 0.75:
        level = PriorityLevelEnum.CRITICAL
        exp = f"Critical multi-factor emergency: Level {incident.severity_level} {incident.disaster_type} with {pop:,} residents exposed."
    elif final_score >= 0.50:
        level = PriorityLevelEnum.HIGH
        exp = f"High priority incident requiring immediate tactical resource mobilization."
    elif final_score >= 0.25:
        level = PriorityLevelEnum.MEDIUM
        exp = f"Moderate severity incident with localized impact requiring standard response fleet."
    else:
        level = PriorityLevelEnum.LOW
        exp = f"Low severity alert currently under active monitoring."

    factors = ContributingFactors(
        severity_score=round(sev_score, 2),
        risk_score=round(risk_score, 2),
        urgency_score=round(urgency_score, 2),
        population_impact_score=round(pop_score, 2),
        geographic_impact_score=round(geo_score, 2),
        resource_shortage_score=round(shortage_score, 2),
    )

    return PrioritizedIncident(
        incident_id=incident.id,
        name=incident.name,
        disaster_type=incident.disaster_type,
        priority_rank=1,  # Ranked in batch function
        priority_score=final_score,
        priority_level=level,
        contributing_factors=factors,
        explanation=exp,
    )


def rank_and_prioritize_incidents(
    incidents: List[IncidentItem],
    custom_weights: Optional[Dict[str, float]] = None,
) -> List[PrioritizedIncident]:
    """
    Ranks a list of incidents in descending order of priority score.
    """
    scored = [compute_incident_priority(inc, custom_weights) for inc in incidents]
    # Sort descending by priority score
    scored.sort(key=lambda item: item.priority_score, reverse=True)

    for idx, item in enumerate(scored):
        item.priority_rank = idx + 1

    return scored
