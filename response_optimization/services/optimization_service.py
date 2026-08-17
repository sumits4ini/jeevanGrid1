"""
Comprehensive Emergency Response Plan Optimization Orchestrator
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from ai_services.services.ai_manager import ai_manager
from backend.app.core.logging import logger
from backend.app.schemas.ai import RecommendationRequest
from gis_engine.services.gis_service import gis_service
from response_optimization.algorithms.allocation import allocate_resources_deterministically
from response_optimization.algorithms.priority import rank_and_prioritize_incidents
from response_optimization.schemas.allocation import ResourceAssignment, ResourceShortage
from response_optimization.schemas.incident_priority import PriorityLevelEnum
from response_optimization.schemas.response_plan import (
    DeploymentOrderItem,
    OperationalWarning,
    ResponsePlanRequest,
    ResponsePlanResponse,
)


class ResponseOptimizationService:
    """
    High-level orchestrator generating deterministic, explainable emergency response
    plans, prioritized dispatch sequences, and operational warning advisories.
    """

    async def generate_response_plan(
        self, request: ResponsePlanRequest
    ) -> ResponsePlanResponse:
        logger.info(
            f"Generating Emergency Response Plan for {len(request.incidents)} incidents. "
            f"Radius: {request.max_search_radius_km}km, AI Advisory: {request.include_ai_advisory}"
        )

        # 1. Incident Prioritization
        prioritized_incidents = rank_and_prioritize_incidents(request.incidents)

        # 2. Retrieve Available Resources (From request or GIS response_units layer)
        available_resources = request.available_resources
        if available_resources is None:
            res_layer = gis_service.registry.get_layer("response_units")
            available_resources = res_layer.get_features() if res_layer else []

        # 3. Execute Capacitated Allocation
        alloc_response = allocate_resources_deterministically(
            incidents=request.incidents,
            available_resources=available_resources,
            max_search_radius_km=request.max_search_radius_km,
            enforce_strict_capacity=True,
        )

        # 4. Generate Ordered Deployment Sequence (Ordered by priority tier, then ETA)
        tier_weights = {
            PriorityLevelEnum.CRITICAL: 1,
            PriorityLevelEnum.HIGH: 2,
            PriorityLevelEnum.MEDIUM: 3,
            PriorityLevelEnum.LOW: 4,
        }

        sorted_assignments = sorted(
            alloc_response.assignments,
            key=lambda a: (tier_weights.get(a.priority_level, 5), a.estimated_travel_time_minutes),
        )

        deployment_sequence: List[DeploymentOrderItem] = []
        for order_idx, asgn in enumerate(sorted_assignments):
            deployment_sequence.append(
                DeploymentOrderItem(
                    deployment_order=order_idx + 1,
                    incident_id=asgn.incident_id,
                    incident_name=asgn.incident_name,
                    priority_level=asgn.priority_level,
                    resource_id=asgn.resource_id,
                    resource_name=asgn.resource_name,
                    resource_type=asgn.resource_type,
                    resource_code=asgn.resource_code,
                    allocated_quantity=asgn.allocated_quantity,
                    estimated_eta_minutes=asgn.estimated_travel_time_minutes,
                    is_eta_estimated=True,
                    staging_point=f"Forward Staging Area ({asgn.distance_km}km from origin)",
                )
            )

        # 5. Generate Operational Warnings & Shortages
        warnings: List[OperationalWarning] = []

        if alloc_response.shortages:
            for s in alloc_response.shortages:
                warnings.append(
                    OperationalWarning(
                        warning_code="RESOURCE_DEFICIT",
                        severity="CRITICAL" if s.urgency == "IMMEDIATE" else "HIGH",
                        title=f"Supply Shortage: {s.resource_type}",
                        message=s.impact_explanation,
                        affected_incident_id=s.incident_id,
                    )
                )

        # Check for isolated critical incidents with 0 assignments
        assigned_inc_ids = {a.incident_id for a in alloc_response.assignments}
        for p_inc in prioritized_incidents:
            if p_inc.priority_level == PriorityLevelEnum.CRITICAL and p_inc.incident_id not in assigned_inc_ids:
                warnings.append(
                    OperationalWarning(
                        warning_code="CRITICAL_INCIDENT_UNSERVICED",
                        severity="CRITICAL",
                        title=f"No Rescue Units Allocated to {p_inc.name}",
                        message="All nearby units exhausted or out of range. Immediate mutual aid escalation required.",
                        affected_incident_id=p_inc.incident_id,
                    )
                )

        # 6. Synthesize Recommended Actions
        recommended_actions: List[str] = [
            f"Deploy {len(deployment_sequence)} authorized rescue units according to priority dispatch order.",
            "Establish forward tactical communications link with lead NDRF rescue craft.",
            "Pre-position ambulances at designated high-elevation patient handover nodes.",
        ]

        if alloc_response.shortages:
            recommended_actions.append(
                f"Transmit mutual aid requisition to State EOC for {len(alloc_response.shortages)} unfulfilled resource requests."
            )

        # 7. AI Recommendation Enrichment if requested
        if request.include_ai_advisory and request.incidents:
            try:
                top_inc = request.incidents[0]
                ai_rec = await ai_manager.generate_recommendations(
                    RecommendationRequest(
                        disaster_type=top_inc.disaster_type,
                        severity_level=top_inc.severity_level,
                        latitude=top_inc.latitude,
                        longitude=top_inc.longitude,
                    )
                )
                if ai_rec and ai_rec.recommendations:
                    for rec in ai_rec.recommendations[:2]:
                        recommended_actions.append(f"[AI Advisory] {rec.title}: {rec.description}")
            except Exception as exc:
                logger.warning(f"AI advisory enrichment note: {exc}")

        plan_summary = {
            "total_incidents": len(request.incidents),
            "critical_incidents_count": sum(1 for i in prioritized_incidents if i.priority_level == PriorityLevelEnum.CRITICAL),
            "total_units_allocated": len(deployment_sequence),
            "total_shortages_count": len(alloc_response.shortages),
            "average_deployment_eta_mins": (
                int(sum(d.estimated_eta_minutes for d in deployment_sequence) / max(1, len(deployment_sequence)))
            ),
        }

        return ResponsePlanResponse(
            plan_id=f"plan-{uuid.uuid4().hex[:8]}",
            generated_at=datetime.now(timezone.utc).isoformat(),
            incident_priorities=prioritized_incidents,
            deployment_sequence=deployment_sequence,
            allocations=alloc_response.assignments,
            unresolved_shortages=alloc_response.shortages,
            operational_warnings=warnings,
            recommended_actions=recommended_actions,
            plan_summary=plan_summary,
        )


# Global default instance
optimization_service = ResponseOptimizationService()
