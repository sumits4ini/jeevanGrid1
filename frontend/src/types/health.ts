/**
 * System Health & Telemetry Types
 */

export interface HealthServiceStatus {
  status: "healthy" | "ready" | "configured" | "degraded" | "offline";
  latency_ms?: number;
  message?: string;
}

export interface HealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  app_name: string;
  app_version: string;
  environment: string;
  simulation_mode: boolean;
  timestamp: string;
  services: Record<string, HealthServiceStatus>;
}
