"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  AlertOctagon,
  AlertTriangle,
  ChevronRight,
  Compass,
  Filter,
  Layers,
  MapPin,
  Shield,
  ShieldAlert,
  Truck,
  Users,
  Zap,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { useEOC, RiskHex } from "@/context/EOCContext";

export default function RiskZonesPage() {
  const {
    riskZones,
    selectedHex,
    selectRiskHex,
    resources,
  } = useEOC();

  const [filterTier, setFilterTier] = useState<string>("ALL");

  const filtered = riskZones.filter((h) => {
    if (filterTier === "ALL") return true;
    return h.tier === filterTier;
  });

  const activeHex = selectedHex || riskZones[0];

  return (
    <div className="space-y-6 pb-12">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-surface-100 border border-surface-border shadow-xl">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse" />
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-slate-100 dark:text-slate-100 light:text-slate-900">
              Multi-Criteria Decision Analysis (MCDA) & Risk Hexgrid
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Spatial vulnerability modeling, Uber H3 Resolution-8 hex indexing, and population exposure matrix
          </p>
        </div>

        <Link href={`/gis?hex=${activeHex?.hex_id}&lat=${activeHex?.latitude}&lng=${activeHex?.longitude}`}>
          <Button size="sm" variant="primary" icon={<Layers className="w-3.5 h-3.5" />}>
            Open Hexgrid on GIS Map
          </Button>
        </Link>
      </div>

      {/* KPI Overview */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Composite Risk Index</span>
          <div className="text-2xl font-bold font-mono text-rose-400 mt-1">
            0.88 / 1.00
          </div>
          <span className="text-[10px] text-rose-400 font-mono">CRITICAL DEFCON 1</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Critical H3 Cells</span>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-1">
            {riskZones.filter((h) => h.tier === "CRITICAL").length} Cells (Res-8)
          </div>
          <span className="text-[10px] text-slate-500 font-mono">1.25m Inundation</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">High Risk Population</span>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">
            {riskZones.reduce((acc, h) => acc + h.population, 0).toLocaleString()}
          </div>
          <span className="text-[10px] text-cyan-400 font-mono">Urgent Evacuation Required</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">MCDA Factor Confidence</span>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
            94%
          </div>
          <span className="text-[10px] text-emerald-400 font-mono">Spatial Telemetry Validated</span>
        </div>
      </div>

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: H3 Risk Cells List (6 Cols) */}
        <div className="lg:col-span-6 space-y-3">
          <div className="flex items-center justify-between px-1 text-xs text-slate-400 font-mono">
            <span>H3 Hexgrid Index ({filtered.length})</span>
            <div className="flex items-center gap-1">
              {["ALL", "CRITICAL", "HIGH", "MEDIUM"].map((tier) => (
                <button
                  key={tier}
                  onClick={() => setFilterTier(tier)}
                  className={`px-2 py-0.5 rounded text-[10px] transition-colors ${
                    filterTier === tier ? "bg-amber-500/20 text-amber-300 font-bold" : "text-slate-500"
                  }`}
                >
                  {tier}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-3">
            {filtered.map((hex) => {
              const isSelected = activeHex?.hex_id === hex.hex_id;
              return (
                <div
                  key={hex.hex_id}
                  onClick={() => selectRiskHex(hex.hex_id)}
                  className={`p-4 rounded-xl border transition-all cursor-pointer ${
                    isSelected
                      ? "bg-amber-500/10 border-amber-500/50 shadow-lg shadow-amber-950/30"
                      : "bg-surface-100/80 border-surface-border hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <Badge
                          variant={
                            hex.tier === "CRITICAL"
                              ? "critical"
                              : hex.tier === "HIGH"
                              ? "warning"
                              : "default"
                          }
                          size="sm"
                          dot
                        >
                          {hex.tier} ({hex.risk_score})
                        </Badge>
                        <span className="text-[10px] font-mono text-slate-500">[{hex.hex_id}]</span>
                      </div>
                      <h3 className="text-sm font-bold text-slate-100 mt-1.5">{hex.location_name}</h3>
                    </div>
                  </div>

                  <div className="mt-3 pt-2.5 border-t border-surface-border/60 flex items-center justify-between text-xs font-mono">
                    <span className="text-slate-400 flex items-center gap-1">
                      <Users className="w-3.5 h-3.5 text-cyan-400" />
                      {hex.population.toLocaleString()} exposed
                    </span>
                    <span className="text-amber-400 font-semibold flex items-center gap-1">
                      Inspect Hex <ChevronRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Hex Detail & MCDA Formulation (6 Cols) */}
        <div className="lg:col-span-6 space-y-4">
          {activeHex && (
            <Card className="border-amber-500/30 bg-surface-100 shadow-2xl p-5 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-surface-border gap-2">
                <div>
                  <span className="text-[10px] uppercase font-mono text-slate-400">
                    H3 Cell: {activeHex.hex_id}
                  </span>
                  <h2 className="text-lg font-bold text-slate-100 mt-0.5">{activeHex.location_name}</h2>
                </div>

                <div className="flex items-center gap-2">
                  <Link href={`/gis?hex=${activeHex.hex_id}&lat=${activeHex.latitude}&lng=${activeHex.longitude}`}>
                    <Button size="sm" variant="secondary" icon={<MapPin className="w-3.5 h-3.5 text-amber-400" />}>
                      Locate on GIS
                    </Button>
                  </Link>
                  <Link href="/resources">
                    <Button size="sm" variant="primary" icon={<Truck className="w-3.5 h-3.5" />}>
                      View Resources
                    </Button>
                  </Link>
                </div>
              </div>

              {/* Risk Factor Breakdown Bars */}
              <div className="space-y-3">
                <div>
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="text-slate-300">Hydrological Inundation Factor (40%)</span>
                    <span className="text-rose-400 font-bold">0.92</span>
                  </div>
                  <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden mt-1.5">
                    <div className="h-full bg-rose-500 rounded-full" style={{ width: "92%" }} />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="text-slate-300">Demographic Vulnerability Factor (35%)</span>
                    <span className="text-amber-400 font-bold">0.88</span>
                  </div>
                  <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden mt-1.5">
                    <div className="h-full bg-amber-500 rounded-full" style={{ width: "88%" }} />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="text-slate-300">Infrastructure Disruption Factor (25%)</span>
                    <span className="text-cyan-400 font-bold">0.85</span>
                  </div>
                  <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden mt-1.5">
                    <div className="h-full bg-cyan-500 rounded-full" style={{ width: "85%" }} />
                  </div>
                </div>
              </div>

              {/* Critical Facilities in Hex */}
              <div className="pt-2 border-t border-surface-border">
                <span className="text-[10px] font-bold font-mono text-slate-400 uppercase tracking-wider block mb-2">
                  Compromised Facilities Inside H3 Cell:
                </span>
                <div className="space-y-1.5">
                  {activeHex.critical_facilities.map((fac, idx) => (
                    <div key={idx} className="p-2.5 rounded-lg bg-surface-200 border border-surface-border text-xs text-rose-300 font-mono flex items-center gap-2">
                      <AlertOctagon className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                      <span>{fac}</span>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
