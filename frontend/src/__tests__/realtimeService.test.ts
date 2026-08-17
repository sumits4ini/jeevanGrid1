import { describe, it, expect } from "vitest";
import {
  fetchOperationsStatus,
  fetchTacticalAlerts,
  fetchNotifications,
  fetchOperationalEvents,
} from "@/services/realtimeService";

describe("Realtime Service Client", () => {
  it("returns structured operations status metrics", async () => {
    const status = await fetchOperationsStatus();
    expect(status).toBeDefined();
    expect(status.active_incidents).toBeGreaterThanOrEqual(1);
    expect(status.total_response_units).toBeGreaterThanOrEqual(4);
    expect(status.system_readiness_status).toBeDefined();
  });

  it("returns tactical alert anomalies with deduplication metadata", async () => {
    const alerts = await fetchTacticalAlerts();
    expect(alerts).toBeInstanceOf(Array);
    expect(alerts.length).toBeGreaterThanOrEqual(1);
    const firstAlert = alerts[0];
    expect(firstAlert.alert_id).toBeDefined();
    expect(firstAlert.severity).toBeDefined();
    expect(firstAlert.occurrence_count).toBeGreaterThanOrEqual(1);
  });

  it("returns in-app notifications with unread counter", async () => {
    const notifs = await fetchNotifications();
    expect(notifs).toBeDefined();
    expect(notifs.notifications).toBeInstanceOf(Array);
    expect(typeof notifs.unread_count).toBe("number");
  });

  it("returns operational event telemetry stream", async () => {
    const events = await fetchOperationalEvents(5);
    expect(events).toBeInstanceOf(Array);
    expect(events.length).toBeGreaterThanOrEqual(1);
    expect(events[0].event_type).toBeDefined();
  });
});
