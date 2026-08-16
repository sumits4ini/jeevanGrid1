/**
 * Emergency Response Resource & Unit Types
 */

export type UnitType =
  | "NDRF_TEAM"
  | "SDRF_TEAM"
  | "AMBULANCE"
  | "RESCUE_BOAT"
  | "FOOD_WATER_TRUCK"
  | "MOBILE_GENERATOR"
  | "DRONE_SURVEILLANCE";

export type UnitStatus = "AVAILABLE" | "DISPATCHED" | "ON_MISSION" | "MAINTENANCE" | "OFFLINE";

export interface ResponseUnit {
  id: string;
  unit_code: string;
  unit_type: UnitType;
  status: UnitStatus;
  latitude: number;
  longitude: number;
  capacity_payload: Record<string, unknown>;
  assigned_incident_id?: string;
}

export interface ResourceReadinessSummary {
  total_units: number;
  available_units: number;
  dispatched_units: number;
  on_mission_units: number;
  breakdown: Record<UnitType, { total: number; available: number }>;
}
