"use client";

import React, { useState } from "react";
import {
  AlertCircle,
  AlertTriangle,
  Anchor,
  CheckCircle2,
  ChevronRight,
  Clock,
  Compass,
  FileCheck,
  ListOrdered,
  Radio,
  RefreshCw,
  Shield,
  ShieldAlert,
  Truck,
  Zap,
} from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { ResponsePlanResponse } from "@/types/optimization";

interface ResponsePlanCardProps {
  initialPlan: ResponsePlanResponse;
}

export const ResponsePlanCard: React.FC<ResponsePlanCardProps> = ({ initialPlan }) => {
  const [activeTab, setActiveTab] = useState<"sequence" | "shortages" | "warnings">("sequence");
  const [isSolving, setIsSolving] = useState(false);

  const handleResolve = () => {
    setIsSolving(true);
    setTimeout(() => setIsSolving(false), 900);
  };

  const getPriorityBadge = (tier: string) => {
    switch (tier) {
      case "CRITICAL":
        return <Badge variant="critical" size="sm" dot>CRITICAL</Badge>;
      case "HIGH":
        return <Badge variant="warning" size="sm" dot>HIGH</Badge>;
      case "MEDIUM":
        return <Badge variant="info" size="sm">MEDIUM</Badge>;
      default:
        return <Badge variant="default" size="sm">LOW</Badge>;
    }
  };

  const getUnitIcon = (unitType: string) => {
    switch (unitType) {
      case "RESCUE_BOAT":
        return <Anchor className="w-4 h-4 text-cyan-400" />;
      case "AMBULANCE":
        return <Truck className="w-4 h-4 text-rose-400" />;
      case "FOOD_WATER_TRUCK":
        return <Zap className="w-4 h-4 text-amber-400" />;
      default:
        return <Shield className="w-4 h-4 text-emerald-400" />;
    }
  };

  return (
    <Card className="border-emerald-500/30 bg-gradient-to-b from-surface-200/90 to-surface-100/90 shadow-xl">
      {/* Header with Plan ID and Re-Solve button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-surface-border gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500/20 to-cyan-600/30 border border-emerald-500/40 flex items-center justify-center text-emerald-400 shrink-0">
            <Compass className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-base font-bold text-slate-100 flex items-center gap-1.5">
                Emergency Response Plan & Dispatch Engine
              </h3>
              <Badge variant="success" size="sm">
                <FileCheck className="w-3 h-3" />
                {initialPlan.plan_id}
              </Badge>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Deterministic MILP allocation with terrain-modeled travel times & shortage tracking
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <Button
            size="sm"
            variant="primary"
            onClick={handleResolve}
            disabled={isSolving}
            icon={<RefreshCw className={`w-3.5 h-3.5 ${isSolving ? "animate-spin" : ""}`} />}
          >
            {isSolving ? "Solving MILP..." : "Re-Solve Dispatch Plan"}
          </Button>
        </div>
      </div>

      {/* Plan KPI Summary Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 my-4">
        <div className="p-3 rounded-xl bg-surface-100/80 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Total Incidents</span>
          <div className="text-xl font-bold font-mono text-slate-100 mt-0.5">
            {initialPlan.plan_summary.total_incidents}
          </div>
          <span className="text-[10px] text-rose-400 font-mono">
            {initialPlan.plan_summary.critical_incidents_count} Critical Priority
          </span>
        </div>

        <div className="p-3 rounded-xl bg-surface-100/80 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Units Allocated</span>
          <div className="text-xl font-bold font-mono text-emerald-400 mt-0.5">
            {initialPlan.plan_summary.total_units_allocated} Units
          </div>
          <span className="text-[10px] text-slate-500 font-mono">Ordered by Priority</span>
        </div>

        <div className="p-3 rounded-xl bg-surface-100/80 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Supply Shortages</span>
          <div className="text-xl font-bold font-mono text-amber-400 mt-0.5">
            {initialPlan.plan_summary.total_shortages_count}
          </div>
          <span className="text-[10px] text-amber-400 font-mono">Mutual Aid Triggered</span>
        </div>

        <div className="p-3 rounded-xl bg-surface-100/80 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Avg Deployment ETA</span>
          <div className="text-xl font-bold font-mono text-cyan-400 mt-0.5">
            {initialPlan.plan_summary.average_deployment_eta_mins} mins
          </div>
          <span className="text-[10px] text-slate-500 font-mono">Terrain-Modeled</span>
        </div>
      </div>

      {/* Interactive Tabs */}
      <div className="flex items-center gap-2 pb-2 border-b border-surface-border/60 overflow-x-auto">
        <button
          onClick={() => setActiveTab("sequence")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all shrink-0 ${
            activeTab === "sequence"
              ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
              : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
          }`}
        >
          <ListOrdered className="w-3.5 h-3.5" />
          <span>1. Deployment Sequence ({initialPlan.deployment_sequence.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("shortages")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all shrink-0 ${
            activeTab === "shortages"
              ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
              : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
          }`}
        >
          <AlertCircle className="w-3.5 h-3.5" />
          <span>2. Supply Shortages ({initialPlan.unresolved_shortages.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("warnings")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all shrink-0 ${
            activeTab === "warnings"
              ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
              : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
          }`}
        >
          <ShieldAlert className="w-3.5 h-3.5" />
          <span>3. Operational Warnings ({initialPlan.operational_warnings.length})</span>
        </button>
      </div>

      {/* Tab 1: Deployment Sequence View */}
      {activeTab === "sequence" && (
        <div className="mt-4 space-y-3">
          <div className="space-y-2.5">
            {initialPlan.deployment_sequence.map((order) => (
              <div
                key={order.deployment_order}
                className="p-3.5 rounded-xl bg-surface-100/70 border border-surface-border hover:border-slate-700 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center font-mono font-bold text-sm text-emerald-400 shrink-0">
                    #{order.deployment_order}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <div className="flex items-center gap-1.5">
                        {getUnitIcon(order.resource_type)}
                        <span className="text-sm font-semibold text-slate-100">
                          {order.resource_name}
                        </span>
                      </div>
                      {getPriorityBadge(order.priority_level)}
                      <span className="text-[10px] font-mono text-slate-500">[{order.resource_code}]</span>
                    </div>
                    <p className="text-xs text-slate-300 mt-1">
                      <span className="text-slate-500 font-mono">Assigned Target: </span>
                      <span className="text-cyan-300">{order.incident_name}</span>
                    </p>
                    <div className="mt-1 text-[11px] text-slate-400 font-mono">
                      ↳ Staging: {order.staging_point}
                    </div>
                  </div>
                </div>

                <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center border-t sm:border-t-0 pt-2 sm:pt-0 border-surface-border/40 shrink-0 text-xs font-mono">
                  <span className="text-slate-400">Estimated Transit:</span>
                  <span className="text-emerald-400 font-bold text-sm mt-0.5">
                    ~{order.estimated_eta_minutes} mins
                  </span>
                  <span className="text-[10px] text-slate-500">(Terrain-Modeled)</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 2: Supply Shortages View */}
      {activeTab === "shortages" && (
        <div className="mt-4 space-y-3">
          {initialPlan.unresolved_shortages.length === 0 ? (
            <div className="p-6 text-center text-slate-400 text-xs font-mono">
              <CheckCircle2 className="w-6 h-6 text-emerald-400 mx-auto mb-2" />
              All incident demand successfully fulfilled by committed local depot units.
            </div>
          ) : (
            initialPlan.unresolved_shortages.map((shortage, sIdx) => (
              <div
                key={sIdx}
                className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-2"
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
                    <span className="text-sm font-semibold text-amber-300">
                      Deficit: {shortage.shortage_count}x {shortage.resource_type}
                    </span>
                  </div>
                  <Badge variant="warning" size="sm">
                    {shortage.urgency}
                  </Badge>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {shortage.impact_explanation}
                </p>
                <div className="pt-2 border-t border-amber-500/20 text-[11px] text-amber-400 font-mono">
                  ↳ Recommended Action: {shortage.recommended_mitigation}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Tab 3: Operational Warnings View */}
      {activeTab === "warnings" && (
        <div className="mt-4 space-y-3">
          {initialPlan.operational_warnings.map((warn, wIdx) => (
            <div
              key={wIdx}
              className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-start gap-3"
            >
              <ShieldAlert className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold text-rose-300">{warn.title}</span>
                  <span className="text-[10px] font-mono text-slate-500">[{warn.warning_code}]</span>
                </div>
                <p className="text-xs text-slate-300 mt-1 leading-relaxed">{warn.message}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Bottom Dispatch Disclaimer */}
      <div className="mt-4 pt-3 border-t border-surface-border/60 flex items-center gap-2 text-[10px] text-slate-500 font-mono">
        <Radio className="w-3 h-3 text-emerald-400 animate-pulse shrink-0" />
        <span className="truncate">{initialPlan.disclaimer}</span>
      </div>
    </Card>
  );
};
