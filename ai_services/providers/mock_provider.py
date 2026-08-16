"""
Deterministic Rule-Informed AI Intelligence Provider
"""

from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional
import uuid

from backend.app.schemas.ai import (
    ActionCategoryEnum,
    RecommendationItem,
    RecommendationRequest,
    RecommendationResponse,
    ResourcePrioritizationRequest,
    ResourcePrioritizationResponse,
    ResourcePriorityItem,
    ResourceUrgencyEnum,
    RiskAnalysisRequest,
    RiskAnalysisResponse,
    RiskFactor,
    RiskLevelEnum,
)
from gis_engine.geometry.transforms import calculate_haversine_distance_m


class MockAIProvider:
    """
    Intelligent deterministic AI provider.
    Implements NDMA / UNDRR disaster management heuristics, risk formulation,
    and GIS-informed spatial reasoning without external API dependencies.
    """

    @property
    def provider_name(self) -> str:
        return "mock_intelligence"

    async def health_check(self) -> Dict[str, Any]:
        return {
            "provider": self.provider_name,
            "status": "ready",
            "mode": "deterministic_expert_system",
            "latency_ms": 1.2,
        }

    async def analyze_disaster_risk(self, request: RiskAnalysisRequest) -> RiskAnalysisResponse:
        """Computes comprehensive multi-factor disaster risk scores."""
        # 1. Base intensity from severity level (1-5 -> 0.2 to 1.0)
        base_intensity = min(1.0, max(0.1, request.severity_level / 5.0))

        # 2. Inundation depth weight
        depth_factor = min(1.0, (request.inundation_depth_m or 0.0) / 2.5)

        # 3. Population exposure factor
        pop_count = request.affected_population_estimate or 0
        pop_factor = min(1.0, math.log10(max(10, pop_count)) / 6.0)

        # 4. Composite Risk Score calculation (weighted average)
        composite_score = round(
            (0.40 * base_intensity) + (0.35 * depth_factor) + (0.25 * pop_factor),
            2,
        )

        # Classify Risk Level
        if composite_score >= 0.75:
            risk_level = RiskLevelEnum.CRITICAL
            priority = "CRITICAL / DEFCON 1"
        elif composite_score >= 0.50:
            risk_level = RiskLevelEnum.HIGH
            priority = "HIGH / DEFCON 2"
        elif composite_score >= 0.25:
            risk_level = RiskLevelEnum.MODERATE
            priority = "ELEVATED / DEFCON 3"
        else:
            risk_level = RiskLevelEnum.LOW
            priority = "STANDARD / DEFCON 4"

        # Construct specific risk factors
        risk_factors: List[RiskFactor] = [
            RiskFactor(
                category="Hydrological",
                factor_name="Surface Water Inundation Depth",
                severity_score=round(depth_factor, 2),
                description=f"Inundation depth recorded at {request.inundation_depth_m}m in low-lying sector.",
                mitigation_hint="Deploy motorized shallow-draft rescue craft.",
            ),
            RiskFactor(
                category="Demographic",
                factor_name="Vulnerable Population Exposure",
                severity_score=round(pop_factor, 2),
                description=f"Estimated {pop_count:,} residents residing within the immediate hazard perimeter.",
                mitigation_hint="Issue ward-level automated evacuation advisories.",
            ),
            RiskFactor(
                category="Infrastructure",
                factor_name="Transportation Corridor Severance",
                severity_score=round(base_intensity * 0.9, 2),
                description="Key bridge links and low-elevation arterial roads compromised by flood surge.",
                mitigation_hint="Reroute ambulances via secondary elevated bypass roads.",
            ),
            RiskFactor(
                category="Meteorological",
                factor_name="Precipitation Intensity",
                severity_score=0.82 if request.severity_level >= 4 else 0.45,
                description="Heavy upstream catchment basin rainfall sustaining river overflow levels.",
                mitigation_hint="Monitor IMD radar feeds for 3-hour precipitation projections.",
            ),
        ]

        possible_consequences = [
            "Complete physical isolation of low-lying wards without boat access.",
            "Potential secondary grid failure at vulnerable distribution substations.",
            "Water contamination and municipal drinking water supply disruption.",
            "Overcrowding and medical supply depletion at nearby civil hospitals.",
        ]

        recommended_actions = [
            "Establish forward Incident Command Post (ICP) on high-elevation terrain.",
            "Mobilize 6 NDRF boat teams for urgent residential evacuations.",
            "Deploy mobile emergency generator to Barpeta Civil Hospital.",
            "Coordinate with district logistics for emergency food and clean water distribution.",
        ]

        resource_requirements = {
            "RESCUE_BOAT": 8 if request.severity_level >= 4 else 4,
            "AMBULANCE": 6 if request.severity_level >= 4 else 2,
            "NDRF_TEAM": 4 if request.severity_level >= 4 else 2,
            "FOOD_WATER_TRUCK": 3,
            "MOBILE_GENERATOR": 2,
        }

        affected_area_summary = (
            f"{request.disaster_name} ({request.disaster_type}) centered at "
            f"({request.latitude:.4f}°, {request.longitude:.4f}°). "
            f"Composite risk evaluated at {composite_score:.2f} ({risk_level.value}) "
            f"with {pop_count:,} exposed residents."
        )

        return RiskAnalysisResponse(
            analysis_id=f"risk-ai-{uuid.uuid4().hex[:8]}",
            disaster_name=request.disaster_name or "Incident",
            risk_score=composite_score,
            risk_level=risk_level,
            confidence_score=0.94,
            priority_level=priority,
            affected_area_summary=affected_area_summary,
            risk_factors=risk_factors,
            possible_consequences=possible_consequences,
            recommended_actions=recommended_actions,
            resource_requirements=resource_requirements,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    async def prioritize_resources(
        self,
        request: ResourcePrioritizationRequest,
        available_units: List[Dict[str, Any]],
    ) -> ResourcePrioritizationResponse:
        """Ranks rescue assets by distance, type compatibility, and urgency."""
        prioritized_items: List[ResourcePriorityItem] = []

        # Type relevance weighting based on disaster type
        type_weights = {
            "FLOOD": {"RESCUE_BOAT": 1.0, "NDRF_TEAM": 0.9, "AMBULANCE": 0.85, "FOOD_WATER_TRUCK": 0.7},
            "CYCLONE": {"NDRF_TEAM": 1.0, "AMBULANCE": 0.9, "RESCUE_BOAT": 0.8, "FOOD_WATER_TRUCK": 0.75},
            "EARTHQUAKE": {"AMBULANCE": 1.0, "NDRF_TEAM": 0.95, "FOOD_WATER_TRUCK": 0.8, "RESCUE_BOAT": 0.2},
            "LANDSLIDE": {"NDRF_TEAM": 1.0, "AMBULANCE": 0.9, "FOOD_WATER_TRUCK": 0.7, "RESCUE_BOAT": 0.1},
        }
        weights_for_disaster = type_weights.get(request.disaster_type.upper(), type_weights["FLOOD"])

        for unit in available_units:
            unit_id = str(unit.get("id", ""))
            unit_name = str(unit.get("name", "Unit"))
            unit_type = str(unit.get("unit_type", "NDRF_TEAM"))
            unit_code = str(unit.get("unit_code", unit_id))
            status = str(unit.get("status", "AVAILABLE"))

            u_lat = float(unit.get("latitude", request.target_latitude))
            u_lng = float(unit.get("longitude", request.target_longitude))

            # Calculate geodesic distance in km
            dist_m = calculate_haversine_distance_m(
                request.target_longitude, request.target_latitude, u_lng, u_lat
            )
            dist_km = round(dist_m / 1000.0, 2)

            if dist_km > request.max_search_radius_km:
                continue

            # Compute priority score:
            # - Distance penalty (closer = higher score)
            dist_score = max(0.1, 1.0 - (dist_km / request.max_search_radius_km))
            # - Type match multiplier
            type_score = weights_for_disaster.get(unit_type, 0.5)
            # - Availability boost
            avail_score = 1.0 if status == "AVAILABLE" else 0.4

            raw_score = (0.45 * dist_score) + (0.35 * type_score) + (0.20 * avail_score)
            priority_score = round(min(1.0, max(0.05, raw_score)), 2)

            # Assign Urgency Tier
            if priority_score >= 0.80:
                urgency = ResourceUrgencyEnum.IMMEDIATE
            elif priority_score >= 0.60:
                urgency = ResourceUrgencyEnum.URGENT
            elif priority_score >= 0.40:
                urgency = ResourceUrgencyEnum.STANDARD
            else:
                urgency = ResourceUrgencyEnum.STANDBY

            # Estimated transit minutes (assuming 35 km/h urban disaster transit speed)
            transit_minutes = max(3, int((dist_km / 35.0) * 60))

            reason = f"{unit_type} located {dist_km}km away. Status: {status}. High tactical relevance for {request.disaster_type}."
            task = f"Deploy to Sector ({request.target_latitude:.3f}°, {request.target_longitude:.3f}°) for life-rescue."

            prioritized_items.append(
                ResourcePriorityItem(
                    unit_id=unit_id,
                    unit_name=unit_name,
                    unit_type=unit_type,
                    unit_code=unit_code,
                    priority_score=priority_score,
                    priority_rank=1,  # Will rank below
                    urgency=urgency,
                    distance_km=dist_km,
                    estimated_transit_minutes=transit_minutes,
                    status=status,
                    reason=reason,
                    recommended_task=task,
                )
            )

        # Sort descending by priority score
        prioritized_items.sort(key=lambda x: x.priority_score, reverse=True)

        # Assign 1-indexed ranks
        for idx, item in enumerate(prioritized_items[: request.limit]):
            item.priority_rank = idx + 1

        top_items = prioritized_items[: request.limit]

        allocation_summary = {
            "total_available_units": len(available_units),
            "units_within_radius": len(prioritized_items),
            "immediate_dispatch_recommended": sum(1 for i in top_items if i.urgency == ResourceUrgencyEnum.IMMEDIATE),
            "average_eta_minutes": int(sum(i.estimated_transit_minutes for i in top_items) / max(1, len(top_items))),
        }

        return ResourcePrioritizationResponse(
            plan_id=f"plan-{uuid.uuid4().hex[:8]}",
            target_location={"latitude": request.target_latitude, "longitude": request.target_longitude},
            total_units_evaluated=len(available_units),
            prioritized_resources=top_items,
            allocation_summary=allocation_summary,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    async def generate_recommendations(
        self,
        request: RecommendationRequest,
        context_data: Optional[Dict[str, Any]] = None,
    ) -> RecommendationResponse:
        """Generates structured, categorized, actionable Incident Command guidelines."""
        rec_items: List[RecommendationItem] = [
            RecommendationItem(
                id="rec-01",
                category=ActionCategoryEnum.IMMEDIATE_ACTION,
                title="Establish Forward Incident Command Post & Staging Area",
                description="Position mobile command vehicles on elevated ground outside the 100-year flood line to maintain direct radio telemetry.",
                priority_level=RiskLevelEnum.CRITICAL,
                target_sector="Barpeta Central Sector #4",
                actionable_steps=[
                    "Deploy satellite communications trailer at Circuit House grounds.",
                    "Establish designated boat launch staging at NH-31 dry junction.",
                    "Verify secondary VHF radio frequencies across all responding teams.",
                ],
                timeframe="Immediate (0 - 30 minutes)",
            ),
            RecommendationItem(
                id="rec-02",
                category=ActionCategoryEnum.RESOURCE_DEPLOYMENT,
                title="Immediate Mobilization of Motorized Rescue Boats",
                description="Direct 6 high-priority rescue craft to Wards 4 and 7 to extract stranded residents cut off by Bridge B-12 submergence.",
                priority_level=RiskLevelEnum.CRITICAL,
                target_sector="Inundation Sector East",
                actionable_steps=[
                    "Dispatch NDRF Boat Alpha-1 and Alpha-2 to eastern bank slipways.",
                    "Equip each boat with high-intensity floodlights and medical trauma kits.",
                    "Establish patient handover point with waiting ALS ambulances.",
                ],
                timeframe="30 - 60 minutes",
            ),
            RecommendationItem(
                id="rec-03",
                category=ActionCategoryEnum.INFRASTRUCTURE_SAFEGUARD,
                title="Backup Power Safeguard for Civil Hospital",
                description="Barpeta Civil Hospital backup fuel reserves estimated at 6 hours. Secondary power grid failure alert is active.",
                priority_level=RiskLevelEnum.HIGH,
                target_sector="Barpeta Civil Hospital Complex",
                actionable_steps=[
                    "Dispatch mobile 250kVA diesel generator unit from District Depot.",
                    "Route fuel bowser via high-elevation western bypass road.",
                    "Confirm critical ICU/ventilator power circuits are prioritized.",
                ],
                timeframe="1 - 2 hours",
            ),
            RecommendationItem(
                id="rec-04",
                category=ActionCategoryEnum.EVACUATION_CONSIDERATION,
                title="Phased Evacuation of Riverbank Settlements",
                description="Precipitation forecasts project an additional 0.3m water level rise over the next 4 hours in low-lying riverside colonies.",
                priority_level=RiskLevelEnum.HIGH,
                target_sector="Riverine Ward Slums & Lowland Wards",
                actionable_steps=[
                    "Issue localized sirens and automated SMS alert broadcast in Assamese and Bengali.",
                    "Open Sector 4 High School Relief Shelter for displaced families.",
                    "Pre-position drinking water tankers and dry rations at shelter gate.",
                ],
                timeframe="2 - 4 hours",
            ),
            RecommendationItem(
                id="rec-05",
                category=ActionCategoryEnum.MONITORING_FOLLOWUP,
                title="Real-Time Hydrological & Radar Ingestion Cycle",
                description="Continuously recalculate inundation risk contours every 15 minutes using incoming IMD radar rainfall measurements.",
                priority_level=RiskLevelEnum.MODERATE,
                target_sector="Brahmaputra Hydrological Monitoring Basin",
                actionable_steps=[
                    "Stream Doppler radar reflectivity products into JeevanGrid GIS engine.",
                    "Update road network blockage graph automatically upon water depth exceedance.",
                    "Brief District Magistrate and DDMA every 2 hours on revised risk contours.",
                ],
                timeframe="Ongoing / 15-minute cycles",
            ),
        ]

        overall_strategy = (
            f"Multi-agency coordinated response for {request.disaster_type} (Severity Level {request.severity_level}). "
            "Focus priority on life extraction in cut-off wards, safeguarding critical hospital power, "
            "and maintaining resilient bypass supply corridors."
        )

        return RecommendationResponse(
            recommendation_id=f"rec-ai-{uuid.uuid4().hex[:8]}",
            disaster_context=f"{request.disaster_type} Incident at ({request.latitude:.4f}°, {request.longitude:.4f}°)",
            overall_strategy=overall_strategy,
            recommendations=rec_items,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
