"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Activity,
  Anchor,
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
  Zap,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

interface ResourceUnitItem {
  id: string;
  unit_code: string;
  name: string;
  unit_type: "RESCUE_BOAT" | "AMBULANCE" | "NDRF_TEAM" | "HOSPITAL" | "POWER_STATION" | "SHELTER";
  status: "AVAILABLE" | "ASSIGNED" | "STANDBY" | "OFFLINE";
  capacity: string;
  latitude: number;
  longitude: number;
  assigned_incident?: string;
  current_task?: string;
}

const SAMPLE_RESOURCES: ResourceUnitItem[] = [
  {
    id: "ru-boat-01",
    unit_code: "BOAT-NDRF-01",
    name: "NDRF Rescue Craft Alpha-1",
    unit_type: "RESCUE_BOAT",
    status: "AVAILABLE",
    capacity: "12 Persons / Shallow Draft",
    latitude: 26.3200,
    longitude: 91.0080,
    assigned_incident: "Assam Flood Sector East",
    current_task: "Pre-positioned at NH-31 dry slipway junction.",
  },
  {
    id: "ru-boat-02",
    unit_code: "BOAT-NDRF-02",
    name: "NDRF Rescue Craft Alpha-2",
    unit_type: "RESCUE_BOAT",
    status: "AVAILABLE",
    capacity: "12 Persons / Shallow Draft",
    latitude: 26.3150,
    longitude: 91.0120,
    assigned_incident: "Assam Flood Sector East",
    current_task: "Standby for Ward 4 triage extraction.",
  },
  {
    id: "ru-amb-01",
    unit_code: "AMB-108-A",
    name: "ALS Ambulance Unit 108-A",
    unit_type: "AMBULANCE",
    status: "AVAILABLE",
    capacity: "2 Stretcher / Critical Life Support",
    latitude: 26.3200,
    longitude: 91.0200,
    assigned_incident: "Assam Flood Sector East",
    current_task: "Standby at high-elevation Western Bypass node.",
  },
  {
    id: "ru-ndrf-01",
    unit_code: "NDRF-BAT-01",
    name: "1st Battalion NDRF Rescue Team",
    unit_type: "NDRF_TEAM",
    status: "ASSIGNED",
    capacity: "45 Tactical Specialists",
    latitude: 26.3216,
    longitude: 91.0063,
    assigned_incident: "Assam Flood Sector East",
    current_task: "Conducting house-to-house boat extractions.",
  },
  {
    id: "loc-hosp-01",
    unit_code: "HOSP-BARPETA",
    name: "Barpeta District Civil Hospital",
    unit_type: "HOSPITAL",
    status: "STANDBY",
    capacity: "350 Beds / Trauma Unit",
    latitude: 26.3260,
    longitude: 91.0110,
    assigned_incident: "Assam Flood Sector East",
    current_task: "Emergency ward operating on generator power.",
  },
];

export default function ResourcesPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState<string>("ALL");
  const [filterStatus, setFilterStatus] = useState<string>("ALL");

  const filtered = SAMPLE_RESOURCES.filter((r) => {
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
        return <Anchor className="w-4 h-4 text-cyan-400" />;
      case "AMBULANCE":
        return <Truck className="w-4 h-4 text-rose-400" />;
      case "HOSPITAL":
        return <Hospital className="w-4 h-4 text-emerald-400" />;
      default:
        return <Shield className="w-4 h-4 text-amber-400" />;
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-surface-100 border border-surface-border shadow-xl">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-slate-100 dark:text-slate-100 light:text-slate-900">
              Emergency Response Fleet & Tactical Assets
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time fleet readiness telemetry, motorized boat tracking, and medical facility status
          </p>
        </div>

        <Link href="/gis">
          <Button size="sm" variant="primary" icon={<Layers className="w-3.5 h-3.5" />}>
            View Fleet on GIS Map
          </Button>
        </Link>
      </div>

      {/* KPI Overview Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Total Response Fleet</span>
          <div className="text-2xl font-bold font-mono text-slate-100 mt-1">
            32 Units
          </div>
          <span className="text-[10px] text-slate-500 font-mono">Assam Basin Depot</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Available For Dispatch</span>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
            18 Available
          </div>
          <span className="text-[10px] text-emerald-400 font-mono">56.3% Readiness</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Committed on Missions</span>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-1">
            14 Assigned
          </div>
          <span className="text-[10px] text-amber-400 font-mono">Ward 4 Residential Zone</span>
        </div>

        <div className="p-4 rounded-xl bg-surface-100 border border-surface-border">
          <span className="text-[10px] uppercase font-mono text-slate-400">Mutual Aid Requisitioned</span>
          <div className="text-2xl font-bold font-mono text-rose-400 mt-1">
            1 Deficit
          </div>
          <span className="text-[10px] text-rose-400 font-mono">Water Supply Tankers</span>
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
            className="w-full pl-9 pr-4 py-2 rounded-lg bg-surface-200 border border-surface-border text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex items-center gap-2 flex-wrap text-xs font-mono">
          <div className="flex items-center gap-1 bg-surface-200 p-1 rounded-lg border border-surface-border">
            {["ALL", "RESCUE_BOAT", "AMBULANCE", "NDRF_TEAM"].map((t) => (
              <button
                key={t}
                onClick={() => setFilterType(t)}
                className={`px-2.5 py-1 rounded text-[10px] transition-colors ${
                  filterType === t ? "bg-cyan-500/20 text-cyan-300 font-bold" : "text-slate-400 hover:text-slate-200"
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
                  filterStatus === st ? "bg-emerald-500/20 text-emerald-300 font-bold" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {st}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Resource Fleet Table & Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((unit) => (
          <Card key={unit.id} className="border-surface-border bg-surface-100 hover:border-slate-700 transition-colors p-4 space-y-3 shadow-lg">
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-start gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-surface-200 border border-surface-border flex items-center justify-center shrink-0">
                  {getUnitIcon(unit.unit_type)}
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-100">{unit.name}</h3>
                  <span className="text-[10px] font-mono text-slate-500">[{unit.unit_code}]</span>
                </div>
              </div>
              {getStatusBadge(unit.status)}
            </div>

            <div className="p-2.5 rounded-lg bg-surface-200/70 border border-surface-border text-xs space-y-1">
              <div className="text-[11px] text-slate-300 font-mono">
                <span className="text-slate-500">Capacity: </span>
                {unit.capacity}
              </div>
              <div className="text-[11px] text-cyan-300 font-mono">
                <span className="text-slate-500">Mission: </span>
                {unit.current_task}
              </div>
            </div>

            <div className="pt-2 border-t border-surface-border/60 flex items-center justify-between text-xs font-mono">
              <span className="text-slate-400 text-[10px]">
                {unit.latitude}° N, {unit.longitude}° E
              </span>

              <Link href={`/gis?lat=${unit.latitude}&lng=${unit.longitude}`}>
                <Button size="sm" variant="secondary" icon={<MapPin className="w-3 h-3 text-cyan-400" />}>
                  Locate on Map
                </Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
