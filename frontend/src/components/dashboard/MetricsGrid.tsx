import React from "react";
import { AlertOctagon, Flame, ShieldCheck, Users, Waves, Zap } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { formatNumber } from "@/lib/utils";
import { DashboardKPIMetrics } from "@/types/dashboard";

interface MetricsGridProps {
  metrics: DashboardKPIMetrics;
}

export const MetricsGrid: React.FC<MetricsGridProps> = ({ metrics }) => {
  const cards = [
    {
      title: "Active Disasters",
      value: metrics.activeDisastersCount,
      subtext: "1 Flood • 1 Storm Surge",
      icon: Waves,
      iconColor: "text-cyan-500 dark:text-cyan-400",
      iconBg: "bg-cyan-500/10 border-cyan-500/20",
      badge: "LIVE TRACKING",
      badgeColor: "text-cyan-600 dark:text-cyan-400 bg-cyan-500/10",
    },
    {
      title: "Critical Risk Hexagons",
      value: metrics.criticalRiskZonesCount,
      subtext: "MCDA Score ≥ 0.75 (H3 Res-8)",
      icon: AlertOctagon,
      iconColor: "text-rose-500 dark:text-rose-400",
      iconBg: "bg-rose-500/10 border-rose-500/20",
      badge: "ACTION REQUIRED",
      badgeColor: "text-rose-600 dark:text-rose-400 bg-rose-500/10",
    },
    {
      title: "Exposed Population",
      value: formatNumber(metrics.totalExposedPopulation),
      subtext: "Across 6 inundation wards",
      icon: Users,
      iconColor: "text-amber-500 dark:text-amber-400",
      iconBg: "bg-amber-500/10 border-amber-500/20",
      badge: "HIGH VULNERABILITY",
      badgeColor: "text-amber-600 dark:text-amber-400 bg-amber-500/10",
    },
    {
      title: "Available Response Units",
      value: `${metrics.availableRescueUnits} / ${metrics.totalRescueUnits}`,
      subtext: "10 Boats • 4 Ambulances ready",
      icon: ShieldCheck,
      iconColor: "text-emerald-500 dark:text-emerald-400",
      iconBg: "bg-emerald-500/10 border-emerald-500/20",
      badge: "READY FOR DISPATCH",
      badgeColor: "text-emerald-600 dark:text-emerald-400 bg-emerald-500/10",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <Card
            key={idx}
            className="hover:border-slate-400 dark:hover:border-slate-700 hover:shadow-md transition-all duration-200"
          >
            <div className="flex items-start justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 font-mono">
                {card.title}
              </span>
              <div
                className={`w-9 h-9 rounded-lg border flex items-center justify-center ${card.iconBg}`}
              >
                <Icon className={`w-4 h-4 ${card.iconColor}`} />
              </div>
            </div>

            <div className="mt-3">
              <div className="text-2xl font-bold font-mono tracking-tight text-foreground">
                {card.value}
              </div>
              <div className="flex items-center justify-between mt-2 pt-2 border-t border-surface-border">
                <span className="text-xs text-slate-500 dark:text-slate-400 truncate">{card.subtext}</span>
                <span
                  className={`text-[10px] font-semibold px-2 py-0.5 rounded-full font-mono shrink-0 ${card.badgeColor}`}
                >
                  {card.badge}
                </span>
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
};
