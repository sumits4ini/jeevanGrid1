"use client";

import React, { useState } from "react";
import { Compass, Eye, Layers, Maximize2, Navigation, Radio, ZoomIn, ZoomOut } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export const MapPlaceholder: React.FC = () => {
  const [activeLayers, setActiveLayers] = useState<string[]>([
    "hazard_inundation",
    "critical_infra",
    "h3_hexagons",
  ]);

  const toggleLayer = (layerId: string) => {
    setActiveLayers((prev) =>
      prev.includes(layerId) ? prev.filter((id) => id !== layerId) : [...prev, layerId]
    );
  };

  const layersList = [
    { id: "hazard_inundation", label: "Inundation Polygons", color: "bg-rose-500" },
    { id: "critical_infra", label: "Critical Hospitals & Power", color: "bg-cyan-400" },
    { id: "h3_hexagons", label: "H3 Risk Hexgrid (Res-8)", color: "bg-amber-400" },
    { id: "road_network", label: "Road Network Severances", color: "bg-orange-500" },
    { id: "rescue_units", label: "Rescue Fleet Telemetry", color: "bg-emerald-400" },
  ];

  return (
    <Card className="relative overflow-hidden border-surface-border p-0 bg-[#060a12]">
      {/* Top Map Toolbar */}
      <div className="absolute top-3 left-3 right-3 z-10 flex items-center justify-between pointer-events-none">
        <div className="flex items-center gap-2 pointer-events-auto">
          <Badge variant="brand" size="md">
            <Radio className="w-3 h-3 animate-pulse" />
            GIS VECTOR ENGINE
          </Badge>
          <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-lg bg-surface-200/90 border border-surface-border text-xs text-slate-300 font-mono backdrop-blur-md">
            <span>26.3216° N, 91.0063° E</span>
            <span className="text-slate-600">|</span>
            <span>Zoom: 11.4</span>
            <span className="text-slate-600">|</span>
            <span>EPSG:4326</span>
          </div>
        </div>

        <div className="flex items-center gap-1.5 pointer-events-auto">
          <Button size="sm" variant="secondary" title="Zoom In">
            <ZoomIn className="w-3.5 h-3.5" />
          </Button>
          <Button size="sm" variant="secondary" title="Zoom Out">
            <ZoomOut className="w-3.5 h-3.5" />
          </Button>
          <Button size="sm" variant="secondary" title="Reset Orientation">
            <Compass className="w-3.5 h-3.5" />
          </Button>
        </div>
      </div>

      {/* Main Tactical Map Display Area */}
      <div className="h-[440px] w-full relative flex items-center justify-center bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:24px_24px]">
        {/* Subtle Map Coordinate Grid Lines */}
        <div className="absolute inset-0 opacity-20 pointer-events-none">
          <div className="absolute top-1/2 left-0 right-0 h-px bg-cyan-500/40" />
          <div className="absolute left-1/2 top-0 bottom-0 w-px bg-cyan-500/40" />
        </div>

        {/* Center Target & Map Overview Callout */}
        <div className="text-center z-10 max-w-md px-6 py-5 rounded-2xl bg-surface-200/95 border border-surface-border shadow-2xl backdrop-blur-md">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/30 mx-auto flex items-center justify-center text-cyan-400 mb-3">
            <Layers className="w-6 h-6 animate-pulse" />
          </div>
          <h4 className="text-base font-semibold text-slate-100">
            Interactive GIS Map Viewport
          </h4>
          <p className="text-xs text-slate-400 mt-1 leading-relaxed">
            Ready for <span className="text-cyan-400 font-mono">Phase 5 (MapLibre GL JS)</span>. Vector tiles, PostGIS hazard overlays, H3 hexagons, and dynamic flood-routing graphs will render in this viewport.
          </p>

          {/* Active Sector Summary Pill */}
          <div className="mt-4 pt-3 border-t border-surface-border/80 flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400">Target Region:</span>
            <span className="text-cyan-400 font-semibold">Barpeta District, Assam</span>
          </div>
        </div>

        {/* Bottom Layer Control Overlay */}
        <div className="absolute bottom-3 left-3 z-10 flex flex-wrap items-center gap-1.5 max-w-[calc(100%-24px)]">
          {layersList.map((layer) => {
            const isActive = activeLayers.includes(layer.id);
            return (
              <button
                key={layer.id}
                onClick={() => toggleLayer(layer.id)}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-mono transition-all backdrop-blur-md border ${
                  isActive
                    ? "bg-surface-100/90 text-slate-200 border-slate-600"
                    : "bg-surface-200/50 text-slate-500 border-surface-border/40 opacity-60"
                }`}
              >
                <span className={`w-2 h-2 rounded-full ${layer.color}`} />
                <span>{layer.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </Card>
  );
};
