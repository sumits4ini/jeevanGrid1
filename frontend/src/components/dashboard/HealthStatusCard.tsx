import React from "react";
import { Activity, CheckCircle2, Cpu, Database, Server } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { StatusIndicator, StatusType } from "@/components/ui/StatusIndicator";
import { HealthResponse } from "@/types/health";

interface HealthStatusCardProps {
  health: HealthResponse;
}

export const HealthStatusCard: React.FC<HealthStatusCardProps> = ({ health }) => {
  const serviceList = [
    {
      name: "FastAPI Application Gateway",
      serviceKey: "api_gateway",
      icon: Server,
    },
    {
      name: "PostgreSQL & PostGIS Database",
      serviceKey: "database",
      icon: Database,
    },
    {
      name: "GIS Spatial Analytics Engine",
      serviceKey: "gis_engine",
      icon: Cpu,
    },
    {
      name: "MILP Operations Optimizer",
      serviceKey: "optimizer",
      icon: Activity,
    },
  ];

  return (
    <Card>
      <CardHeader
        title="Subsystem Telemetry"
        subtitle={`App: ${health.app_name} (v${health.app_version})`}
        badge={
          <StatusIndicator
            status={health.status as StatusType}
            label={health.status.toUpperCase()}
          />
        }
      />

      <div className="space-y-2.5">
        {serviceList.map((item, idx) => {
          const service = health.services[item.serviceKey] || {
            status: "offline",
            message: "Not initialized",
          };
          const Icon = item.icon;

          return (
            <div
              key={idx}
              className="p-2.5 rounded-lg bg-surface-200 border border-surface-border flex items-center justify-between text-xs"
            >
              <div className="flex items-center gap-2.5 min-w-0">
                <Icon className="w-4 h-4 text-slate-500 dark:text-slate-400 shrink-0" />
                <div className="truncate">
                  <p className="font-medium text-foreground truncate">{item.name}</p>
                  <p className="text-[10px] text-slate-500 dark:text-slate-400 font-mono truncate">
                    {service.message || "Ready"}
                  </p>
                </div>
              </div>

              <div className="shrink-0 pl-2">
                <StatusIndicator status={service.status as StatusType} />
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
