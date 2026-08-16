/**
 * Central Dashboard Aggregation Service
 */

import { fetchDisasterSummary } from "./disasterService";
import { fetchSystemHealth } from "./healthService";
import { DashboardInitialData, DashboardKPIMetrics, ActivityLogItem } from "@/types/dashboard";
import { ResourceReadinessSummary } from "@/types/resource";
import { RiskSummary } from "@/types/risk";

export async function fetchDashboardData(): Promise<DashboardInitialData> {
  const [summary, health] = await Promise.all([
    fetchDisasterSummary(),
    fetchSystemHealth(),
  ]);

  const riskSummary: RiskSummary = {
    critical_zones_count: 8,
    high_zones_count: 14,
    moderate_zones_count: 22,
    low_zones_count: 45,
    total_exposed_population: summary.total_affected_population,
    top_risk_zones: [
      {
        h3_index: "8860a4421ffffff",
        latitude: 26.3216,
        longitude: 91.0063,
        population_count: 18450,
        mcda_breakdown: {
          hazard_intensity_score: 0.88,
          exposure_score: 0.92,
          vulnerability_score: 0.85,
          coping_capacity_score: 0.25,
          composite_risk_score: 0.91,
          risk_category: "CRITICAL",
        },
      },
      {
        h3_index: "8860a4423ffffff",
        latitude: 26.3280,
        longitude: 91.0140,
        population_count: 12200,
        mcda_breakdown: {
          hazard_intensity_score: 0.76,
          exposure_score: 0.81,
          vulnerability_score: 0.78,
          coping_capacity_score: 0.32,
          composite_risk_score: 0.82,
          risk_category: "CRITICAL",
        },
      },
    ],
  };

  const resourceSummary: ResourceReadinessSummary = {
    total_units: 32,
    available_units: 18,
    dispatched_units: 10,
    on_mission_units: 4,
    breakdown: {
      NDRF_TEAM: { total: 8, available: 5 },
      RESCUE_BOAT: { total: 10, available: 6 },
      AMBULANCE: { total: 8, available: 4 },
      FOOD_WATER_TRUCK: { total: 4, available: 2 },
      MOBILE_GENERATOR: { total: 2, available: 1 },
      SDRF_TEAM: { total: 0, available: 0 },
      DRONE_SURVEILLANCE: { total: 0, available: 0 },
    },
  };

  const metrics: DashboardKPIMetrics = {
    activeDisastersCount: summary.total_active_disasters,
    criticalRiskZonesCount: riskSummary.critical_zones_count,
    totalExposedPopulation: summary.total_affected_population,
    availableRescueUnits: resourceSummary.available_units,
    totalRescueUnits: resourceSummary.total_units,
    systemOperationalReadiness: 94,
  };

  const recentActivities: ActivityLogItem[] = [
    {
      id: "act-1",
      timestamp: new Date(Date.now() - 120000).toISOString(),
      title: "Bridge B-12 Water Submergence Detected",
      description: "PostGIS spatial intersection detected 0.65m floodwater. Ambulance routing penalized; road link severed.",
      severity: "CRITICAL",
      source: "GIS_SPATIAL_ENGINE",
      targetLocation: "Barpeta NH-31 Link",
    },
    {
      id: "act-2",
      timestamp: new Date(Date.now() - 360000).toISOString(),
      title: "Barpeta Civil Hospital Evacuation Advisory",
      description: "Backup power at 6 hours. Secondary power grid failure alert triggered.",
      severity: "WARNING",
      source: "INFRA_MONITOR",
      targetLocation: "Civil Hospital Barpeta",
    },
    {
      id: "act-3",
      timestamp: new Date(Date.now() - 600000).toISOString(),
      title: "MILP Rescue Dispatch Plan Solved",
      description: "Optimal allocation: 6 NDRF boats assigned to Sector East (Wards 4 & 7). Execution time: 320ms.",
      severity: "SUCCESS",
      source: "MILP_OPTIMIZER",
      targetLocation: "Sector East Depots",
    },
    {
      id: "act-4",
      timestamp: new Date(Date.now() - 900000).toISOString(),
      title: "IMD Weather Radar Ingestion",
      description: "Precipitation rate: 45mm/hr in catchment basin. Inundation depth projection recalculated.",
      severity: "INFO",
      source: "IMD_RADAR_INGEST",
      targetLocation: "Brahmaputra Basin",
    },
  ];

  return {
    metrics,
    disasters: summary.disasters,
    riskSummary,
    resourceSummary,
    health,
    recentActivities,
  };
}
