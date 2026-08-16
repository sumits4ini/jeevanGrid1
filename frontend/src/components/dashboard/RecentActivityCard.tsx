import React from "react";
import { Activity, AlertCircle, CheckCircle2, Info, Radio } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { formatRelativeTime } from "@/lib/utils";
import { ActivityLogItem, ActivitySeverity } from "@/types/dashboard";

interface RecentActivityCardProps {
  activities: ActivityLogItem[];
}

export const RecentActivityCard: React.FC<RecentActivityCardProps> = ({ activities }) => {
  const getSeverityIcon = (sev: ActivitySeverity) => {
    switch (sev) {
      case "CRITICAL":
        return <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />;
      case "WARNING":
        return <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />;
      case "SUCCESS":
        return <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />;
      default:
        return <Info className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />;
    }
  };

  return (
    <Card>
      <CardHeader
        title="Live Incident & Distress Feed"
        subtitle="Real-time multi-source event telemetry log"
        badge={
          <Badge variant="brand" size="sm" dot>
            STREAMING
          </Badge>
        }
      />

      <div className="space-y-3">
        {activities.map((act) => (
          <div
            key={act.id}
            className="p-3 rounded-lg bg-surface-100/60 border border-surface-border flex items-start gap-3"
          >
            {getSeverityIcon(act.severity)}
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2">
                <h5 className="text-xs font-semibold text-slate-200 truncate">{act.title}</h5>
                <span className="text-[10px] text-slate-500 font-mono shrink-0">
                  {formatRelativeTime(act.timestamp)}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">{act.description}</p>
              <div className="mt-2 flex items-center gap-2 text-[10px] font-mono text-slate-500">
                <span className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-400">
                  {act.source}
                </span>
                {act.targetLocation && (
                  <span className="text-cyan-400/80">• {act.targetLocation}</span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
