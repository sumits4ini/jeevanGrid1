"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Activity,
  AlertOctagon,
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  Compass,
  Eye,
  Flame,
  Layers,
  MapPin,
  RefreshCw,
  Shield,
  Truck,
  Users,
  Waves,
  X,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { useEOC, Incident } from "@/context/EOCContext";

export default function DisastersPage() {
  const {
    disasters,
    selectedDisaster,
    selectDisaster,
    escalateDisaster,
    resolveDisaster,
    resources,
    assignResourceToIncident,
  } = useEOC();

  const [filterType, setFilterType] = useState<string>("ALL");
  const [isAssignModalOpen, setIsAssignModalOpen] = useState(false);
  const [selectedUnitId, setSelectedUnitId] = useState<string>("");
  const [actionNotice, setActionNotice] = useState<string | null>(null);

  const filtered = disasters.filter((d) => {
    if (filterType === "ALL") return true;
    return d.type === filterType;
  });

  const activeIncident = selectedDisaster || disasters[0];
  const availableResources = resources.filter((r) => r.status === "AVAILABLE");

  const handleEscalate = () => {
    if (!activeIncident) return;
    escalateDisaster(activeIncident.id);
    setActionNotice(`Incident ${activeIncident.name} escalated to DEFCON 1 maximum readiness.`);
    setTimeout(() => setActionNotice(null), 3000);
  };

  const handleResolve = () => {
    if (!activeIncident) return;
    resolveDisaster(activeIncident.id);
    setActionNotice(`Incident ${activeIncident.name} transitioned to RESOLVED status.`);
    setTimeout(() => setActionNotice(null), 3000);
  };

  const handleAssignUnit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedUnitId || !activeIncident) return;
    assignResourceToIncident(selectedUnitId, activeIncident.id, `Dispatched to ${activeIncident.name}`);
    setIsAssignModalOpen(false);
    setSelectedUnitId("");
    setActionNotice("Response Unit dispatched successfully to incident zone.");
    setTimeout(() => setActionNotice(null), 3000);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-surface-100 border border-surface-border shadow-xl">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse" />
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-slate-100 dark:text-slate-100 light:text-slate-900">
              Disaster Intelligence & Incident Management
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Multi-hazard detection, breach perimeter monitoring, and emergency response decision workflow
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link href={`/gis?incident=${activeIncident?.id}&lat=${activeIncident?.latitude}&lng=${activeIncident?.longitude}`}>
            <Button size="sm" variant="primary" icon={<Layers className="w-3.5 h-3.5" />}>
              Open Incident on GIS
            </Button>
          </Link>
        </div>
      </div>

      {/* Action Notification Alert */}
      {actionNotice && (
        <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/40 text-cyan-300 text-xs font-mono flex items-center justify-between animate-in fade-in">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-cyan-400" />
            <span>{actionNotice}</span>
          </div>
          <button onClick={() => setActionNotice(null)}>
            <X className="w-3.5 h-3.5 text-slate-400" />
          </button>
        </div>
      )}

      {/* KPI Overview Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Active Incidents</span>
          <div className="text-2xl font-bold font-mono text-slate-100 mt-1">
            {disasters.filter((d) => d.status === "ACTIVE").length}
          </div>
          <span className="text-[10px] text-rose-400 font-mono">1 DEFCON 1 Critical</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Total Exposed Population</span>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">
            {disasters.reduce((acc, d) => acc + d.affected_population, 0).toLocaleString()}
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
          <span className="text-[10px] uppercase font-mono text-slate-400">Available Fleet Units</span>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
            {availableResources.length} Units
          </div>
          <span className="text-[10px] text-emerald-400 font-mono">Ready for Dispatch</span>
        </div>
      </div>

      {/* Main Grid: Disaster List + Detailed Tactical Workflow */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Disaster Incident List (5 Cols) */}
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
              const isSelected = activeIncident?.id === disaster.id;
              return (
                <div
                  key={disaster.id}
                  onClick={() => selectDisaster(disaster.id)}
                  className={`p-4 rounded-xl border transition-all cursor-pointer ${
                    isSelected
                      ? "bg-cyan-500/10 border-cyan-500/50 shadow-lg shadow-cyan-950/30"
                      : "bg-surface-100/80 border-surface-border hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <Badge
                          variant={
                            disaster.status === "RESOLVED"
                              ? "success"
                              : disaster.severity_level >= 4
                              ? "critical"
                              : "warning"
                          }
                          size="sm"
                          dot
                        >
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
                      Inspect Workflow <ChevronRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Tactical Command & Action Workflow (7 Cols) */}
        <div className="lg:col-span-7 space-y-4">
          {activeIncident ? (
            <Card className="border-cyan-500/30 bg-surface-100 shadow-2xl p-5 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-surface-border gap-3">
                <div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <Badge
                      variant={
                        activeIncident.status === "RESOLVED"
                          ? "success"
                          : activeIncident.severity_level >= 4
                          ? "critical"
                          : "warning"
                      }
                      size="md"
                      dot
                    >
                      {activeIncident.criticality}
                    </Badge>
                    <span className="text-xs font-mono text-slate-400">
                      Status: <strong className="text-emerald-400">{activeIncident.status}</strong>
                    </span>
                  </div>
                  <h2 className="text-lg font-bold text-slate-100 mt-1.5">{activeIncident.name}</h2>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  <Link href={`/gis?incident=${activeIncident.id}&lat=${activeIncident.latitude}&lng=${activeIncident.longitude}`}>
                    <Button size="sm" variant="secondary" icon={<MapPin className="w-3.5 h-3.5 text-cyan-400" />}>
                      View on Map
                    </Button>
                  </Link>
                  <Link href="/risk-zones">
                    <Button size="sm" variant="secondary" icon={<Layers className="w-3.5 h-3.5 text-amber-400" />}>
                      Risk Zone
                    </Button>
                  </Link>
                </div>
              </div>

              {/* Action Buttons Workflow */}
              <div className="p-3 rounded-xl bg-surface-200 border border-surface-border flex items-center justify-between gap-2 flex-wrap">
                <span className="text-[11px] font-mono text-slate-300 font-semibold">Incident Actions:</span>
                <div className="flex items-center gap-2 flex-wrap">
                  <Button
                    size="sm"
                    variant="secondary"
                    onClick={() => setIsAssignModalOpen(true)}
                    icon={<Truck className="w-3.5 h-3.5 text-emerald-400" />}
                  >
                    Assign Fleet Unit
                  </Button>
                  {activeIncident.status !== "RESOLVED" && (
                    <>
                      <Button
                        size="sm"
                        variant="secondary"
                        onClick={handleEscalate}
                        icon={<Flame className="w-3.5 h-3.5 text-rose-400" />}
                      >
                        Escalate (DEFCON 1)
                      </Button>
                      <Button
                        size="sm"
                        variant="primary"
                        onClick={handleResolve}
                        icon={<CheckCircle2 className="w-3.5 h-3.5" />}
                      >
                        Resolve Incident
                      </Button>
                    </>
                  )}
                </div>
              </div>

              {/* Tactical Metrics Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                <div className="p-3 rounded-lg bg-surface-200 border border-surface-border">
                  <span className="text-[10px] font-mono text-slate-400 uppercase">GPS Centerpoint</span>
                  <div className="text-xs font-mono font-bold text-slate-200 mt-1">
                    {activeIncident.latitude}° N, {activeIncident.longitude}° E
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-surface-200 border border-surface-border">
                  <span className="text-[10px] font-mono text-slate-400 uppercase">Inundation Depth</span>
                  <div className="text-xs font-mono font-bold text-rose-400 mt-1">
                    {activeIncident.inundation_depth_m || 0.5}m Recorded
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-surface-200 border border-surface-border">
                  <span className="text-[10px] font-mono text-slate-400 uppercase">Hazard Zones</span>
                  <div className="text-xs font-mono font-bold text-amber-400 mt-1">
                    {activeIncident.hazard_zones_count} Polygons Monitored
                  </div>
                </div>
              </div>

              {/* Narrative Brief */}
              <div className="p-3.5 rounded-xl bg-surface-200/70 border border-surface-border text-xs text-slate-300 leading-relaxed">
                <strong className="text-cyan-400 font-mono uppercase text-[10px] block mb-1">
                  EOC Tactical Intelligence Brief:
                </strong>
                {activeIncident.description}
              </div>
            </Card>
          ) : (
            <Card className="p-8 text-center text-xs text-slate-400 font-mono">
              Select an incident from the feed to inspect details and dispatch resources.
            </Card>
          )}
        </div>
      </div>

      {/* Modal: Assign Resource to Incident */}
      {isAssignModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in">
          <div className="w-full max-w-md rounded-2xl bg-surface-100 border border-surface-border shadow-2xl p-5 space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-surface-border">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <Truck className="w-4 h-4 text-cyan-400" />
                Dispatch Fleet to {activeIncident?.name}
              </h3>
              <button onClick={() => setIsAssignModalOpen(false)} className="text-slate-400 hover:text-slate-200">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleAssignUnit} className="space-y-3 text-xs font-mono">
              <div>
                <label className="block text-slate-400 mb-1">Select Available Unit:</label>
                <select
                  value={selectedUnitId}
                  onChange={(e) => setSelectedUnitId(e.target.value)}
                  className="w-full p-2.5 rounded-lg bg-surface-200 border border-surface-border text-slate-200 focus:outline-none focus:border-cyan-500"
                  required
                >
                  <option value="">-- Choose Emergency Unit --</option>
                  {availableResources.map((unit) => (
                    <option key={unit.id} value={unit.id}>
                      {unit.name} [{unit.unit_code}] — {unit.capacity}
                    </option>
                  ))}
                </select>
              </div>

              <div className="pt-2 flex items-center justify-end gap-2">
                <Button size="sm" variant="secondary" onClick={() => setIsAssignModalOpen(false)}>
                  Cancel
                </Button>
                <Button size="sm" variant="primary" disabled={!selectedUnitId}>
                  Confirm Dispatch
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
