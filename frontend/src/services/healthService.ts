/**
 * Health & Subsystem Telemetry Service
 */

import { apiClient } from "@/lib/apiClient";
import { HealthResponse } from "@/types/health";

export async function fetchSystemHealth(): Promise<HealthResponse> {
  try {
    const response = await apiClient.get<HealthResponse>("/health");
    return response.data;
  } catch {
    // Graceful offline fallback data for frontend development
    return {
      status: "degraded",
      app_name: "JeevanGrid Disaster Intelligence Platform",
      app_version: "0.1.0",
      environment: "development (local UI mode)",
      simulation_mode: true,
      timestamp: new Date().toISOString(),
      services: {
        api_gateway: { status: "ready", message: "FastAPI Gateway configured" },
        gis_engine: { status: "ready", message: "Spatial core initialized" },
        risk_engine: { status: "ready", message: "MCDA risk matrix ready" },
        optimizer: { status: "ready", message: "MILP solver ready" },
        database: { status: "offline", message: "PostgreSQL/PostGIS awaiting connection" },
      },
    };
  }
}
