"use client";

import React from "react";
import {
  Activity,
  AlertOctagon,
  Flame,
  Radio,
  Shield,
  ShieldAlert,
  Truck,
  Wifi,
  WifiOff,
} from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { useRealtimeOperations } from "@/hooks/useRealtimeOperations";
import { OperationsStatus } from "@/types/realtime";

interface CommandCenterOverviewProps {
  initialStatus: OperationsStatus;
}

export const CommandCenterOverview: React.FC<CommandCenterOverviewProps> = ({ initialStatus }) => {
  const { status: wsStatus } = useRealtimeOperations();

  const isLive = wsStatus === "CONNECTED";

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      {/* 1. Active Incidents */}
      <div className="p-3.5 rounded-xl bg-surface-100 border border-surface-border flex flex-col justify-between shadow-md">
        <div className="flex items-center justify-between text-slate-500 dark:text-slate-400">
          <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">Active Hazards</span>
          <Flame className="w-4 h-4 text-amber-500" />
        </div>
        <div className="mt-2">
          <div className="text-2xl font-bold font-mono text-foreground">
            {initialStatus.active_incidents}
          </div>
          <span className="text-[10px] text-amber-600 dark:text-amber-400 font-mono">Assam Basin Active</span>
        </div>
      </div>

      {/* 2. Critical Incidents */}
      <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 flex flex-col justify-between shadow-md">
        <div className="flex items-center justify-between text-rose-600 dark:text-rose-400">
          <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">Critical Incidents</span>
          <AlertOctagon className="w-4 h-4 text-rose-500 animate-pulse" />
        </div>
        <div className="mt-2">
          <div className="text-2xl font-bold font-mono text-rose-600 dark:text-rose-300">
            {initialStatus.critical_incidents}
          </div>
          <span className="text-[10px] text-rose-600 dark:text-rose-400 font-mono">DEFCON 1 Flash Flood</span>
        </div>
      </div>

      {/* 3. Tactical Alerts */}
      <div className="p-3.5 rounded-xl bg-surface-100 border border-surface-border flex flex-col justify-between shadow-md">
        <div className="flex items-center justify-between text-slate-500 dark:text-slate-400">
          <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">Active Alerts</span>
          <ShieldAlert className="w-4 h-4 text-rose-500" />
        </div>
        <div className="mt-2">
          <div className="text-2xl font-bold font-mono text-foreground">
            {initialStatus.active_alerts}
          </div>
          <span className="text-[10px] text-rose-600 dark:text-rose-400 font-mono">
            {initialStatus.critical_alerts} Critical Alerts
          </span>
        </div>
      </div>

      {/* 4. Response Fleet Readiness */}
      <div className="p-3.5 rounded-xl bg-surface-100 border border-surface-border flex flex-col justify-between shadow-md">
        <div className="flex items-center justify-between text-slate-500 dark:text-slate-400">
          <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">Fleet Available</span>
          <Truck className="w-4 h-4 text-emerald-500" />
        </div>
        <div className="mt-2">
          <div className="text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
            {initialStatus.available_response_units} / {initialStatus.total_response_units}
          </div>
          <span className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
            {initialStatus.allocated_response_units} Units Committed
          </span>
        </div>
      </div>

      {/* 5. Resource Shortages */}
      <div className="p-3.5 rounded-xl bg-surface-100 border border-surface-border flex flex-col justify-between shadow-md">
        <div className="flex items-center justify-between text-slate-500 dark:text-slate-400">
          <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">Unmet Demand</span>
          <Activity className="w-4 h-4 text-amber-500" />
        </div>
        <div className="mt-2">
          <div className="text-2xl font-bold font-mono text-amber-600 dark:text-amber-400">
            {initialStatus.resource_shortages}
          </div>
          <span className="text-[10px] text-amber-600 dark:text-amber-400 font-mono">Mutual Aid Triggered</span>
        </div>
      </div>

      {/* 6. Live Telemetry Stream Connection */}
      <div className="p-3.5 rounded-xl bg-surface-100 border border-surface-border flex flex-col justify-between shadow-md">
        <div className="flex items-center justify-between text-slate-500 dark:text-slate-400">
          <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">Telemetry Stream</span>
          {isLive ? (
            <Wifi className="w-4 h-4 text-emerald-500" />
          ) : (
            <WifiOff className="w-4 h-4 text-amber-500 animate-pulse" />
          )}
        </div>
        <div className="mt-2">
          <div className="flex items-center gap-2">
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                isLive ? "bg-emerald-500 animate-pulse" : "bg-amber-500"
              }`}
            />
            <span className="text-xs font-bold font-mono text-foreground">
              {isLive ? "LIVE SYNC" : "RECONNECTING"}
            </span>
          </div>
          <span className="text-[10px] text-slate-500 dark:text-slate-400 font-mono mt-0.5 block">
            WebSocket WS/1.1
          </span>
        </div>
      </div>
    </div>
  );
};
