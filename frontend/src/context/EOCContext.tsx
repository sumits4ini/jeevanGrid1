"use client";

import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { Alert, NotificationItem, OperationalEvent, OperationsStatus } from "@/types/realtime";
import {
  acknowledgeAlert as apiAcknowledgeAlert,
  resolveAlert as apiResolveAlert,
  fetchOperationsStatus,
  fetchOperationalEvents,
  fetchTacticalAlerts,
  fetchNotifications,
} from "@/services/realtimeService";
import { useRealtimeOperations, ConnectionStatus } from "@/hooks/useRealtimeOperations";

export interface Incident {
  id: string;
  name: string;
  type: string;
  severity_level: number;
  status: "ACTIVE" | "CONTAINED" | "RESOLVED";
  latitude: number;
  longitude: number;
  affected_population: number;
  inundation_depth_m?: number;
  reported_at: string;
  description: string;
  hazard_zones_count: number;
  criticality: string;
}

export interface ResourceUnit {
  id: string;
  unit_code: string;
  name: string;
  unit_type: "RESCUE_BOAT" | "AMBULANCE" | "NDRF_TEAM" | "HOSPITAL" | "POWER_STATION" | "SHELTER";
  status: "AVAILABLE" | "ASSIGNED" | "STANDBY" | "OFFLINE";
  capacity: string;
  latitude: number;
  longitude: number;
  assigned_incident_id?: string;
  assigned_incident_name?: string;
  current_task?: string;
}

export interface RiskHex {
  hex_id: string;
  location_name: string;
  risk_score: number;
  tier: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  population: number;
  inundation_depth_m: number;
  critical_facilities: string[];
  latitude: number;
  longitude: number;
}

interface EOCContextType {
  // Telemetry & Connection
  connectionStatus: ConnectionStatus;
  lastUpdated: string;
  secondsSinceSync: number;
  isRefreshing: boolean;
  refreshAll: () => Promise<void>;

  // Operations Status KPI
  operationsStatus: OperationsStatus;

  // Disasters / Incidents
  disasters: Incident[];
  selectedDisaster: Incident | null;
  selectDisaster: (id: string) => void;
  escalateDisaster: (id: string) => void;
  resolveDisaster: (id: string) => void;

  // Tactical Alerts
  alerts: Alert[];
  acknowledgeAlert: (alertId: string, acknowledgedBy?: string, notes?: string) => Promise<void>;
  resolveAlert: (alertId: string, resolvedBy?: string, notes?: string) => Promise<void>;

  // Emergency Resources
  resources: ResourceUnit[];
  assignResourceToIncident: (unitId: string, incidentId: string, taskDescription?: string) => void;
  releaseResource: (unitId: string) => void;

  // Risk Zones
  riskZones: RiskHex[];
  selectedHex: RiskHex | null;
  selectRiskHex: (hexId: string) => void;

  // Live Events Stream
  liveEvents: OperationalEvent[];
}

const INITIAL_DISASTERS: Incident[] = [
  {
    id: "dis-assam-01",
    name: "Assam Brahmaputra Basin Inundation 2026",
    type: "FLOOD",
    severity_level: 4,
    status: "ACTIVE",
    latitude: 26.3216,
    longitude: 91.0063,
    affected_population: 85400,
    inundation_depth_m: 1.25,
    reported_at: "2026-08-16T14:30:00Z",
    description: "Severe riverine flood wave across Barpeta lowlands. Critical bridge access severed.",
    hazard_zones_count: 3,
    criticality: "DEFCON 1 • CRITICAL",
  },
  {
    id: "dis-chennai-02",
    name: "Chennai Coastal Storm Surge Alert",
    type: "CYCLONE",
    severity_level: 3,
    status: "ACTIVE",
    latitude: 13.0827,
    longitude: 80.2707,
    affected_population: 32000,
    inundation_depth_m: 0.45,
    reported_at: "2026-08-17T06:15:00Z",
    description: "Deep depression in Bay of Bengal generating 45 knot gusts and storm tides.",
    hazard_zones_count: 2,
    criticality: "DEFCON 2 • HIGH ALERT",
  },
];

const INITIAL_RESOURCES: ResourceUnit[] = [
  {
    id: "ru-boat-01",
    unit_code: "BOAT-NDRF-01",
    name: "NDRF Rescue Craft Alpha-1",
    unit_type: "RESCUE_BOAT",
    status: "AVAILABLE",
    capacity: "12 Persons / Shallow Draft",
    latitude: 26.3200,
    longitude: 91.0080,
    assigned_incident_name: "Assam Flood Sector East",
    current_task: "Pre-positioned at NH-31 dry slipway junction.",
  },
  {
    id: "ru-boat-02",
    unit_code: "BOAT-NDRF-02",
    name: "NDRF Rescue Craft Alpha-2",
    unit_type: "RESCUE_BOAT",
    status: "AVAILABLE",
    capacity: "12 Persons / Shallow Draft",
    latitude: 26.3150,
    longitude: 91.0120,
    assigned_incident_name: "Assam Flood Sector East",
    current_task: "Standby for Ward 4 triage extraction.",
  },
  {
    id: "ru-amb-01",
    unit_code: "AMB-108-A",
    name: "ALS Ambulance Unit 108-A",
    unit_type: "AMBULANCE",
    status: "AVAILABLE",
    capacity: "2 Stretcher / Critical Life Support",
    latitude: 26.3200,
    longitude: 91.0200,
    assigned_incident_name: "Assam Flood Sector East",
    current_task: "Standby at high-elevation Western Bypass node.",
  },
  {
    id: "ru-ndrf-01",
    unit_code: "NDRF-BAT-01",
    name: "1st Battalion NDRF Rescue Team",
    unit_type: "NDRF_TEAM",
    status: "ASSIGNED",
    capacity: "45 Tactical Specialists",
    latitude: 26.3216,
    longitude: 91.0063,
    assigned_incident_id: "dis-assam-01",
    assigned_incident_name: "Assam Brahmaputra Basin Inundation",
    current_task: "Conducting house-to-house boat extractions.",
  },
  {
    id: "loc-hosp-01",
    unit_code: "HOSP-BARPETA",
    name: "Barpeta District Civil Hospital",
    unit_type: "HOSPITAL",
    status: "STANDBY",
    capacity: "350 Beds / Trauma Unit",
    latitude: 26.3260,
    longitude: 91.0110,
    assigned_incident_name: "Assam Flood Sector East",
    current_task: "Emergency ward operating on generator power.",
  },
];

const INITIAL_RISK_ZONES: RiskHex[] = [
  {
    hex_id: "8860145b23fffff",
    location_name: "Barpeta Ward 4 Residential Core",
    risk_score: 0.94,
    tier: "CRITICAL",
    population: 48500,
    inundation_depth_m: 1.25,
    critical_facilities: ["Civil Hospital (Backup power only)", "Substation #4 (Offline)"],
    latitude: 26.3216,
    longitude: 91.0063,
  },
  {
    hex_id: "8860145b27fffff",
    location_name: "Barpeta East Bridge Approach",
    risk_score: 0.78,
    tier: "HIGH",
    population: 36900,
    inundation_depth_m: 0.85,
    critical_facilities: ["Bridge B-12 (Impassable)"],
    latitude: 26.3180,
    longitude: 91.0150,
  },
  {
    hex_id: "8860145b2bfffff",
    location_name: "Northwestern Agricultural Sector",
    risk_score: 0.45,
    tier: "MEDIUM",
    population: 18200,
    inundation_depth_m: 0.35,
    critical_facilities: ["Primary Health Clinic"],
    latitude: 26.3350,
    longitude: 90.9850,
  },
];

const EOCContext = createContext<EOCContextType | undefined>(undefined);

export const EOCProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { status: connectionStatus, latestAlert, latestEvent } = useRealtimeOperations();

  const [disasters, setDisasters] = useState<Incident[]>(INITIAL_DISASTERS);
  const [selectedDisaster, setSelectedDisaster] = useState<Incident | null>(INITIAL_DISASTERS[0]);
  const [resources, setResources] = useState<ResourceUnit[]>(INITIAL_RESOURCES);
  const [riskZones, setRiskZones] = useState<RiskHex[]>(INITIAL_RISK_ZONES);
  const [selectedHex, setSelectedHex] = useState<RiskHex | null>(INITIAL_RISK_ZONES[0]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [liveEvents, setLiveEvents] = useState<OperationalEvent[]>([]);
  const [operationsStatus, setOperationsStatus] = useState<OperationsStatus>({
    active_incidents: 2,
    critical_incidents: 1,
    active_alerts: 3,
    critical_alerts: 1,
    total_response_units: 32,
    available_response_units: 18,
    allocated_response_units: 14,
    resource_shortages: 1,
    active_response_plans: 1,
    system_readiness_status: "CRITICAL_DEFCON_1",
    connected_clients_count: 1,
    last_sync_timestamp: new Date().toISOString(),
  });

  const [lastUpdated, setLastUpdated] = useState<string>(new Date().toLocaleTimeString());
  const [secondsSinceSync, setSecondsSinceSync] = useState<number>(0);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);

  // Initial Data Hydration
  const refreshAll = useCallback(async () => {
    setIsRefreshing(true);
    try {
      const [ops, fetchedAlerts, fetchedEvents] = await Promise.all([
        fetchOperationsStatus(),
        fetchTacticalAlerts(),
        fetchOperationalEvents(15),
      ]);
      setOperationsStatus(ops);
      setAlerts(fetchedAlerts);
      setLiveEvents(fetchedEvents);
      setLastUpdated(new Date().toLocaleTimeString());
      setSecondsSinceSync(0);
    } catch {
      // Retain existing state on fallback
    } finally {
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    refreshAll();
  }, [refreshAll]);

  // Sync Timer (Seconds Since Last Update)
  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsSinceSync((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Listen to incoming WebSocket alerts & events
  useEffect(() => {
    if (latestAlert) {
      setAlerts((prev) => {
        const existingIdx = prev.findIndex((a) => a.alert_id === latestAlert.alert_id);
        if (existingIdx >= 0) {
          const updated = [...prev];
          updated[existingIdx] = latestAlert;
          return updated;
        }
        return [latestAlert, ...prev];
      });
    }
  }, [latestAlert]);

  useEffect(() => {
    if (latestEvent) {
      setLiveEvents((prev) => [latestEvent, ...prev.slice(0, 49)]);
    }
  }, [latestEvent]);

  // Alert Lifecycle Actions
  const acknowledgeAlert = async (alertId: string, acknowledgedBy = "EOC_COMMANDER", notes = "Acknowledged") => {
    try {
      const updated = await apiAcknowledgeAlert(alertId, acknowledgedBy, notes);
      setAlerts((prev) => prev.map((a) => (a.alert_id === alertId ? updated : a)));
    } catch {
      setAlerts((prev) =>
        prev.map((a) =>
          a.alert_id === alertId
            ? { ...a, status: "ACKNOWLEDGED", acknowledged_at: new Date().toISOString() }
            : a
        )
      );
    }
  };

  const resolveAlert = async (alertId: string, resolvedBy = "EOC_COMMANDER", notes = "Resolved in field") => {
    try {
      const updated = await apiResolveAlert(alertId, resolvedBy, notes);
      setAlerts((prev) => prev.map((a) => (a.alert_id === alertId ? updated : a)));
    } catch {
      setAlerts((prev) =>
        prev.map((a) =>
          a.alert_id === alertId
            ? { ...a, status: "RESOLVED", resolved_at: new Date().toISOString() }
            : a
        )
      );
    }
  };

  // Disaster Management Actions
  const selectDisaster = (id: string) => {
    const found = disasters.find((d) => d.id === id);
    if (found) setSelectedDisaster(found);
  };

  const escalateDisaster = (id: string) => {
    setDisasters((prev) =>
      prev.map((d) =>
        d.id === id
          ? {
              ...d,
              severity_level: 5,
              criticality: "DEFCON 1 • MAXIMUM ESCALATION",
            }
          : d
      )
    );
    if (selectedDisaster?.id === id) {
      setSelectedDisaster((prev) =>
        prev
          ? { ...prev, severity_level: 5, criticality: "DEFCON 1 • MAXIMUM ESCALATION" }
          : null
      );
    }
  };

  const resolveDisaster = (id: string) => {
    setDisasters((prev) =>
      prev.map((d) =>
        d.id === id
          ? {
              ...d,
              status: "RESOLVED",
              criticality: "STANDBY • RECOVERY",
            }
          : d
      )
    );
    if (selectedDisaster?.id === id) {
      setSelectedDisaster((prev) =>
        prev ? { ...prev, status: "RESOLVED", criticality: "STANDBY • RECOVERY" } : null
      );
    }
  };

  // Resource Assignment Actions
  const assignResourceToIncident = (unitId: string, incidentId: string, taskDescription?: string) => {
    const targetIncident = disasters.find((d) => d.id === incidentId);
    setResources((prev) =>
      prev.map((r) =>
        r.id === unitId
          ? {
              ...r,
              status: "ASSIGNED",
              assigned_incident_id: incidentId,
              assigned_incident_name: targetIncident?.name || "Assam Flood Sector East",
              current_task: taskDescription || `Dispatched to incident ${incidentId}`,
            }
          : r
      )
    );

    // Update EOC counters
    setOperationsStatus((prev) => ({
      ...prev,
      available_response_units: Math.max(0, prev.available_response_units - 1),
      allocated_response_units: prev.allocated_response_units + 1,
    }));
  };

  const releaseResource = (unitId: string) => {
    setResources((prev) =>
      prev.map((r) =>
        r.id === unitId
          ? {
              ...r,
              status: "AVAILABLE",
              assigned_incident_id: undefined,
              assigned_incident_name: undefined,
              current_task: "Standby at depot depot.",
            }
          : r
      )
    );

    setOperationsStatus((prev) => ({
      ...prev,
      available_response_units: prev.available_response_units + 1,
      allocated_response_units: Math.max(0, prev.allocated_response_units - 1),
    }));
  };

  const selectRiskHex = (hexId: string) => {
    const found = riskZones.find((h) => h.hex_id === hexId);
    if (found) setSelectedHex(found);
  };

  return (
    <EOCContext.Provider
      value={{
        connectionStatus,
        lastUpdated,
        secondsSinceSync,
        isRefreshing,
        refreshAll,
        operationsStatus,
        disasters,
        selectedDisaster,
        selectDisaster,
        escalateDisaster,
        resolveDisaster,
        alerts,
        acknowledgeAlert,
        resolveAlert,
        resources,
        assignResourceToIncident,
        releaseResource,
        riskZones,
        selectedHex,
        selectRiskHex,
        liveEvents,
      }}
    >
      {children}
    </EOCContext.Provider>
  );
};

export const useEOC = (): EOCContextType => {
  const context = useContext(EOCContext);
  if (!context) {
    throw new Error("useEOC must be used within an EOCProvider");
  }
  return context;
};
