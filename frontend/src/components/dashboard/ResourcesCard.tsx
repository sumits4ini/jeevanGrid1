import React from "react";
import { Anchor, Shield, Truck, Zap } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { ResourceReadinessSummary } from "@/types/resource";

interface ResourcesCardProps {
  resourceSummary: ResourceReadinessSummary;
}

export const ResourcesCard: React.FC<ResourcesCardProps> = ({ resourceSummary }) => {
  const assets = [
    {
      label: "Motorized Rescue Boats",
      available: resourceSummary.breakdown.RESCUE_BOAT.available,
      total: resourceSummary.breakdown.RESCUE_BOAT.total,
      icon: Anchor,
      color: "text-cyan-400",
    },
    {
      label: "ALS Ambulances (Ground)",
      available: resourceSummary.breakdown.AMBULANCE.available,
      total: resourceSummary.breakdown.AMBULANCE.total,
      icon: Truck,
      color: "text-rose-400",
    },
    {
      label: "NDRF Rescue Battalions",
      available: resourceSummary.breakdown.NDRF_TEAM.available,
      total: resourceSummary.breakdown.NDRF_TEAM.total,
      icon: Shield,
      color: "text-emerald-400",
    },
    {
      label: "Food & Water Logistics",
      available: resourceSummary.breakdown.FOOD_WATER_TRUCK.available,
      total: resourceSummary.breakdown.FOOD_WATER_TRUCK.total,
      icon: Zap,
      color: "text-amber-400",
    },
  ];

  return (
    <Card>
      <CardHeader
        title="Emergency Response Fleet"
        subtitle="Live depot status & deployment capacity"
        badge={
          <Badge variant="success" size="sm" dot>
            {resourceSummary.available_units} Ready
          </Badge>
        }
      />

      <div className="space-y-2.5">
        {assets.map((asset, idx) => {
          const Icon = asset.icon;
          const percent = Math.round((asset.available / asset.total) * 100);
          return (
            <div
              key={idx}
              className="p-2.5 rounded-lg bg-surface-100/60 border border-surface-border"
            >
              <div className="flex items-center justify-between mb-1.5 text-xs">
                <div className="flex items-center gap-2">
                  <Icon className={`w-3.5 h-3.5 ${asset.color}`} />
                  <span className="font-medium text-slate-200">{asset.label}</span>
                </div>
                <div className="font-mono text-slate-300">
                  <span className="text-emerald-400 font-bold">{asset.available}</span>
                  <span className="text-slate-500"> / {asset.total}</span>
                </div>
              </div>

              {/* Mini progress track */}
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-500 rounded-full transition-all duration-300"
                  style={{ width: `${percent}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
