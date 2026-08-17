"use client";

import React, { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";
import {
  Activity,
  AlertTriangle,
  Compass,
  Crosshair,
  Eye,
  Layers,
  MapPin,
  Maximize2,
  Navigation,
  RefreshCw,
  Shield,
  Truck,
  Zap,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { GISMap } from "@/components/gis/GISMap";

function GISViewportContent() {
  const searchParams = useSearchParams();
  const paramLat = searchParams.get("lat") ? parseFloat(searchParams.get("lat")!) : 26.3216;
  const paramLng = searchParams.get("lng") ? parseFloat(searchParams.get("lng")!) : 91.0063;

  const [selectedFeature, setSelectedFeature] = useState<any>({
    name: "Assam Brahmaputra Inundation Sector #4",
    type: "FLOOD_PERIMETER",
    status: "CRITICAL_SURGE",
    details: "Inundation depth recorded at 1.25m. 85,400 exposed residents within perimeter buffer.",
    coordinates: `${paramLat}° N, ${paramLng}° E`,
  });

  return (
    <div className="space-y-4 pb-12">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-surface-100 border border-surface-border shadow-xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-600/30 border border-cyan-500/40 flex items-center justify-center text-cyan-400 shrink-0">
            <Layers className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h1 className="text-xl font-bold tracking-tight text-slate-100 dark:text-slate-100 light:text-slate-900">
                GIS Spatial Command Viewport
              </h1>
              <Badge variant="brand" size="sm">
                MapLibre GL JS • Vector Engine
              </Badge>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              High-precision WGS84 geodesic overlays, PostGIS polygon layers, and dynamic fleet tracking
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md" dot>
            POSTGIS ONLINE
          </Badge>
        </div>
      </div>

      {/* Main Map Viewport & Feature Inspector Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
        {/* Primary Map Column (9 Cols) */}
        <div className="lg:col-span-9 h-[680px] rounded-2xl overflow-hidden shadow-2xl border border-surface-border">
          <GISMap
            initialCenter={[paramLng, paramLat]}
            initialZoom={12}
            className="w-full h-full"
            onFeatureClick={(feature) => setSelectedFeature(feature)}
          />
        </div>

        {/* Right Feature Inspector Column (3 Cols) */}
        <div className="lg:col-span-3 space-y-4">
          <Card className="border-surface-border bg-surface-100 p-4 space-y-3 shadow-xl">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-200 uppercase font-mono pb-2 border-b border-surface-border">
              <MapPin className="w-4 h-4 text-cyan-400" />
              <span>Spatial Feature Inspector</span>
            </div>

            <div className="space-y-2 text-xs">
              <div className="p-3 rounded-lg bg-surface-200 border border-surface-border">
                <span className="text-[10px] font-mono text-slate-400 uppercase">Selected Asset / Zone</span>
                <h4 className="text-sm font-bold text-cyan-400 mt-0.5">{selectedFeature.name}</h4>
                <div className="mt-1.5 flex items-center gap-1.5 flex-wrap">
                  <Badge variant="critical" size="sm">
                    {selectedFeature.status || "ACTIVE"}
                  </Badge>
                  <span className="text-[10px] font-mono text-slate-400">{selectedFeature.type}</span>
                </div>
              </div>

              <div className="p-3 rounded-lg bg-surface-200 border border-surface-border text-slate-300 leading-relaxed text-[11px]">
                <strong className="text-slate-400 block text-[10px] uppercase font-mono mb-1">
                  Tactical Telemetry:
                </strong>
                {selectedFeature.details || selectedFeature.assigned_task || "Real-time spatial telemetry synchronized with PostGIS spatial index."}
              </div>

              <div className="p-2.5 rounded-lg bg-surface-200 border border-surface-border text-[10px] font-mono text-slate-400 space-y-1">
                <div>Coordinates: <strong className="text-slate-200">{selectedFeature.coordinates || "26.3216° N, 91.0063° E"}</strong></div>
                <div>CRS Projection: <strong className="text-emerald-400">EPSG:4326 (WGS84)</strong></div>
                <div>Spatial Index: <strong className="text-cyan-400">GiST R-Tree</strong></div>
              </div>
            </div>
          </Card>

          {/* Quick Filter Legends */}
          <Card className="border-surface-border bg-surface-100 p-4 space-y-2 shadow-xl text-xs font-mono">
            <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider pb-1 border-b border-surface-border">
              Map Symbology Legend
            </div>
            <div className="space-y-1.5 pt-1 text-[11px]">
              <div className="flex items-center gap-2 text-slate-300">
                <span className="w-3 h-3 rounded-full bg-cyan-400/80 border border-cyan-300" />
                <span>Flood Inundation Perimeter</span>
              </div>
              <div className="flex items-center gap-2 text-slate-300">
                <span className="w-3 h-3 rounded-full bg-rose-500 border border-white" />
                <span>Critical Hospital / Medical</span>
              </div>
              <div className="flex items-center gap-2 text-slate-300">
                <span className="w-3 h-3 rounded-full bg-amber-500 border border-white" />
                <span>Power Substation / Grid</span>
              </div>
              <div className="flex items-center gap-2 text-slate-300">
                <span className="w-3 h-3 rounded-full bg-emerald-500 border border-white" />
                <span>Rescue Fleet (Boats / Ambulance)</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default function GISViewportPage() {
  return (
    <Suspense
      fallback={
        <div className="p-12 text-center font-mono text-xs text-slate-400">
          Loading GIS Spatial Viewport...
        </div>
      }
    >
      <GISViewportContent />
    </Suspense>
  );
}
