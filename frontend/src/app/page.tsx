import React from "react";
import {
  Compass,
  Download,
  Flame,
  Play,
  Radio,
  RefreshCw,
  ShieldAlert,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { MetricsGrid } from "@/components/dashboard/MetricsGrid";
import { MapPlaceholder } from "@/components/dashboard/MapPlaceholder";
import { DisasterOverviewCard } from "@/components/dashboard/DisasterOverviewCard";
import { RiskZonesCard } from "@/components/dashboard/RiskZonesCard";
import { ResourcesCard } from "@/components/dashboard/ResourcesCard";
import { HealthStatusCard } from "@/components/dashboard/HealthStatusCard";
import { RecentActivityCard } from "@/components/dashboard/RecentActivityCard";
import { fetchDashboardData } from "@/services/dashboardService";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const data = await fetchDashboardData();

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner / Operational Command Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-gradient-to-r from-surface-100 via-surface-200 to-surface-100 border border-surface-border shadow-xl">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse" />
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-slate-100">
              Emergency Operations Center (EOC) Command
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Active Multi-Hazard Incident: <span className="text-cyan-400 font-semibold">Assam Brahmaputra Basin Inundation</span> • Real-time Spatial Fusion
          </p>
        </div>

        {/* Operational Action Buttons */}
        <div className="flex items-center gap-2.5 flex-wrap">
          <Button
            size="sm"
            variant="secondary"
            icon={<RefreshCw className="w-3.5 h-3.5" />}
          >
            Sync Telemetry
          </Button>
          <Button
            size="sm"
            variant="secondary"
            icon={<Download className="w-3.5 h-3.5" />}
          >
            Export Brief
          </Button>
          <Button
            size="sm"
            variant="primary"
            icon={<Compass className="w-3.5 h-3.5" />}
          >
            1-Click Optimize Dispatch
          </Button>
        </div>
      </div>

      {/* KPI Overview Metrics */}
      <MetricsGrid metrics={data.metrics} />

      {/* Main Tactical Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Primary Column: GIS Map, Disasters, and Live Feed (8 Cols) */}
        <div className="lg:col-span-8 space-y-6">
          {/* GIS Map Viewport Placeholder */}
          <MapPlaceholder />

          {/* Active Disasters Overview */}
          <DisasterOverviewCard disasters={data.disasters} />

          {/* Live Activity & Distress Telemetry Log */}
          <RecentActivityCard activities={data.recentActivities} />
        </div>

        {/* Right Secondary Column: Risk Analysis, Resources Fleet, and Telemetry (4 Cols) */}
        <div className="lg:col-span-4 space-y-6">
          {/* MCDA Risk & Vulnerability Index Card */}
          <RiskZonesCard riskSummary={data.riskSummary} />

          {/* Emergency Response Fleet Status Card */}
          <ResourcesCard resourceSummary={data.resourceSummary} />

          {/* Subsystem Health & Readiness Card */}
          <HealthStatusCard health={data.health} />
        </div>
      </div>
    </div>
  );
}
