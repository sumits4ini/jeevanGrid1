/**
 * Risk Assessment & MCDA Types
 */

export type RiskCategory = "LOW" | "MODERATE" | "HIGH" | "CRITICAL";

export interface MCDAScoreBreakdown {
  hazard_intensity_score: number;
  exposure_score: number;
  vulnerability_score: number;
  coping_capacity_score: number;
  composite_risk_score: number;
  risk_category: RiskCategory;
}

export interface HexagonRiskFeature {
  h3_index: string;
  latitude: number;
  longitude: number;
  population_count: number;
  mcda_breakdown: MCDAScoreBreakdown;
}

export interface RiskSummary {
  critical_zones_count: number;
  high_zones_count: number;
  moderate_zones_count: number;
  low_zones_count: number;
  total_exposed_population: number;
  top_risk_zones: HexagonRiskFeature[];
}
