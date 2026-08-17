"""
Scoring and Prioritization Service
"""

from typing import Any, Dict, List, Optional
from response_optimization.algorithms.priority import rank_and_prioritize_incidents
from response_optimization.algorithms.suitability import calculate_resource_suitability
from response_optimization.schemas.incident_priority import (
    IncidentItem,
    IncidentPriorityRequest,
    IncidentPriorityResponse,
)


class ScoringService:
    """Provides incident priority ranking and resource suitability scoring."""

    def prioritize_incidents(
        self, request: IncidentPriorityRequest
    ) -> IncidentPriorityResponse:
        from datetime import datetime, timezone

        prioritized = rank_and_prioritize_incidents(
            incidents=request.incidents,
            custom_weights=request.custom_weights,
        )
        return IncidentPriorityResponse(
            total_incidents=len(prioritized),
            prioritized_incidents=prioritized,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    def evaluate_suitability(
        self,
        incident: IncidentItem,
        resource: Dict[str, Any],
        distance_km: float,
        max_search_radius_km: float = 50.0,
    ) -> Dict[str, Any]:
        score, reason = calculate_resource_suitability(
            incident=incident,
            resource=resource,
            distance_km=distance_km,
            max_search_radius_km=max_search_radius_km,
        )
        return {"suitability_score": score, "reason": reason}


# Global default instance
scoring_service = ScoringService()
