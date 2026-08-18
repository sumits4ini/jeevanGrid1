"use client";

import React, { useState } from "react";
import {
  AlertOctagon,
  Bot,
  CheckCircle,
  ChevronRight,
  Clock,
  Compass,
  FileText,
  ListOrdered,
  Radio,
  RefreshCw,
  ShieldAlert,
  Sparkles,
  Truck,
  Zap,
} from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import {
  RecommendationResponse,
  ResourcePrioritizationResponse,
  RiskAnalysisResponse,
} from "@/types/ai";

interface AIIntelligenceCardProps {
  initialRisk: RiskAnalysisResponse;
  initialResources: ResourcePrioritizationResponse;
  initialRecommendations: RecommendationResponse;
}

export const AIIntelligenceCard: React.FC<AIIntelligenceCardProps> = ({
  initialRisk,
  initialResources,
  initialRecommendations,
}) => {
  const [activeTab, setActiveTab] = useState<"risk" | "resources" | "recommendations">("risk");
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 800);
  };

  const getUrgencyBadge = (urgency: string) => {
    switch (urgency) {
      case "IMMEDIATE":
        return <Badge variant="critical" size="sm" dot>IMMEDIATE</Badge>;
      case "URGENT":
        return <Badge variant="warning" size="sm" dot>URGENT</Badge>;
      case "STANDARD":
        return <Badge variant="info" size="sm">STANDARD</Badge>;
      default:
        return <Badge variant="default" size="sm">STANDBY</Badge>;
    }
  };

  return (
    <Card className="border-cyan-500/30 bg-surface-100 shadow-xl">
      {/* Header with AI Engine status badge and recompute trigger */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-surface-border gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-600/30 border border-cyan-500/40 flex items-center justify-center text-cyan-500 dark:text-cyan-400 shrink-0">
            <Bot className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-base font-bold text-foreground flex items-center gap-1.5">
                AI Intelligence & Decision Support
              </h3>
              <Badge variant="brand" size="sm">
                <Sparkles className="w-3 h-3" />
                94% Confidence
              </Badge>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Multi-source geospatial reasoning & automated tactical decision matrix
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <Button
            size="sm"
            variant="secondary"
            onClick={handleRefresh}
            disabled={isRefreshing}
            icon={<RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin text-cyan-500 dark:text-cyan-400" : ""}`} />}
          >
            {isRefreshing ? "Recomputing..." : "Recompute Matrix"}
          </Button>
        </div>
      </div>

      {/* Interactive Tabs Navigation */}
      <div className="flex items-center gap-2 mt-4 pb-2 border-b border-surface-border overflow-x-auto">
        <button
          onClick={() => setActiveTab("risk")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all shrink-0 ${
            activeTab === "risk"
              ? "bg-cyan-500/20 text-cyan-700 dark:text-cyan-300 border border-cyan-500/40"
              : "text-slate-600 dark:text-slate-400 hover:text-foreground hover:bg-surface-200"
          }`}
        >
          <ShieldAlert className="w-3.5 h-3.5" />
          <span>1. Risk Intelligence</span>
        </button>

        <button
          onClick={() => setActiveTab("resources")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all shrink-0 ${
            activeTab === "resources"
              ? "bg-cyan-500/20 text-cyan-700 dark:text-cyan-300 border border-cyan-500/40"
              : "text-slate-600 dark:text-slate-400 hover:text-foreground hover:bg-surface-200"
          }`}
        >
          <ListOrdered className="w-3.5 h-3.5" />
          <span>2. Resource Prioritization ({initialResources.prioritized_resources.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("recommendations")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all shrink-0 ${
            activeTab === "recommendations"
              ? "bg-cyan-500/20 text-cyan-700 dark:text-cyan-300 border border-cyan-500/40"
              : "text-slate-600 dark:text-slate-400 hover:text-foreground hover:bg-surface-200"
          }`}
        >
          <FileText className="w-3.5 h-3.5" />
          <span>3. Command Advisories ({initialRecommendations.recommendations.length})</span>
        </button>
      </div>

      {/* Tab 1: AI Risk Intelligence View */}
      {activeTab === "risk" && (
        <div className="mt-4 space-y-4">
          {/* Top Score Banner */}
          <div className="p-4 rounded-xl bg-surface-200 border border-surface-border flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <span className="text-[10px] uppercase font-mono tracking-widest text-slate-500 dark:text-slate-400">
                Composite AI Risk Level
              </span>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-2xl font-bold font-mono text-rose-600 dark:text-rose-400">
                  {initialRisk.risk_score.toFixed(2)} / 1.00
                </span>
                <Badge variant="critical" size="md" dot>
                  {initialRisk.risk_level}
                </Badge>
                <span className="text-xs font-mono text-slate-500 dark:text-slate-400">
                  [{initialRisk.priority_level}]
                </span>
              </div>
              <p className="text-xs text-slate-700 dark:text-slate-300 mt-2 leading-relaxed">
                {initialRisk.affected_area_summary}
              </p>
            </div>

            {/* Resource Requirements Pill */}
            <div className="p-3 rounded-lg bg-surface-100 border border-surface-border text-xs shrink-0">
              <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400 uppercase">
                Estimated Minimum Assets:
              </span>
              <div className="grid grid-cols-2 gap-x-4 gap-y-1 mt-1.5 font-mono">
                <span className="text-cyan-600 dark:text-cyan-400">Boats: {initialRisk.resource_requirements.RESCUE_BOAT || 6}</span>
                <span className="text-rose-600 dark:text-rose-400">Ambulances: {initialRisk.resource_requirements.AMBULANCE || 4}</span>
                <span className="text-emerald-600 dark:text-emerald-400">NDRF Teams: {initialRisk.resource_requirements.NDRF_TEAM || 4}</span>
                <span className="text-amber-600 dark:text-amber-400">Power Units: {initialRisk.resource_requirements.MOBILE_GENERATOR || 2}</span>
              </div>
            </div>
          </div>

          {/* Risk Factors Breakdown */}
          <div>
            <h4 className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider font-mono mb-2.5">
              AI-Identified Hazard & Vulnerability Factors
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {initialRisk.risk_factors.map((factor, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-lg bg-surface-200 border border-surface-border flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-foreground">{factor.factor_name}</span>
                      <span className="text-rose-600 dark:text-rose-400 font-mono font-bold">
                        {factor.severity_score}
                      </span>
                    </div>
                    <div className="h-1.5 w-full bg-surface-100 rounded-full overflow-hidden my-2 border border-surface-border">
                      <div
                        className="h-full bg-rose-500 rounded-full"
                        style={{ width: `${Math.round(factor.severity_score * 100)}%` }}
                      />
                    </div>
                    <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                      {factor.description}
                    </p>
                  </div>
                  {factor.mitigation_hint && (
                    <div className="mt-2.5 pt-2 border-t border-surface-border text-[10px] text-cyan-600 dark:text-cyan-400 font-mono">
                      ↳ {factor.mitigation_hint}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Resource Prioritization View */}
      {activeTab === "resources" && (
        <div className="mt-4 space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 px-1 font-mono">
            <span>Prioritized Rescue Assets by Proximity & Vehicle Relevance</span>
            <span className="text-cyan-600 dark:text-cyan-400">
              Avg Transit ETA: {initialResources.allocation_summary.average_eta_minutes} mins
            </span>
          </div>

          <div className="space-y-2.5">
            {initialResources.prioritized_resources.map((unit) => (
              <div
                key={unit.unit_id}
                className="p-3.5 rounded-xl bg-surface-200 border border-surface-border hover:border-slate-400 dark:hover:border-slate-700 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-surface-100 border border-surface-border flex items-center justify-center font-mono font-bold text-sm text-cyan-600 dark:text-cyan-400 shrink-0">
                    #{unit.priority_rank}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-sm font-semibold text-foreground">{unit.unit_name}</span>
                      {getUrgencyBadge(unit.urgency)}
                      <span className="text-[10px] font-mono text-slate-500">[{unit.unit_code}]</span>
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed">{unit.reason}</p>
                    <div className="mt-1.5 text-xs text-cyan-700 dark:text-cyan-300 font-mono">
                      <span className="text-slate-500">Assigned Task: </span>
                      {unit.recommended_task}
                    </div>
                  </div>
                </div>

                <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center border-t sm:border-t-0 pt-2 sm:pt-0 border-surface-border shrink-0 text-xs font-mono">
                  <div className="text-right">
                    <span className="text-slate-500 dark:text-slate-400">Distance: </span>
                    <span className="text-foreground font-semibold">{unit.distance_km} km</span>
                  </div>
                  <div className="text-right mt-0.5">
                    <span className="text-slate-500 dark:text-slate-400">ETA: </span>
                    <span className="text-emerald-600 dark:text-emerald-400 font-semibold">{unit.estimated_transit_minutes} mins</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Command Recommendations View */}
      {activeTab === "recommendations" && (
        <div className="mt-4 space-y-3">
          <div className="p-3 rounded-lg bg-surface-200 border border-surface-border text-xs text-slate-700 dark:text-slate-300">
            <span className="font-bold text-cyan-600 dark:text-cyan-400 font-mono">Incident Strategy: </span>
            {initialRecommendations.overall_strategy}
          </div>

          <div className="space-y-3">
            {initialRecommendations.recommendations.map((rec) => (
              <div
                key={rec.id}
                className="p-3.5 rounded-xl bg-surface-200 border border-surface-border space-y-2"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <h4 className="text-sm font-semibold text-foreground">{rec.title}</h4>
                      <Badge variant={rec.priority_level === "CRITICAL" ? "critical" : "warning"} size="sm">
                        {rec.priority_level}
                      </Badge>
                    </div>
                    <span className="text-[10px] text-cyan-600 dark:text-cyan-400 font-mono">
                      Sector: {rec.target_sector} • Timeframe: {rec.timeframe}
                    </span>
                  </div>
                </div>

                <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">{rec.description}</p>

                <div className="pt-2 border-t border-surface-border">
                  <span className="text-[10px] uppercase tracking-wider text-slate-500 font-mono font-semibold">
                    Actionable Steps:
                  </span>
                  <ul className="mt-1 space-y-1 text-xs text-slate-700 dark:text-slate-300">
                    {rec.actionable_steps.map((step, sIdx) => (
                      <li key={sIdx} className="flex items-start gap-2">
                        <ChevronRight className="w-3.5 h-3.5 text-cyan-500 dark:text-cyan-400 shrink-0 mt-0.5" />
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Bottom AI Advisory Disclaimer */}
      <div className="mt-4 pt-3 border-t border-surface-border flex items-center gap-2 text-[10px] text-slate-500 font-mono">
        <Radio className="w-3 h-3 text-cyan-500 dark:text-cyan-400 animate-pulse shrink-0" />
        <span className="truncate">
          AI Decision Support Advisory • DDMA Incident Commander verification required prior to executive field deployment.
        </span>
      </div>
    </Card>
  );
};
