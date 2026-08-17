"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Activity,
  AlertOctagon,
  AlertTriangle,
  ArrowRight,
  Calendar,
  ChevronRight,
  Compass,
  Eye,
  Flame,
  Layers,
  MapPin,
  RefreshCw,
  Shield,
  Users,
  Waves,
  Wind,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

interface DisasterItem {
  id: string;
  name: string;
  type: string;
  severity_level: number;
  status: string;
  latitude: number;
  longitude: number;
  affected_population: number;
  inundation_depth_m?: number;
  reported_at: string;
  description: string;
  hazard_zones_count: number;
  criticality: string;
}

const SAMPLE_DISASTERS: DisasterItem[] = [
  {
    id: "dis-assam-01",
    name: "Assam Brahmaputra Basin Inundation 2026",
    type: "FLOOD",
    severity_level: 4,
    status: "ACTIVE",
    latitude: 26.3216,
    longitude: 91.0063,
    affected_population: 85400,
    inundation_depth_m: 1.25,
    reported_at: "2026-08-16T14:30:00Z",
    description: "Severe riverine flood wave across Barpeta lowlands. Critical bridge access severed.",
    hazard_zones_count: 3,
    criticality: "DEFCON 1 • CRITICAL",
  },
  {
    id: "dis-chennai-02",
    name: "Chennai Coastal Storm Surge Alert",
    type: "CYCLONE",
    severity_level: 3,
    status: "ACTIVE",
    latitude: 13.0827,
    longitude: 80.2707,
    affected_population: 32000,
    inundation_depth_m: 0.45,
    reported_at: "2026-08-17T06:15:00Z",
    description: "Deep depression in Bay of Bengal generating 45 knot gusts and storm tides along southern corridor.",
    hazard_zones_count: 2,
    criticality: "DEFCON 2 • HIGH ALERT",
  },
];

export default function DisastersPage() {
  const [selectedDisaster, setSelectedDisaster] = useState<DisasterItem>(SAMPLE_DISASTERS[0]);
  const [filterType, setFilterType] = useState<string>("ALL");

  const filtered = SAMPLE_DISASTERS.filter((d) => {
    if (filterType === "ALL") return true;
    return d.type === filterType;
  });

  return (
    <div className="space-y-6 pb-12">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-surface-100 border border-surface-border shadow-xl">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse" />
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-slate-100 dark:text-slate-100 light:text-slate-900">
              Disaster Intelligence & Hazard Tracking
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time multi-hazard telemetry fusion, flood breach monitoring, and casualty impact tracking
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link href="/gis">
            <Button size="sm" variant="primary" icon={<Layers className="w-3.5 h-3.5" />}>
              Open Full GIS Map
            </Button>
          </Link>
        </div>
      </div>

      {/* KPI Overview Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Active Incidents</span>
          <div className="text-2xl font-bold font-mono text-slate-100 mt-1">
            {SAMPLE_DISASTERS.length}
          </div>
          <span className="text-[10px] text-rose-400 font-mono">1 Critical DEFCON 1</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Total Exposed Population</span>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">
            117,400
          </div>
          <span className="text-[10px] text-slate-500 font-mono">Within Hazard Buffer</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Peak Inundation Depth</span>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-1">
            1.25m
          </div>
          <span className="text-[10px] text-amber-400 font-mono">Barpeta Lowlands</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Monitored Zones</span>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
            5 Perimeters
          </div>
          <span className="text-[10px] text-slate-500 font-mono">PostGIS Polygon Sync</span>
        </div>
      </div>

      {/* Main Grid: Disaster List + Disaster Detail Drawer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Disaster List (5 Cols) */}
        <div className="lg:col-span-5 space-y-3">
          <div className="flex items-center justify-between px-1 text-xs text-slate-400 font-mono">
            <span>Incident Feed ({filtered.length})</span>
            <div className="flex items-center gap-1">
              {["ALL", "FLOOD", "CYCLONE"].map((t) => (
                <button
                  key={t}
                  onClick={() => setFilterType(t)}
                  className={`px-2 py-0.5 rounded text-[10px] transition-colors ${
                    filterType === t ? "bg-cyan-500/20 text-cyan-300 font-bold" : "text-slate-500"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-3">
            {filtered.map((disaster) => {
              const isSelected = selectedDisaster.id === disaster.id;
              return (
                <div
                  key={disaster.id}
                  onClick={() => setSelectedDisaster(disaster)}
                  className={`p-4 rounded-xl border transition-all cursor-pointer ${
                    isSelected
                      ? "bg-cyan-500/10 border-cyan-500/50 shadow-lg shadow-cyan-950/30"
                      : "bg-surface-100/80 border-surface-border hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <Badge variant={disaster.severity_level >= 4 ? "critical" : "warning"} size="sm" dot>
                          Level {disaster.severity_level} {disaster.type}
                        </Badge>
                        <span className="text-[10px] font-mono text-slate-500">[{disaster.id}]</span>
                      </div>
                      <h3 className="text-sm font-bold text-slate-100 mt-1.5">{disaster.name}</h3>
                      <p className="text-xs text-slate-400 mt-1 line-clamp-2">{disaster.description}</p>
                    </div>
                  </div>

                  <div className="mt-3 pt-2.5 border-t border-surface-border/60 flex items-center justify-between text-xs font-mono">
                    <span className="text-slate-400 flex items-center gap-1">
                      <Users className="w-3.5 h-3.5 text-cyan-400" />
                      {disaster.affected_population.toLocaleString()} exposed
                    </span>
                    <span className="text-cyan-400 font-semibold flex items-center gap-1">
                      Inspect Details <ChevronRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Detailed Tactical Breakdown (7 Cols) */}
        <div className="lg:col-span-7 space-y-4">
          <Card className="border-cyan-500/30 bg-surface-100 shadow-2xl p-5 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-surface-border gap-2">
              <div>
                <div className="flex items-center gap-2">
                  <Badge variant={selectedDisaster.severity_level >= 4 ? "critical" : "warning"} size="md" dot>
                    {selectedDisaster.criticality}
                  </Badge>
                  <span className="text-xs font-mono text-slate-400">
                    Status: <strong className="text-emerald-400">{selectedDisaster.status}</strong>
                  </span>
                </div>
                <h2 className="text-lg font-bold text-slate-100 mt-1.5">{selectedDisaster.name}</h2>
              </div>

              <Link href={`/gis?lat=${selectedDisaster.latitude}&lng=${selectedDisaster.longitude}`}>
                <Button size="sm" variant="primary" icon={<MapPin className="w-3.5 h-3.5" />}>
                  View on GIS Map
                </Button>
              </Link>
            </div>

            {/* Tactical Metrics Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              <div className="p-3 rounded-lg bg-surface-200 border border-surface-border">
                <span className="text-[10px] font-mono text-slate-400 uppercase">GPS Centerpoint</span>
                <div className="text-xs font-mono font-bold text-slate-200 mt-1">
                  {selectedDisaster.latitude}° N, {selectedDisaster.longitude}° E
                </div>
              </div>

              <div className="p-3 rounded-lg bg-surface-200 border border-surface-border">
                <span className="text-[10px] font-mono text-slate-400 uppercase">Inundation Depth</span>
                <div className="text-xs font-mono font-bold text-rose-400 mt-1">
                  {selectedDisaster.inundation_depth_m || 0.5}m Recorded
                </div>
              </div>

              <div className="p-3 rounded-lg bg-surface-200 border border-surface-border">
                <span className="text-[10px] font-mono text-slate-400 uppercase">Hazard Zones</span>
                <div className="text-xs font-mono font-bold text-amber-400 mt-1">
                  {selectedDisaster.hazard_zones_count} Polygon Polygons
                </div>
              </div>
            </div>

            {/* Narrative Description */}
            <div className="p-3.5 rounded-xl bg-surface-200/70 border border-surface-border text-xs text-slate-300 leading-relaxed">
              <strong className="text-cyan-400 font-mono uppercase text-[10px] block mb-1">
                EOC Tactical Intelligence Brief:
              </strong>
              {selectedDisaster.description}
            </div>

            {/* Action Directives */}
            <div>
              <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider font-mono mb-2">
                Operational Field Directives
              </h4>
              <div className="space-y-2 text-xs text-slate-300">
                <div className="p-2.5 rounded-lg bg-surface-200/50 border border-surface-border/70 flex items-start gap-2">
                  <ChevronRight className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                  <span>Deploy motorized shallow-draft rescue craft to eastern riverine slipways.</span>
                </div>
                <div className="p-2.5 rounded-lg bg-surface-200/50 border border-surface-border/70 flex items-start gap-2">
                  <ChevronRight className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                  <span>Mobilize mobile emergency power backup unit to District Civil Hospital.</span>
                </div>
                <div className="p-2.5 rounded-lg bg-surface-200/50 border border-surface-border/70 flex items-start gap-2">
                  <ChevronRight className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                  <span>Issue automated SMS advisories for high-elevation assembly points.</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
