import React from "react";
import { AlertCircle, ChevronRight, MapPin, Users } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { formatNumber, formatRelativeTime, getSeverityBadgeProps } from "@/lib/utils";
import { Disaster } from "@/types/disaster";

interface DisasterOverviewCardProps {
  disasters: Disaster[];
}

export const DisasterOverviewCard: React.FC<DisasterOverviewCardProps> = ({ disasters }) => {
  return (
    <Card>
      <CardHeader
        title="Active Disaster Incidents"
        subtitle="Real-time multi-hazard telemetry feeds"
        badge={
          <Badge variant="critical" size="sm" dot>
            {disasters.length} Active
          </Badge>
        }
      />

      <div className="space-y-3">
        {disasters.map((disaster) => {
          const badgeProps = getSeverityBadgeProps(disaster.severity_level);
          return (
            <div
              key={disaster.id}
              className="p-3.5 rounded-xl bg-surface-200 border border-surface-border hover:border-slate-400 dark:hover:border-slate-700 transition-colors"
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="text-sm font-semibold text-foreground">{disaster.name}</h4>
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border font-mono ${badgeProps.className}`}
                    >
                      {badgeProps.label}
                    </span>
                  </div>
                  {disaster.description && (
                    <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 line-clamp-2 leading-relaxed">
                      {disaster.description}
                    </p>
                  )}
                </div>
              </div>

              <div className="mt-3 pt-2.5 border-t border-surface-border flex flex-wrap items-center justify-between text-xs text-slate-500 dark:text-slate-400 gap-2 font-mono">
                <div className="flex items-center gap-3">
                  <span className="flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    {disaster.latitude.toFixed(4)}°, {disaster.longitude.toFixed(4)}°
                  </span>
                  {disaster.affected_population_estimate ? (
                    <span className="flex items-center gap-1 text-amber-600 dark:text-amber-400">
                      <Users className="w-3.5 h-3.5" />
                      {formatNumber(disaster.affected_population_estimate)} exposed
                    </span>
                  ) : null}
                </div>
                <span className="text-[10px] text-slate-400">
                  Updated {formatRelativeTime(disaster.updated_at)}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
