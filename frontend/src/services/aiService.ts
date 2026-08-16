/**
 * AI Decision Support API Service
 */

import { apiClient } from "@/lib/apiClient";
import {
  RecommendationResponse,
  ResourcePrioritizationResponse,
  RiskAnalysisResponse,
} from "@/types/ai";

export async function fetchAIRiskAnalysis(): Promise<RiskAnalysisResponse> {
  try {
    const payload = {
      disaster_name: "Assam Brahmaputra Basin Inundation 2026",
      disaster_type: "FLOOD",
      severity_level: 4,
      latitude: 26.3216,
      longitude: 91.0063,
      affected_population_estimate: 85400,
      inundation_depth_m: 1.25,
    };
    const response = await apiClient.post<RiskAnalysisResponse>("/ai/risk-analysis", payload);
    return response.data;
  } catch {
    // High-fidelity fallback for offline frontend development
    return {
      analysis_id: "risk-ai-mock-01",
      disaster_name: "Assam Brahmaputra Flash Flood 2026",
      risk_score: 0.88,
      risk_level: "CRITICAL",
      confidence_score: 0.94,
      priority_level: "CRITICAL / DEFCON 1",
      affected_area_summary: "Severe riverine flood wave across Barpeta lowlands. 85,400 exposed residents.",
      risk_factors: [
        {
          category: "Hydrological",
          factor_name: "Surface Water Inundation Depth",
          severity_score: 0.88,
          description: "Inundation depth recorded at 1.25m in low-lying sector.",
          mitigation_hint: "Deploy motorized shallow-draft rescue craft.",
        },
        {
          category: "Demographic",
          factor_name: "Vulnerable Population Exposure",
          severity_score: 0.92,
          description: "Estimated 85,400 residents residing within the immediate hazard perimeter.",
          mitigation_hint: "Issue ward-level automated evacuation advisories.",
        },
        {
          category: "Infrastructure",
          factor_name: "Transportation Corridor Severance",
          severity_score: 0.85,
          description: "Key bridge links and low-elevation arterial roads compromised by flood surge.",
          mitigation_hint: "Reroute ambulances via secondary elevated bypass roads.",
        },
      ],
      possible_consequences: [
        "Complete physical isolation of low-lying wards without boat access.",
        "Secondary grid failure at Barpeta East Power Substation #4.",
        "Drinking water contamination in suburban relief zones.",
      ],
      recommended_actions: [
        "Establish forward Incident Command Post on elevated terrain.",
        "Mobilize 6 NDRF boat teams for urgent residential evacuations.",
        "Deploy mobile emergency generator to Barpeta Civil Hospital.",
      ],
      resource_requirements: {
        RESCUE_BOAT: 8,
        AMBULANCE: 6,
        NDRF_TEAM: 4,
        FOOD_WATER_TRUCK: 3,
        MOBILE_GENERATOR: 2,
      },
      generated_at: new Date().toISOString(),
    };
  }
}

export async function fetchAIResourcePriorities(): Promise<ResourcePrioritizationResponse> {
  try {
    const payload = {
      target_latitude: 26.3216,
      target_longitude: 91.0063,
      disaster_type: "FLOOD",
      severity_level: 4,
      max_search_radius_km: 50.0,
      limit: 10,
    };
    const response = await apiClient.post<ResourcePrioritizationResponse>("/ai/resource-priority", payload);
    return response.data;
  } catch {
    return {
      plan_id: "plan-mock-01",
      target_location: { latitude: 26.3216, longitude: 91.0063 },
      total_units_evaluated: 4,
      prioritized_resources: [
        {
          unit_id: "ru-boat-01",
          unit_name: "NDRF Rescue Boat Alpha-1",
          unit_type: "RESCUE_BOAT",
          unit_code: "BOAT-NDRF-01",
          priority_score: 0.96,
          priority_rank: 1,
          urgency: "IMMEDIATE",
          distance_km: 1.42,
          estimated_transit_minutes: 4,
          status: "AVAILABLE",
          reason: "Motorized boat 1.4km from epicenter. Immediate access to eastern flood slipways.",
          recommended_task: "Extract stranded residents in Ward 4 residential cluster.",
        },
        {
          unit_id: "ru-boat-02",
          unit_name: "NDRF Rescue Boat Alpha-2",
          unit_type: "RESCUE_BOAT",
          unit_code: "BOAT-NDRF-02",
          priority_score: 0.91,
          priority_rank: 2,
          urgency: "IMMEDIATE",
          distance_km: 2.15,
          estimated_transit_minutes: 6,
          status: "AVAILABLE",
          reason: "Rescue craft stationed at southern depot. Optimal for Sector 7 evacuation.",
          recommended_task: "Support elderly and triage transfers to dry staging point.",
        },
        {
          unit_id: "ru-amb-01",
          unit_name: "ALS Ambulance Unit 108-A",
          unit_type: "AMBULANCE",
          unit_code: "AMB-108-A",
          priority_score: 0.78,
          priority_rank: 3,
          urgency: "URGENT",
          distance_km: 3.20,
          estimated_transit_minutes: 8,
          status: "AVAILABLE",
          reason: "Advanced Life Support unit pre-positioned at Western Medical Hub.",
          recommended_task: "Standby at boat handover landing on elevated NH-31 bypass.",
        },
      ],
      allocation_summary: {
        total_available_units: 4,
        units_within_radius: 3,
        immediate_dispatch_recommended: 2,
        average_eta_minutes: 6,
      },
      generated_at: new Date().toISOString(),
    };
  }
}

export async function fetchAIRecommendations(): Promise<RecommendationResponse> {
  try {
    const payload = {
      disaster_type: "FLOOD",
      severity_level: 4,
      latitude: 26.3216,
      longitude: 91.0063,
    };
    const response = await apiClient.post<RecommendationResponse>("/ai/recommendations", payload);
    return response.data;
  } catch {
    return {
      recommendation_id: "rec-mock-01",
      disaster_context: "FLOOD Incident at (26.3216°, 91.0063°)",
      overall_strategy: "Multi-agency coordinated response prioritizing life extraction in cut-off wards and hospital backup power.",
      recommendations: [
        {
          id: "rec-01",
          category: "IMMEDIATE_ACTION",
          title: "Establish Forward Incident Command Post",
          description: "Position mobile command vehicle on elevated ground to maintain satellite telemetry.",
          priority_level: "CRITICAL",
          target_sector: "Barpeta Central Sector #4",
          actionable_steps: [
            "Deploy satellite communications trailer at Circuit House grounds.",
            "Establish designated boat launch staging at NH-31 dry junction.",
          ],
          timeframe: "Immediate (0 - 30 minutes)",
        },
        {
          id: "rec-02",
          category: "RESOURCE_DEPLOYMENT",
          title: "Mobilize Motorized Rescue Boats to Sector East",
          description: "Direct 6 rescue boats to extract stranded residents cut off by Bridge B-12 submergence.",
          priority_level: "CRITICAL",
          target_sector: "Inundation Sector East (Wards 4 & 7)",
          actionable_steps: [
            "Dispatch NDRF Boat Alpha-1 and Alpha-2 to eastern slipways.",
            "Equip teams with floodlights and trauma stabilization kits.",
          ],
          timeframe: "30 - 60 minutes",
        },
        {
          id: "rec-03",
          category: "INFRASTRUCTURE_SAFEGUARD",
          title: "Backup Generator Dispatch to Barpeta Civil Hospital",
          description: "Civil Hospital backup fuel reserves at 6 hours. Secondary power grid failure alert active.",
          priority_level: "HIGH",
          target_sector: "Barpeta Civil Hospital Complex",
          actionable_steps: [
            "Dispatch mobile 250kVA generator from District Depot.",
            "Route fuel bowser via high-elevation western bypass road.",
          ],
          timeframe: "1 - 2 hours",
        },
      ],
      disclaimer: "AI-generated decision support advisory. Operational actions must be verified by Incident Commander.",
      generated_at: new Date().toISOString(),
    };
  }
}
