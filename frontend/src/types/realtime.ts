/**
 * Real-Time Emergency Operations, Alerts & Notification TypeScript Types
 */

export type AlertSeverity = "INFO" | "WARNING" | "HIGH" | "CRITICAL";

export type AlertStatus = "ACTIVE" | "ACKNOWLEDGED" | "RESOLVED" | "DISMISSED";

export type AlertCategory =
  | "HYDROLOGICAL"
  | "LOGISTICS"
  | "INFRASTRUCTURE"
  | "TACTICAL_DISPATCH"
  | "GENERAL";

export interface Alert {
  alert_id: string;
  alert_code: string;
  severity: AlertSeverity;
  status: AlertStatus;
  category: AlertCategory;
  title: string;
  message: string;
  entity_type: string;
  entity_id: string;
  latitude?: number;
  longitude?: number;
  recommended_action?: string;
  occurrence_count: number;
  created_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
  resolution_notes?: string;
}

export interface OperationalEvent {
  event_id: string;
  event_type: string;
  entity_type: string;
  entity_id: string;
  severity: string;
  source: string;
  latitude?: number;
  longitude?: number;
  payload: Record<string, unknown>;
  timestamp: string;
}

export interface NotificationItem {
  notification_id: string;
  recipient_role: string;
  title: string;
  message: string;
  severity: string;
  related_alert_id?: string;
  is_read: boolean;
  created_at: string;
  read_at?: string;
}

export interface NotificationListResponse {
  total_notifications: number;
  unread_count: number;
  notifications: NotificationItem[];
}

export interface OperationsStatus {
  active_incidents: number;
  critical_incidents: number;
  active_alerts: number;
  critical_alerts: number;
  total_response_units: number;
  available_response_units: number;
  allocated_response_units: number;
  resource_shortages: number;
  active_response_plans: number;
  system_readiness_status: string;
  connected_clients_count: number;
  last_sync_timestamp: string;
}

export interface WebSocketMessage {
  type: string;
  timestamp: string;
  data?: Record<string, unknown>;
  status?: string;
  message?: string;
}
