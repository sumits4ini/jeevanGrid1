/**
 * Disaster Entity Types
 */

export type DisasterType = "FLOOD" | "CYCLONE" | "LANDSLIDE" | "EARTHQUAKE" | "URBAN_FIRE" | "OTHER";
export type DisasterStatus = "ACTIVE" | "CONTAINED" | "RESOLVED" | "SIMULATED";

export interface Disaster {
  id: string;
  name: string;
  disaster_type: DisasterType;
  severity_level: number; // 1 to 5
  status: DisasterStatus;
  description?: string;
  latitude: number;
  longitude: number;
  affected_population_estimate?: number;
  created_at: string;
  updated_at: string;
}

export interface DisasterSummary {
  total_active_disasters: number;
  critical_alerts_count: number;
  total_affected_population: number;
  active_rescue_units: number;
  disasters: Disaster[];
}
