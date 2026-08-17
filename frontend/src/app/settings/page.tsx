"use client";

import React, { useState } from "react";
import {
  Check,
  Compass,
  Database,
  Globe,
  Layers,
  Moon,
  Radio,
  Save,
  Server,
  Settings as SettingsIcon,
  Shield,
  Sun,
  Zap,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { useTheme } from "@/context/ThemeContext";

export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const [activeScenario, setActiveScenario] = useState("assam-2026");
  const [mapProvider, setMapProvider] = useState("carto-dark");
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = () => {
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 2000);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-surface-100 border border-surface-border shadow-xl">
        <div>
          <div className="flex items-center gap-2.5">
            <SettingsIcon className="w-5 h-5 text-cyan-400" />
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-slate-100 dark:text-slate-100 light:text-slate-900">
              Settings & Command Configuration
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            EOC operational parameters, disaster simulation scenarios, and GIS visualization settings
          </p>
        </div>

        <Button
          size="sm"
          variant="primary"
          onClick={handleSave}
          icon={isSaved ? <Check className="w-3.5 h-3.5" /> : <Save className="w-3.5 h-3.5" />}
        >
          {isSaved ? "Settings Saved" : "Save Changes"}
        </Button>
      </div>

      {/* Settings Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 1. Theme & Appearance */}
        <Card className="border-surface-border bg-surface-100 p-5 space-y-4 shadow-xl">
          <div className="flex items-center gap-2 pb-2 border-b border-surface-border">
            <Sun className="w-4 h-4 text-amber-400" />
            <h3 className="text-sm font-bold text-slate-100">Theme & Visual Experience</h3>
          </div>
          <p className="text-xs text-slate-400">
            Choose your preferred interface theme. Selection persists automatically across sessions.
          </p>

          <div className="grid grid-cols-2 gap-3 pt-2">
            <button
              onClick={() => setTheme("dark")}
              className={`p-4 rounded-xl border flex flex-col items-center gap-2 transition-all ${
                theme === "dark"
                  ? "bg-slate-900 border-cyan-500 text-cyan-300 shadow-lg shadow-cyan-950/40"
                  : "bg-surface-200 border-surface-border text-slate-400 hover:text-slate-200"
              }`}
            >
              <Moon className="w-6 h-6 text-cyan-400" />
              <span className="text-xs font-bold font-mono">Dark Tactical EOC</span>
              <span className="text-[10px] text-slate-500 font-mono">Optimized for Night Operations</span>
            </button>

            <button
              onClick={() => setTheme("light")}
              className={`p-4 rounded-xl border flex flex-col items-center gap-2 transition-all ${
                theme === "light"
                  ? "bg-white border-cyan-500 text-cyan-700 shadow-lg"
                  : "bg-surface-200 border-surface-border text-slate-400 hover:text-slate-200"
              }`}
            >
              <Sun className="w-6 h-6 text-amber-500" />
              <span className="text-xs font-bold font-mono">Light High-Contrast</span>
              <span className="text-[10px] text-slate-500 font-mono">Optimized for Bright Daylight</span>
            </button>
          </div>
        </Card>

        {/* 2. Simulation Scenario Selection */}
        <Card className="border-surface-border bg-surface-100 p-5 space-y-4 shadow-xl">
          <div className="flex items-center gap-2 pb-2 border-b border-surface-border">
            <Compass className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-100">Disaster Scenario Simulation</h3>
          </div>
          <p className="text-xs text-slate-400">
            Select the active disaster incident scenario to load relevant GIS perimeters and fleet telemetry.
          </p>

          <div className="space-y-2 pt-1">
            {[
              {
                id: "assam-2026",
                title: "Assam Brahmaputra Basin Inundation 2026",
                sub: "Riverine flood wave, bridge submergences, boat rescue operations",
                badge: "ACTIVE",
              },
              {
                id: "chennai-2026",
                title: "Chennai Coastal Storm Surge Alert",
                sub: "Coastal cyclone, gale winds, urban drainage backflow",
                badge: "STANDBY",
              },
              {
                id: "uttarakhand-2026",
                title: "Uttarakhand Mountain Highway Landslide",
                sub: "Debris blockage, high-altitude chopper evacuation",
                badge: "SIMULATION",
              },
            ].map((sc) => (
              <div
                key={sc.id}
                onClick={() => setActiveScenario(sc.id)}
                className={`p-3 rounded-xl border cursor-pointer transition-all ${
                  activeScenario === sc.id
                    ? "bg-cyan-500/10 border-cyan-500 text-slate-100"
                    : "bg-surface-200 border-surface-border text-slate-400 hover:border-slate-700"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold font-mono">{sc.title}</span>
                  <Badge variant={sc.badge === "ACTIVE" ? "critical" : "default"} size="sm">
                    {sc.badge}
                  </Badge>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">{sc.sub}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* 3. GIS Basemap & Vector Settings */}
        <Card className="border-surface-border bg-surface-100 p-5 space-y-3 shadow-xl">
          <div className="flex items-center gap-2 pb-2 border-b border-surface-border">
            <Layers className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-100">GIS & Coordinate Display</h3>
          </div>
          <div className="space-y-2 text-xs font-mono">
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-surface-200 border border-surface-border">
              <span className="text-slate-300">Geodetic Datum:</span>
              <strong className="text-cyan-400">EPSG:4326 (WGS84 GPS)</strong>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-surface-200 border border-surface-border">
              <span className="text-slate-300">Projected Metric CRS:</span>
              <strong className="text-emerald-400">EPSG:3857 (Web Mercator)</strong>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-surface-200 border border-surface-border">
              <span className="text-slate-300">Default Zoom Level:</span>
              <strong className="text-slate-200">11.5x (District View)</strong>
            </div>
          </div>
        </Card>

        {/* 4. API Endpoints & Server Telemetry */}
        <Card className="border-surface-border bg-surface-100 p-5 space-y-3 shadow-xl">
          <div className="flex items-center gap-2 pb-2 border-b border-surface-border">
            <Server className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-100">Network & Engine Endpoints</h3>
          </div>
          <div className="space-y-2 text-xs font-mono">
            <div className="p-2.5 rounded-lg bg-surface-200 border border-surface-border">
              <span className="text-slate-400 text-[10px] block">FastAPI REST URL:</span>
              <strong className="text-slate-200 text-[11px]">http://localhost:8000/api/v1</strong>
            </div>
            <div className="p-2.5 rounded-lg bg-surface-200 border border-surface-border">
              <span className="text-slate-400 text-[10px] block">WebSocket Telemetry URL:</span>
              <strong className="text-emerald-400 text-[11px]">ws://localhost:8000/api/v1/ws/operations</strong>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
