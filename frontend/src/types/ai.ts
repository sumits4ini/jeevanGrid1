/**
 * AI Intelligence & Decision Support TypeScript Interfaces
 */

export type RiskLevel = "LOW" | "MODERATE" | "HIGH" | "CRITICAL";

export type ResourceUrgency = "IMMEDIATE" | "URGENT" | "STANDARD" | "STANDBY";

export type ActionCategory =
  | "IMMEDIATE_ACTION"
  | "RESOURCE_DEPLOYMENT"
  | "EVACUATION_CONSIDERATION"
  | "INFRASTRUCTURE_SAFEGUARD"
  | "MONITORING_FOLLOWUP";

export interface RiskFactor {
  category: string;
  factor_name: string;
  severity_score: number;
  description: string;
  mitigation_hint?: string;
}

export interface RiskAnalysisResponse {
  analysis_id: string;
  disaster_name: string;
  risk_score: number;
  risk_level: RiskLevel;
  confidence_score: number;
  priority_level: string;
  affected_area_summary: string;
  risk_factors: RiskFactor[];
  possible_consequences: string[];
  recommended_actions: string[];
  resource_requirements: Record<string, number>;
  generated_at: string;
}

export interface ResourcePriorityItem {
  unit_id: string;
  unit_name: string;
  unit_type: string;
  unit_code: string;
  priority_score: number;
  priority_rank: number;
  urgency: ResourceUrgency;
  distance_km: number;
  estimated_transit_minutes: number;
  status: string;
  reason: string;
  recommended_task: string;
}

export interface ResourcePrioritizationResponse {
  plan_id: string;
  target_location: { latitude: number; longitude: number };
  total_units_evaluated: number;
  prioritized_resources: ResourcePriorityItem[];
  allocation_summary: {
    total_available_units: number;
    units_within_radius: number;
    immediate_dispatch_recommended: number;
    average_eta_minutes: number;
  };
  generated_at: string;
}

export interface RecommendationItem {
  id: string;
  category: ActionCategory;
  title: string;
  description: string;
  priority_level: RiskLevel;
  target_sector: string;
  actionable_steps: string[];
  timeframe: string;
}

export interface RecommendationResponse {
  recommendation_id: string;
  disaster_context: string;
  overall_strategy: string;
  recommendations: RecommendationItem[];
  disclaimer: string;
  generated_at: string;
}
