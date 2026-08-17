"use client";

import React from "react";
import Link from "next/link";
import {
  Compass,
  Download,
  Flame,
  Layers,
  MapPin,
  Play,
  Radio,
  RefreshCw,
  ShieldAlert,
  Truck,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { CommandCenterOverview } from "@/components/dashboard/CommandCenterOverview";
import { LiveAlertsCard } from "@/components/dashboard/LiveAlertsCard";
import { LiveEventsFeed } from "@/components/dashboard/LiveEventsFeed";
import { ResponsePlanCard } from "@/components/dashboard/ResponsePlanCard";
import { AIIntelligenceCard } from "@/components/dashboard/AIIntelligenceCard";
import { MapPlaceholder } from "@/components/dashboard/MapPlaceholder";
import { DisasterOverviewCard } from "@/components/dashboard/DisasterOverviewCard";
import { RiskZonesCard } from "@/components/dashboard/RiskZonesCard";
import { ResourcesCard } from "@/components/dashboard/ResourcesCard";
import { HealthStatusCard } from "@/components/dashboard/HealthStatusCard";
import { useEOC } from "@/context/EOCContext";

export default function DashboardPage() {
  const {
    operationsStatus,
    alerts,
    liveEvents,
    refreshAll,
    isRefreshing,
  } = useEOC();

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner / Operational Command Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-gradient-to-r from-surface-100 via-surface-200 to-surface-100 border border-surface-border shadow-xl">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse" />
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-slate-100 dark:text-slate-100 light:text-slate-900">
              Emergency Operations Center (EOC) Command
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Active Multi-Hazard Incident: <span className="text-cyan-400 font-semibold">Assam Brahmaputra Basin Inundation</span> • Real-Time Spatial Fusion
          </p>
        </div>

        {/* Operational Action Buttons */}
        <div className="flex items-center gap-2.5 flex-wrap">
          <Button
            size="sm"
            variant="secondary"
            onClick={() => refreshAll()}
            disabled={isRefreshing}
            icon={<RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin" : ""}`} />}
          >
            Sync Telemetry
          </Button>
          <Link href="/disasters">
            <Button size="sm" variant="secondary" icon={<Flame className="w-3.5 h-3.5 text-rose-400" />}>
              Active Hazards
            </Button>
          </Link>
          <Link href="/milp">
            <Button size="sm" variant="primary" icon={<Compass className="w-3.5 h-3.5" />}>
              1-Click Optimize Dispatch
            </Button>
          </Link>
        </div>
      </div>

      {/* Real-Time Operational Overview & Telemetry Strip (Synchronized EOC Context) */}
      <CommandCenterOverview initialStatus={operationsStatus} />

      {/* Main Tactical Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Primary Column: GIS Map, Tactical Alerts, Dispatch Plan, AI Decision Support (8 Cols) */}
        <div className="lg:col-span-8 space-y-6">
          {/* GIS Map Viewport */}
          <MapPlaceholder />

          {/* Real-Time Tactical Alerts Card */}
          <LiveAlertsCard initialAlerts={alerts} />

          {/* Active Disasters Overview */}
          <DisasterOverviewCard
            disasters={[
              {
                id: "dis-assam-01",
                name: "Assam Brahmaputra Basin Inundation",
                disaster_type: "FLOOD",
                severity_level: 4,
                status: "ACTIVE",
                latitude: 26.3216,
                longitude: 91.0063,
                affected_population_estimate: 85400,
                created_at: "2026-08-16T14:30:00Z",
                updated_at: "2026-08-17T08:00:00Z",
              },
              {
                id: "dis-chennai-02",
                name: "Chennai Coastal Storm Surge Alert",
                disaster_type: "CYCLONE",
                severity_level: 3,
                status: "ACTIVE",
                latitude: 13.0827,
                longitude: 80.2707,
                affected_population_estimate: 32000,
                created_at: "2026-08-17T06:15:00Z",
                updated_at: "2026-08-17T08:00:00Z",
              },
            ]}
          />
        </div>

        {/* Right Secondary Column: Live Telemetry Stream, MCDA Risk, Fleet, Health (4 Cols) */}
        <div className="lg:col-span-4 space-y-6">
          {/* Live Operational Events Telemetry Stream */}
          <LiveEventsFeed initialEvents={liveEvents} />

          {/* MCDA Risk & Vulnerability Index Card */}
          <RiskZonesCard
            riskSummary={{
              critical_zones_count: 2,
              high_zones_count: 1,
              moderate_zones_count: 1,
              low_zones_count: 0,
              total_exposed_population: 85400,
              top_risk_zones: [
                {
                  h3_index: "8860145b23fffff",
                  latitude: 26.3216,
                  longitude: 91.0063,
                  population_count: 48500,
                  mcda_breakdown: {
                    hazard_intensity_score: 0.95,
                    exposure_score: 0.92,
                    vulnerability_score: 0.90,
                    coping_capacity_score: 0.20,
                    composite_risk_score: 0.94,
                    risk_category: "CRITICAL",
                  },
                },
                {
                  h3_index: "8860145b27fffff",
                  latitude: 26.3180,
                  longitude: 91.0150,
                  population_count: 36900,
                  mcda_breakdown: {
                    hazard_intensity_score: 0.80,
                    exposure_score: 0.75,
                    vulnerability_score: 0.78,
                    coping_capacity_score: 0.35,
                    composite_risk_score: 0.78,
                    risk_category: "HIGH",
                  },
                },
              ],
            }}
          />

          {/* Emergency Response Fleet Status Card */}
          <ResourcesCard
            resourceSummary={{
              total_units: 32,
              available_units: operationsStatus.available_response_units,
              dispatched_units: operationsStatus.allocated_response_units,
              on_mission_units: 14,
              breakdown: {
                RESCUE_BOAT: { total: 10, available: 6 },
                AMBULANCE: { total: 8, available: 4 },
                NDRF_TEAM: { total: 6, available: 3 },
                MOBILE_GENERATOR: { total: 4, available: 2 },
                FOOD_WATER_TRUCK: { total: 4, available: 3 },
                SDRF_TEAM: { total: 0, available: 0 },
                DRONE_SURVEILLANCE: { total: 0, available: 0 },
              },
            }}
          />
        </div>
      </div>
    </div>
  );
}
