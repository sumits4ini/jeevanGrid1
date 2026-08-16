/**
 * Dashboard Aggregated Metrics and Activity Log Types
 */

import { Disaster } from "./disaster";
import { HealthResponse } from "./health";
import { ResourceReadinessSummary } from "./resource";
import { RiskSummary } from "./risk";

export interface DashboardKPIMetrics {
  activeDisastersCount: number;
  criticalRiskZonesCount: number;
  totalExposedPopulation: number;
  availableRescueUnits: number;
  totalRescueUnits: number;
  systemOperationalReadiness: number; // 0 to 100%
}

export type ActivitySeverity = "CRITICAL" | "WARNING" | "INFO" | "SUCCESS";

export interface ActivityLogItem {
  id: string;
  timestamp: string;
  title: string;
  description: string;
  severity: ActivitySeverity;
  source: string; // e.g. "GIS_ENGINE", "IMD_RADAR", "EOC_DISPATCH", "DISTRESS_QUEUE"
  targetLocation?: string;
}

export interface DashboardInitialData {
  metrics: DashboardKPIMetrics;
  disasters: Disaster[];
  riskSummary: RiskSummary;
  resourceSummary: ResourceReadinessSummary;
  health: HealthResponse;
  recentActivities: ActivityLogItem[];
}
