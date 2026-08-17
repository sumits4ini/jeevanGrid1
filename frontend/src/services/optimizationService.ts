/**
 * Response Optimization & Allocation API Service
 */

import { apiClient } from "@/lib/apiClient";
import {
  IncidentPriorityResponse,
  ResourceAllocationResponse,
  ResourceStatusResponse,
  ResponsePlanResponse,
} from "@/types/optimization";

export async function fetchResponsePlan(): Promise<ResponsePlanResponse> {
  try {
    const payload = {
      incidents: [
        {
          id: "inc-assam-01",
          name: "Assam Brahmaputra Inundation Sector East",
          disaster_type: "FLOOD",
          severity_level: 4,
          latitude: 26.3216,
          longitude: 91.0063,
          affected_population: 85400,
          inundation_depth_m: 1.25,
        },
        {
          id: "inc-chennai-02",
          name: "Chennai Coastal Storm Surge Alert",
          disaster_type: "CYCLONE",
          severity_level: 3,
          latitude: 13.0827,
          longitude: 80.2707,
          affected_population: 32000,
        },
      ],
      max_search_radius_km: 50.0,
      include_ai_advisory: true,
    };
    const response = await apiClient.post<ResponsePlanResponse>("/optimization/response-plan", payload);
    return response.data;
  } catch {
    // High-fidelity fallback for offline UI development
    return {
      plan_id: "plan-opt-mock-01",
      generated_at: new Date().toISOString(),
      incident_priorities: [
        {
          incident_id: "inc-assam-01",
          name: "Assam Brahmaputra Inundation Sector East",
          disaster_type: "FLOOD",
          priority_rank: 1,
          priority_score: 0.91,
          priority_level: "CRITICAL",
          contributing_factors: {
            severity_score: 0.8,
            risk_score: 0.88,
            urgency_score: 0.95,
            population_impact_score: 0.82,
            geographic_impact_score: 0.85,
            resource_shortage_score: 0.85,
          },
          explanation: "Critical level flood wave cut off Wards 4 & 7. 85,400 exposed residents.",
        },
        {
          incident_id: "inc-chennai-02",
          name: "Chennai Coastal Storm Surge Alert",
          disaster_type: "CYCLONE",
          priority_rank: 2,
          priority_score: 0.65,
          priority_level: "HIGH",
          contributing_factors: {
            severity_score: 0.6,
            risk_score: 0.62,
            urgency_score: 0.70,
            population_impact_score: 0.75,
            geographic_impact_score: 0.48,
            resource_shortage_score: 0.50,
          },
          explanation: "High priority storm surge with localized coastal inundation.",
        },
      ],
      deployment_sequence: [
        {
          deployment_order: 1,
          incident_id: "inc-assam-01",
          incident_name: "Assam Brahmaputra Inundation Sector East",
          priority_level: "CRITICAL",
          resource_id: "ru-boat-01",
          resource_name: "NDRF Rescue Boat Alpha-1",
          resource_type: "RESCUE_BOAT",
          resource_code: "BOAT-NDRF-01",
          allocated_quantity: 1,
          estimated_eta_minutes: 4,
          is_eta_estimated: true,
          staging_point: "NH-31 Dry Slipway Junction",
        },
        {
          deployment_order: 2,
          incident_id: "inc-assam-01",
          incident_name: "Assam Brahmaputra Inundation Sector East",
          priority_level: "CRITICAL",
          resource_id: "ru-boat-02",
          resource_name: "NDRF Rescue Boat Alpha-2",
          resource_type: "RESCUE_BOAT",
          resource_code: "BOAT-NDRF-02",
          allocated_quantity: 1,
          estimated_eta_minutes: 6,
          is_eta_estimated: true,
          staging_point: "Sector 7 Embankment Depot",
        },
        {
          deployment_order: 3,
          incident_id: "inc-assam-01",
          incident_name: "Assam Brahmaputra Inundation Sector East",
          priority_level: "CRITICAL",
          resource_id: "ru-amb-01",
          resource_name: "ALS Ambulance Unit 108-A",
          resource_type: "AMBULANCE",
          resource_code: "AMB-108-A",
          allocated_quantity: 1,
          estimated_eta_minutes: 8,
          is_eta_estimated: true,
          staging_point: "Western High-Elevation Bypass Node",
        },
      ],
      allocations: [
        {
          assignment_id: "asgn-01",
          incident_id: "inc-assam-01",
          incident_name: "Assam Brahmaputra Inundation Sector East",
          resource_id: "ru-boat-01",
          resource_name: "NDRF Rescue Boat Alpha-1",
          resource_type: "RESCUE_BOAT",
          resource_code: "BOAT-NDRF-01",
          allocated_quantity: 1,
          priority_level: "CRITICAL",
          distance_km: 1.42,
          estimated_travel_time_minutes: 4,
          is_travel_time_estimated: true,
          suitability_score: 0.96,
          reason: "Closest shallow-draft boat unit with immediate riverine deployment capacity.",
          task_assignment: "Residential evacuation in low-lying Ward 4.",
        },
      ],
      unresolved_shortages: [
        {
          incident_id: "inc-assam-01",
          incident_name: "Assam Brahmaputra Inundation Sector East",
          resource_type: "FOOD_WATER_TRUCK",
          quantity_demanded: 1,
          quantity_allocated: 0,
          shortage_count: 1,
          urgency: "HIGH",
          impact_explanation: "Supply deficit for clean drinking water tankers in flood relief camps.",
          recommended_mitigation: "Requisition inter-district mutual aid logistics from Guwahati Supply Base.",
        },
      ],
      operational_warnings: [
        {
          warning_code: "BRIDGE_SEVERANCE",
          severity: "CRITICAL",
          title: "Bridge B-12 Impassable (0.65m Submergence)",
          message: "All ground vehicles must use Western Bypass. Estimated transit +6 mins.",
          affected_incident_id: "inc-assam-01",
        },
        {
          warning_code: "RESOURCE_DEFICIT",
          severity: "HIGH",
          title: "Drinking Water Logistic Shortage",
          message: "Local depot tanker capacity exhausted. Mutual aid requested.",
          affected_incident_id: "inc-assam-01",
        },
      ],
      recommended_actions: [
        "Deploy 3 authorized rescue units according to priority dispatch order.",
        "Establish forward tactical communications link with lead NDRF rescue craft.",
        "Transmit mutual aid requisition to State EOC for unfulfilled water supply tanker.",
        "[AI Advisory] Backup Generator Dispatch: Route 250kVA unit to Barpeta Civil Hospital.",
      ],
      plan_summary: {
        total_incidents: 2,
        critical_incidents_count: 1,
        total_units_allocated: 3,
        total_shortages_count: 1,
        average_deployment_eta_mins: 6,
      },
      disclaimer: "Deterministic Emergency Response Plan generated for decision-support. Incident Commander authorization required prior to field dispatch.",
    };
  }
}

export async function fetchResourceStatus(): Promise<ResourceStatusResponse> {
  try {
    const response = await apiClient.get<ResourceStatusResponse>("/optimization/resource-status");
    return response.data;
  } catch {
    return {
      total_units: 32,
      available_units: 18,
      readiness_percentage: 56.3,
      breakdown: {
        RESCUE_BOAT: { total: 10, available: 6 },
        AMBULANCE: { total: 8, available: 4 },
        NDRF_TEAM: { total: 8, available: 5 },
        FOOD_WATER_TRUCK: { total: 4, available: 2 },
        MOBILE_GENERATOR: { total: 2, available: 1 },
      },
      units: [],
    };
  }
}
