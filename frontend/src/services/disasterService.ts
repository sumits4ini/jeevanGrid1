/**
 * Disaster Incidents Service
 */

import { apiClient } from "@/lib/apiClient";
import { Disaster, DisasterSummary } from "@/types/disaster";

export async function fetchDisasters(): Promise<Disaster[]> {
  try {
    const response = await apiClient.get<Disaster[]>("/disasters");
    return response.data;
  } catch {
    // Demo scenario default
    return [
      {
        id: "d1-assam-flood-2026",
        name: "Assam Brahmaputra Flash Flood 2026",
        disaster_type: "FLOOD",
        severity_level: 4,
        status: "ACTIVE",
        description: "Severe riverine inundation across Barpeta low-lying wards. Bridge B-12 submerged.",
        latitude: 26.3216,
        longitude: 91.0063,
        affected_population_estimate: 85400,
        created_at: new Date(Date.now() - 3600000 * 4).toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        id: "d2-chennai-surge-2026",
        name: "Chennai Coastal Storm Surge Alert",
        disaster_type: "CYCLONE",
        severity_level: 3,
        status: "ACTIVE",
        description: "Coastal wind gusts and localized low-elevation water logging in Sector 3.",
        latitude: 13.0827,
        longitude: 80.2707,
        affected_population_estimate: 32000,
        created_at: new Date(Date.now() - 3600000 * 8).toISOString(),
        updated_at: new Date().toISOString(),
      },
    ];
  }
}

export async function fetchDisasterSummary(): Promise<DisasterSummary> {
  try {
    const response = await apiClient.get<DisasterSummary>("/disasters/summary/overview");
    return response.data;
  } catch {
    const disasters = await fetchDisasters();
    return {
      total_active_disasters: disasters.length,
      critical_alerts_count: 5,
      total_affected_population: 117400,
      active_rescue_units: 18,
      disasters,
    };
  }
}
