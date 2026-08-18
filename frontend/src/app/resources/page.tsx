"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Activity,
  Anchor,
  CheckCircle2,
  Compass,
  Filter,
  Hospital,
  Layers,
  MapPin,
  RefreshCw,
  Search,
  Shield,
  Truck,
  Users,
  X,
  Zap,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { useEOC, ResourceUnit } from "@/context/EOCContext";

export default function ResourcesPage() {
  const {
    resources,
    disasters,
    assignResourceToIncident,
    releaseResource,
  } = useEOC();

  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState<string>("ALL");
  const [filterStatus, setFilterStatus] = useState<string>("ALL");

  // Assignment Modal State
  const [assigningUnit, setAssigningUnit] = useState<ResourceUnit | null>(null);
  const [selectedIncidentId, setSelectedIncidentId] = useState<string>("");
  const [notice, setNotice] = useState<string | null>(null);

  const filtered = resources.filter((r) => {
    if (filterType !== "ALL" && r.unit_type !== filterType) return false;
    if (filterStatus !== "ALL" && r.status !== filterStatus) return false;
    if (
      searchTerm &&
      !r.name.toLowerCase().includes(searchTerm.toLowerCase()) &&
      !r.unit_code.toLowerCase().includes(searchTerm.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  const getStatusBadge = (st: string) => {
    switch (st) {
      case "AVAILABLE":
        return <Badge variant="success" size="sm" dot>AVAILABLE</Badge>;
      case "ASSIGNED":
        return <Badge variant="warning" size="sm" dot>ASSIGNED</Badge>;
      case "STANDBY":
        return <Badge variant="info" size="sm">STANDBY</Badge>;
      default:
        return <Badge variant="critical" size="sm">OFFLINE</Badge>;
    }
  };

  const getUnitIcon = (type: string) => {
    switch (type) {
      case "RESCUE_BOAT":
        return <Anchor className="w-4 h-4 text-cyan-500 dark:text-cyan-400" />;
      case "AMBULANCE":
        return <Truck className="w-4 h-4 text-rose-500 dark:text-rose-400" />;
      case "HOSPITAL":
        return <Hospital className="w-4 h-4 text-emerald-500 dark:text-emerald-400" />;
      default:
        return <Shield className="w-4 h-4 text-amber-500 dark:text-amber-400" />;
    }
  };

  const handleConfirmAssignment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!assigningUnit || !selectedIncidentId) return;
    assignResourceToIncident(assigningUnit.id, selectedIncidentId);
    setNotice(`Unit ${assigningUnit.unit_code} successfully assigned.`);
    setAssigningUnit(null);
    setSelectedIncidentId("");
    setTimeout(() => setNotice(null), 3000);
  };

  const handleRelease = (unit: ResourceUnit) => {
    releaseResource(unit.id);
    setNotice(`Unit ${unit.unit_code} returned to standby readiness.`);
    setTimeout(() => setNotice(null), 3000);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-surface-100 border border-surface-border shadow-xl">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-foreground">
              Emergency Response Fleet & Tactical Assets
            </h1>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Real-time fleet readiness telemetry, motorized boat tracking, and medical facility status
          </p>
        </div>

        <Link href="/gis">
          <Button size="sm" variant="primary" icon={<Layers className="w-3.5 h-3.5" />}>
            View Fleet on GIS Map
          </Button>
        </Link>
      </div>

      {/* Notification Toast */}
      {notice && (
        <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/40 text-emerald-700 dark:text-emerald-300 text-xs font-mono flex items-center justify-between animate-in fade-in">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-500 dark:text-emerald-400" />
            <span>{notice}</span>
          </div>
          <button onClick={() => setNotice(null)}>
            <X className="w-3.5 h-3.5 text-slate-400" />
          </button>
        </div>
      )}

      {/* KPI Overview Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-500 dark:text-slate-400">Total Response Fleet</span>
          <div className="text-2xl font-bold font-mono text-foreground mt-1">
            {resources.length} Units
          </div>
          <span className="text-[10px] text-slate-400 font-mono">Assam Basin Sector</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-500 dark:text-slate-400">Available For Dispatch</span>
          <div className="text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400 mt-1">
            {resources.filter((r) => r.status === "AVAILABLE").length} Available
          </div>
          <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono">Immediate Readiness</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-500 dark:text-slate-400">Committed on Missions</span>
          <div className="text-2xl font-bold font-mono text-amber-600 dark:text-amber-400 mt-1">
            {resources.filter((r) => r.status === "ASSIGNED").length} Assigned
          </div>
          <span className="text-[10px] text-amber-600 dark:text-amber-400 font-mono">Active Deployment</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-500 dark:text-slate-400">Standby / Medical</span>
          <div className="text-2xl font-bold font-mono text-cyan-600 dark:text-cyan-400 mt-1">
            {resources.filter((r) => r.status === "STANDBY").length} Units
          </div>
          <span className="text-[10px] text-cyan-600 dark:text-cyan-400 font-mono">Civil Hospital / Trauma</span>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-xl bg-surface-100 border border-surface-border flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-md">
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by unit code, name, or capability..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 rounded-lg bg-surface-200 border border-surface-border text-xs text-foreground placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex items-center gap-2 flex-wrap text-xs font-mono">
          <div className="flex items-center gap-1 bg-surface-200 p-1 rounded-lg border border-surface-border">
            {["ALL", "RESCUE_BOAT", "AMBULANCE", "NDRF_TEAM"].map((t) => (
              <button
                key={t}
                onClick={() => setFilterType(t)}
                className={`px-2.5 py-1 rounded text-[10px] transition-colors ${
                  filterType === t ? "bg-cyan-500/20 text-cyan-700 dark:text-cyan-300 font-bold" : "text-slate-500 hover:text-foreground"
                }`}
              >
                {t.replace("_", " ")}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-1 bg-surface-200 p-1 rounded-lg border border-surface-border">
            {["ALL", "AVAILABLE", "ASSIGNED"].map((st) => (
              <button
                key={st}
                onClick={() => setFilterStatus(st)}
                className={`px-2.5 py-1 rounded text-[10px] transition-colors ${
                  filterStatus === st ? "bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 font-bold" : "text-slate-500 hover:text-foreground"
                }`}
              >
                {st}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Resource Fleet Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((unit) => (
          <Card key={unit.id} className="border-surface-border bg-surface-100 hover:border-slate-400 dark:hover:border-slate-700 transition-colors p-4 space-y-3 shadow-lg">
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-start gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-surface-200 border border-surface-border flex items-center justify-center shrink-0">
                  {getUnitIcon(unit.unit_type)}
                </div>
                <div>
                  <h3 className="text-sm font-bold text-foreground">{unit.name}</h3>
                  <span className="text-[10px] font-mono text-slate-500">[{unit.unit_code}]</span>
                </div>
              </div>
              {getStatusBadge(unit.status)}
            </div>

            <div className="p-2.5 rounded-lg bg-surface-200 border border-surface-border text-xs space-y-1">
              <div className="text-[11px] text-slate-700 dark:text-slate-300 font-mono">
                <span className="text-slate-500">Capacity: </span>
                {unit.capacity}
              </div>
              <div className="text-[11px] text-cyan-700 dark:text-cyan-300 font-mono truncate">
                <span className="text-slate-500">Mission: </span>
                {unit.current_task}
              </div>
              {unit.assigned_incident_name && (
                <div className="text-[10px] text-amber-600 dark:text-amber-400 font-mono truncate">
                  <span className="text-slate-500">Incident: </span>
                  {unit.assigned_incident_name}
                </div>
              )}
            </div>

            <div className="pt-2 border-t border-surface-border flex items-center justify-between text-xs font-mono gap-2">
              <Link href={`/gis?resource=${unit.id}&lat=${unit.latitude}&lng=${unit.longitude}`}>
                <Button size="sm" variant="secondary" icon={<MapPin className="w-3 h-3 text-cyan-500 dark:text-cyan-400" />}>
                  Locate
                </Button>
              </Link>

              {unit.status === "AVAILABLE" && (
                <Button
                  size="sm"
                  variant="primary"
                  onClick={() => {
                    setAssigningUnit(unit);
                    setSelectedIncidentId(disasters[0]?.id || "");
                  }}
                >
                  Assign Unit
                </Button>
              )}

              {unit.status === "ASSIGNED" && (
                <Button size="sm" variant="secondary" onClick={() => handleRelease(unit)}>
                  Mark Available
                </Button>
              )}
            </div>
          </Card>
        ))}
      </div>

      {/* Modal: Assign Unit to Incident */}
      {assigningUnit && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in">
          <div className="w-full max-w-md rounded-2xl bg-surface-100 border border-surface-border shadow-2xl p-5 space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-surface-border">
              <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
                <Truck className="w-4 h-4 text-cyan-500 dark:text-cyan-400" />
                Assign {assigningUnit.name}
              </h3>
              <button onClick={() => setAssigningUnit(null)} className="text-slate-400 hover:text-foreground">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleConfirmAssignment} className="space-y-3 text-xs font-mono">
              <div>
                <label className="block text-slate-600 dark:text-slate-400 mb-1">Target Incident / Zone:</label>
                <select
                  value={selectedIncidentId}
                  onChange={(e) => setSelectedIncidentId(e.target.value)}
                  className="w-full p-2.5 rounded-lg bg-surface-200 border border-surface-border text-foreground focus:outline-none focus:border-cyan-500"
                  required
                >
                  {disasters.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.name} [Level {d.severity_level} {d.type}]
                    </option>
                  ))}
                </select>
              </div>

              <div className="pt-2 flex items-center justify-end gap-2">
                <Button size="sm" variant="secondary" onClick={() => setAssigningUnit(null)}>
                  Cancel
                </Button>
                <Button size="sm" variant="primary">
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
