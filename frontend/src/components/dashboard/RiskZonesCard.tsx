import React from "react";
import { AlertTriangle, Layers, ShieldAlert } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { formatNumber } from "@/lib/utils";
import { RiskSummary } from "@/types/risk";

interface RiskZonesCardProps {
  riskSummary: RiskSummary;
}

export const RiskZonesCard: React.FC<RiskZonesCardProps> = ({ riskSummary }) => {
  const totalZones =
    riskSummary.critical_zones_count +
    riskSummary.high_zones_count +
    riskSummary.moderate_zones_count +
    riskSummary.low_zones_count;

  const tiers = [
    {
      label: "Critical Risk (≥ 0.75)",
      count: riskSummary.critical_zones_count,
      color: "bg-rose-500",
      textColor: "text-rose-600 dark:text-rose-400",
      percent: Math.round((riskSummary.critical_zones_count / totalZones) * 100),
    },
    {
      label: "High Risk (0.50 - 0.74)",
      count: riskSummary.high_zones_count,
      color: "bg-orange-500",
      textColor: "text-orange-600 dark:text-orange-400",
      percent: Math.round((riskSummary.high_zones_count / totalZones) * 100),
    },
    {
      label: "Moderate Risk (0.25 - 0.49)",
      count: riskSummary.moderate_zones_count,
      color: "bg-yellow-500",
      textColor: "text-yellow-600 dark:text-yellow-400",
      percent: Math.round((riskSummary.moderate_zones_count / totalZones) * 100),
    },
    {
      label: "Low Risk (< 0.25)",
      count: riskSummary.low_zones_count,
      color: "bg-emerald-500",
      textColor: "text-emerald-600 dark:text-emerald-400",
      percent: Math.round((riskSummary.low_zones_count / totalZones) * 100),
    },
  ];

  return (
    <Card>
      <CardHeader
        title="MCDA Risk & Vulnerability Index"
        subtitle="UNDRR formulation: (Hazard × Exposure × Vuln) / Capacity"
        badge={
          <Badge variant="warning" size="sm">
            {totalZones} H3 Hexagons
          </Badge>
        }
      />

      {/* Progress Bar Stack */}
      <div className="h-2.5 w-full rounded-full bg-surface-200 flex overflow-hidden gap-0.5 mb-4">
        {tiers.map((tier, idx) => (
          <div
            key={idx}
            className={`${tier.color} transition-all duration-300`}
            style={{ width: `${tier.percent}%` }}
            title={`${tier.label}: ${tier.count} cells`}
          />
        ))}
      </div>

      {/* Tier Breakdown Rows */}
      <div className="grid grid-cols-2 gap-2.5">
        {tiers.map((tier, idx) => (
          <div
            key={idx}
            className="p-2.5 rounded-lg bg-surface-200 border border-surface-border flex flex-col justify-between"
          >
            <div className="flex items-center gap-1.5 text-xs text-slate-600 dark:text-slate-400">
              <span className={`w-2 h-2 rounded-full ${tier.color}`} />
              <span className="truncate">{tier.label.split(" ")[0]}</span>
            </div>
            <div className="mt-1 flex items-baseline justify-between">
              <span className={`text-base font-bold font-mono ${tier.textColor}`}>
                {tier.count}
              </span>
              <span className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                {tier.percent}%
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Top Critical Hexagon Callout */}
      <div className="mt-4 p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-xs">
        <div className="flex items-center justify-between text-rose-600 dark:text-rose-400 font-semibold mb-1">
          <span className="flex items-center gap-1">
            <ShieldAlert className="w-3.5 h-3.5" />
            Top Vulnerable Sector: Ward 4 & 7
          </span>
          <span className="font-mono">Score: 0.91</span>
        </div>
        <p className="text-slate-700 dark:text-slate-300 text-[11px] leading-relaxed">
          Inundation depth 1.25m • Cut off by Bridge B-12 • 18,450 residents require immediate boat evacuation.
        </p>
      </div>
    </Card>
  );
};
