/**
 * Common TypeScript Types for JeevanGrid Frontend
 */

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  timestamp: string;
}

export interface ErrorResponse {
  success: false;
  error_code: string;
  message: string;
  details?: Record<string, unknown>;
  timestamp: string;
}

export type OperationalReadinessStatus = "OPTIMAL" | "STANDBY" | "HIGH_ALERT" | "CRITICAL_ACTION";

export interface NavigationItem {
  name: string;
  href: string;
  iconName: string;
  badge?: string;
  badgeVariant?: "default" | "critical" | "warning" | "success";
}
