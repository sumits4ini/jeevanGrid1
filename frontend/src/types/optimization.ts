/**
 * Response Optimization & Resource Allocation TypeScript Types
 */

export type PriorityLevel = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

export interface ContributingFactors {
  severity_score: number;
  risk_score: number;
  urgency_score: number;
  population_impact_score: number;
  geographic_impact_score: number;
  resource_shortage_score: number;
}

export interface PrioritizedIncident {
  incident_id: string;
  name: string;
  disaster_type: string;
  priority_rank: number;
  priority_score: number;
  priority_level: PriorityLevel;
  contributing_factors: ContributingFactors;
  explanation: string;
}

export interface IncidentPriorityResponse {
  total_incidents: number;
  prioritized_incidents: PrioritizedIncident[];
  scoring_methodology: string;
  generated_at: string;
}

export interface ResourceAssignment {
  assignment_id: string;
  incident_id: string;
  incident_name: string;
  resource_id: string;
  resource_name: string;
  resource_type: string;
  resource_code: string;
  allocated_quantity: number;
  priority_level: PriorityLevel;
  distance_km: number;
  estimated_travel_time_minutes: number;
  is_travel_time_estimated: boolean;
  suitability_score: number;
  reason: string;
  task_assignment: string;
}

export interface ResourceShortage {
  incident_id: string;
  incident_name: string;
  resource_type: string;
  quantity_demanded: number;
  quantity_allocated: number;
  shortage_count: number;
  urgency: string;
  impact_explanation: string;
  recommended_mitigation: string;
}

export interface ResourceAllocationResponse {
  allocation_id: string;
  total_assignments: number;
  total_shortages: number;
  assignments: ResourceAssignment[];
  shortages: ResourceShortage[];
  allocation_summary: Record<string, unknown>;
  generated_at: string;
}

export interface DeploymentOrderItem {
  deployment_order: number;
  incident_id: string;
  incident_name: string;
  priority_level: PriorityLevel;
  resource_id: string;
  resource_name: string;
  resource_type: string;
  resource_code: string;
  allocated_quantity: number;
  estimated_eta_minutes: number;
  is_eta_estimated: boolean;
  staging_point: string;
}

export interface OperationalWarning {
  warning_code: string;
  severity: string;
  title: string;
  message: string;
  affected_incident_id?: string;
}

export interface ResponsePlanResponse {
  plan_id: string;
  generated_at: string;
  incident_priorities: PrioritizedIncident[];
  deployment_sequence: DeploymentOrderItem[];
  allocations: ResourceAssignment[];
  unresolved_shortages: ResourceShortage[];
  operational_warnings: OperationalWarning[];
  recommended_actions: string[];
  plan_summary: {
    total_incidents: number;
    critical_incidents_count: number;
    total_units_allocated: number;
    total_shortages_count: number;
    average_deployment_eta_mins: number;
  };
  disclaimer: string;
}

export interface ResourceStatusResponse {
  total_units: number;
  available_units: number;
  readiness_percentage: number;
  breakdown: Record<string, { total: number; available: number }>;
  units: Array<Record<string, unknown>>;
}
