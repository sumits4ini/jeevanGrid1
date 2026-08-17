"use client";

import React, { useState } from "react";
import {
  AlertOctagon,
  AlertTriangle,
  CheckCircle2,
  ChevronRight,
  Clock,
  Eye,
  Info,
  Radio,
  RefreshCw,
  ShieldAlert,
  ShieldCheck,
  Zap,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { acknowledgeAlert, resolveAlert } from "@/services/realtimeService";
import { Alert, AlertSeverity, AlertStatus } from "@/types/realtime";

interface LiveAlertsCardProps {
  initialAlerts: Alert[];
}

export const LiveAlertsCard: React.FC<LiveAlertsCardProps> = ({ initialAlerts }) => {
  const [alerts, setAlerts] = useState<Alert[]>(initialAlerts);
  const [filterStatus, setFilterStatus] = useState<"ALL" | "ACTIVE" | "ACKNOWLEDGED" | "RESOLVED">("ALL");
  const [actionLoadingId, setActionLoadingId] = useState<string | null>(null);

  const handleAcknowledge = async (alertId: string) => {
    setActionLoadingId(alertId);
    try {
      const updated = await acknowledgeAlert(alertId, "EOC_COMMANDER", "Operations command acknowledged alert.");
      setAlerts((prev) => prev.map((a) => (a.alert_id === alertId ? updated : a)));
    } catch {
      // Fallback local update
      setAlerts((prev) =>
        prev.map((a) =>
          a.alert_id === alertId
            ? { ...a, status: "ACKNOWLEDGED" as AlertStatus, acknowledged_at: new Date().toISOString() }
            : a
        )
      );
    } finally {
      setActionLoadingId(null);
    }
  };

  const handleResolve = async (alertId: string) => {
    setActionLoadingId(alertId);
    try {
      const updated = await resolveAlert(
        alertId,
        "EOC_COMMANDER",
        "Field rescue unit deployed; hazard contained."
      );
      setAlerts((prev) => prev.map((a) => (a.alert_id === alertId ? updated : a)));
    } catch {
      setAlerts((prev) =>
        prev.map((a) =>
          a.alert_id === alertId
            ? { ...a, status: "RESOLVED" as AlertStatus, resolved_at: new Date().toISOString() }
            : a
        )
      );
    } finally {
      setActionLoadingId(null);
    }
  };

  const filteredAlerts = alerts.filter((a) => {
    if (filterStatus === "ALL") return true;
    return a.status === filterStatus;
  });

  const getSeverityBadge = (severity: AlertSeverity) => {
    switch (severity) {
      case "CRITICAL":
        return <Badge variant="critical" size="sm" dot>CRITICAL</Badge>;
      case "HIGH":
        return <Badge variant="warning" size="sm" dot>HIGH</Badge>;
      case "WARNING":
        return <Badge variant="warning" size="sm">WARNING</Badge>;
      default:
        return <Badge variant="info" size="sm">INFO</Badge>;
    }
  };

  const getStatusBadge = (status: AlertStatus) => {
    switch (status) {
      case "ACTIVE":
        return <Badge variant="critical" size="sm">ACTIVE</Badge>;
      case "ACKNOWLEDGED":
        return <Badge variant="warning" size="sm">ACKNOWLEDGED</Badge>;
      case "RESOLVED":
        return <Badge variant="success" size="sm">RESOLVED</Badge>;
      default:
        return <Badge variant="default" size="sm">DISMISSED</Badge>;
    }
  };

  return (
    <Card className="border-rose-500/30 bg-gradient-to-b from-surface-200/90 to-surface-100/90 shadow-xl">
      {/* Header with Title and Filter Tabs */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-surface-border gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-rose-500/20 to-red-600/30 border border-rose-500/40 flex items-center justify-center text-rose-400 shrink-0">
            <ShieldAlert className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-base font-bold text-slate-100 flex items-center gap-1.5">
                Tactical Alerts & Hazard Anomalies
              </h3>
              <Badge variant="critical" size="sm">
                {alerts.filter((a) => a.status === "ACTIVE").length} Active
              </Badge>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Live automated multi-source hazard alerts with sliding-window deduplication
            </p>
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1 bg-surface-100 p-1 rounded-lg border border-surface-border shrink-0">
          {(["ALL", "ACTIVE", "ACKNOWLEDGED", "RESOLVED"] as const).map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-2.5 py-1 rounded text-[11px] font-mono font-semibold transition-all ${
                filterStatus === st
                  ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {/* Alert List */}
      <div className="mt-4 space-y-3">
        {filteredAlerts.length === 0 ? (
          <div className="p-8 text-center text-slate-400 text-xs font-mono">
            <ShieldCheck className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
            No alerts found under status filter: {filterStatus}.
          </div>
        ) : (
          filteredAlerts.map((alert) => (
            <div
              key={alert.alert_id}
              className={`p-4 rounded-xl border transition-all ${
                alert.status === "ACTIVE"
                  ? "bg-rose-500/10 border-rose-500/30"
                  : alert.status === "ACKNOWLEDGED"
                  ? "bg-amber-500/10 border-amber-500/30"
                  : "bg-surface-100/70 border-surface-border opacity-75"
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    {getSeverityBadge(alert.severity)}
                    {getStatusBadge(alert.status)}
                    <span className="text-sm font-semibold text-slate-100">
                      {alert.title}
                    </span>
                    {alert.occurrence_count > 1 && (
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                        {alert.occurrence_count}x Occurrences
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">{alert.message}</p>

                  {alert.recommended_action && (
                    <div className="p-2.5 rounded-lg bg-surface-200/80 border border-surface-border text-xs text-cyan-300 font-mono flex items-start gap-2">
                      <ChevronRight className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                      <span>
                        <strong className="text-slate-400">Directive: </strong>
                        {alert.recommended_action}
                      </span>
                    </div>
                  )}
                </div>

                {/* Action Controls */}
                <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-start gap-2 shrink-0 border-t sm:border-t-0 pt-2 sm:pt-0 border-surface-border/40">
                  <span className="text-[10px] text-slate-500 font-mono">
                    {alert.alert_code}
                  </span>

                  {alert.status === "ACTIVE" && (
                    <div className="flex items-center gap-1.5">
                      <Button
                        size="sm"
                        variant="secondary"
                        disabled={actionLoadingId === alert.alert_id}
                        onClick={() => handleAcknowledge(alert.alert_id)}
                      >
                        Acknowledge
                      </Button>
                      <Button
                        size="sm"
                        variant="primary"
                        disabled={actionLoadingId === alert.alert_id}
                        onClick={() => handleResolve(alert.alert_id)}
                      >
                        Resolve
                      </Button>
                    </div>
                  )}

                  {alert.status === "ACKNOWLEDGED" && (
                    <Button
                      size="sm"
                      variant="primary"
                      disabled={actionLoadingId === alert.alert_id}
                      onClick={() => handleResolve(alert.alert_id)}
                    >
                      Resolve Alert
                    </Button>
                  )}

                  {alert.status === "RESOLVED" && (
                    <span className="text-[10px] text-emerald-400 font-mono flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> Resolved
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Footer Advisory */}
      <div className="mt-4 pt-3 border-t border-surface-border/60 flex items-center gap-2 text-[10px] text-slate-500 font-mono">
        <Radio className="w-3 h-3 text-rose-400 animate-pulse shrink-0" />
        <span>
          Real-time incident anomalies are deduplicated automatically in a 300-second sliding window.
        </span>
      </div>
    </Card>
  );
};
