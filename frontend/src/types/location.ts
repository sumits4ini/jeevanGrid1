/**
 * Critical Infrastructure & Location Types
 */

export type FacilityType =
  | "HOSPITAL"
  | "POWER_SUBSTATION"
  | "WATER_TREATMENT"
  | "BRIDGE"
  | "COMM_TOWER"
  | "SHELTER"
  | "FIRE_STATION"
  | "POLICE_STATION";

export type FacilityOperationalStatus = "OPERATIONAL" | "DEGRADED" | "FAILED" | "CUT_OFF" | "UNKNOWN";

export interface CriticalInfrastructure {
  id: string;
  name: string;
  facility_type: FacilityType;
  operational_status: FacilityOperationalStatus;
  latitude: number;
  longitude: number;
  max_capacity: number;
  current_occupancy: number;
  backup_power_hours: number;
  contact_phone?: string;
  is_threatened?: boolean;
  distance_to_nearest_hazard_m?: number;
}
