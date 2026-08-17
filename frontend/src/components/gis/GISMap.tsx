"use client";

import React, { useEffect, useRef, useState } from "react";
import maplibregl, { Map as MapLibreMap, StyleSpecification } from "maplibre-gl";
import {
  Activity,
  AlertTriangle,
  Anchor,
  Compass,
  Crosshair,
  Eye,
  EyeOff,
  Hospital,
  Layers,
  Maximize2,
  Minimize2,
  Navigation,
  RefreshCw,
  Shield,
  Truck,
  Zap,
  ZoomIn,
  ZoomOut,
} from "lucide-react";
import { useTheme } from "@/context/ThemeContext";

// GeoJSON Data Sources for Assam / Barpeta 2026 Scenario
const INUNDATION_GEOJSON: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {
        id: "zone-inundation-01",
        name: "Barpeta East Inundation Perimeter",
        depth_m: 1.25,
        risk_level: "CRITICAL",
        population_exposed: 85400,
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [90.9650, 26.3000],
            [91.0450, 26.3050],
            [91.0550, 26.3450],
            [90.9900, 26.3550],
            [90.9550, 26.3250],
            [90.9650, 26.3000],
          ],
        ],
      },
    },
    {
      type: "Feature",
      properties: {
        id: "zone-inundation-02",
        name: "Brahmaputra Lowland Breach",
        depth_m: 0.85,
        risk_level: "HIGH",
        population_exposed: 32000,
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [91.0300, 26.2800],
            [91.0700, 26.2900],
            [91.0800, 26.3200],
            [91.0400, 26.3100],
            [91.0300, 26.2800],
          ],
        ],
      },
    },
  ],
};

const H3_RISK_HEXGRID_GEOJSON: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { hex_id: "8860145b23fffff", risk_score: 0.94, tier: "CRITICAL", fill_color: "#ef4444" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [91.000, 26.335],
            [91.015, 26.342],
            [91.030, 26.335],
            [91.030, 26.320],
            [91.015, 26.313],
            [91.000, 26.320],
            [91.000, 26.335],
          ],
        ],
      },
    },
    {
      type: "Feature",
      properties: { hex_id: "8860145b27fffff", risk_score: 0.78, tier: "HIGH", fill_color: "#f97316" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [91.030, 26.335],
            [91.045, 26.342],
            [91.060, 26.335],
            [91.060, 26.320],
            [91.045, 26.313],
            [91.030, 26.320],
            [91.030, 26.335],
          ],
        ],
      },
    },
    {
      type: "Feature",
      properties: { hex_id: "8860145b2bfffff", risk_score: 0.45, tier: "MEDIUM", fill_color: "#eab308" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [90.970, 26.335],
            [90.985, 26.342],
            [91.000, 26.335],
            [91.000, 26.320],
            [90.985, 26.313],
            [90.970, 26.320],
            [90.970, 26.335],
          ],
        ],
      },
    },
  ],
};

const INFRASTRUCTURE_GEOJSON: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {
        id: "loc-hosp-01",
        name: "Barpeta Civil Hospital",
        type: "HOSPITAL",
        status: "OPERATIONAL_BACKUP",
        capacity: "350 Beds",
        details: "Generator operating on 6h backup fuel reserves.",
      },
      geometry: { type: "Point", coordinates: [91.0110, 26.3260] },
    },
    {
      type: "Feature",
      properties: {
        id: "loc-power-04",
        name: "Barpeta East Substation #4",
        type: "POWER_STATION",
        status: "OFFLINE_FLOODED",
        capacity: "33/11 kV",
        details: "Submerged. Transformer banks isolated for safety.",
      },
      geometry: { type: "Point", coordinates: [91.0280, 26.3180] },
    },
    {
      type: "Feature",
      properties: {
        id: "loc-bridge-12",
        name: "Bridge B-12 Overpass",
        type: "BRIDGE",
        status: "IMPASSABLE",
        capacity: "2-Lane",
        details: "0.65m flood water over deck. Rerouting required.",
      },
      geometry: { type: "Point", coordinates: [91.0150, 26.3180] },
    },
    {
      type: "Feature",
      properties: {
        id: "loc-shelter-01",
        name: "District Sports Complex Shelter",
        type: "SHELTER",
        status: "ACTIVE_RELIEF",
        capacity: "1,200 Persons",
        details: "Clean drinking water distribution active.",
      },
      geometry: { type: "Point", coordinates: [90.9850, 26.3380] },
    },
  ],
};

const RESCUE_FLEET_GEOJSON: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {
        id: "ru-boat-01",
        name: "NDRF Rescue Boat Alpha-1",
        unit_code: "BOAT-NDRF-01",
        unit_type: "RESCUE_BOAT",
        status: "AVAILABLE",
        speed_kmh: 18,
        assigned_task: "Residential extraction at Ward 4 slipway.",
      },
      geometry: { type: "Point", coordinates: [91.0080, 26.3200] },
    },
    {
      type: "Feature",
      properties: {
        id: "ru-boat-02",
        name: "NDRF Rescue Boat Alpha-2",
        unit_code: "BOAT-NDRF-02",
        unit_type: "RESCUE_BOAT",
        status: "AVAILABLE",
        speed_kmh: 18,
        assigned_task: "Support elderly and triage transfers.",
      },
      geometry: { type: "Point", coordinates: [91.0120, 26.3150] },
    },
    {
      type: "Feature",
      properties: {
        id: "ru-amb-01",
        name: "ALS Ambulance Unit 108-A",
        unit_code: "AMB-108-A",
        unit_type: "AMBULANCE",
        status: "AVAILABLE",
        speed_kmh: 35,
        assigned_task: "Standby at elevated NH-31 bypass.",
      },
      geometry: { type: "Point", coordinates: [91.0200, 26.3300] },
    },
  ],
};

interface GISMapProps {
  initialCenter?: [number, number];
  initialZoom?: number;
  interactive?: boolean;
  className?: string;
  onFeatureClick?: (feature: any) => void;
}

export const GISMap: React.FC<GISMapProps> = ({
  initialCenter = [91.0063, 26.3216],
  initialZoom = 11.5,
  interactive = true,
  className = "w-full h-full min-h-[420px]",
  onFeatureClick,
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MapLibreMap | null>(null);
  const { theme } = useTheme();

  // Layer Visibility State
  const [layers, setLayers] = useState({
    inundation: true,
    infrastructure: true,
    riskHexgrid: true,
    rescueFleet: true,
    roadDisruptions: true,
  });

  // HUD Metrics
  const [cursorCoords, setCursorCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [currentZoom, setCurrentZoom] = useState<number>(initialZoom);

  // Map Tile Style based on Theme
  const getMapStyle = (): StyleSpecification => {
    if (theme === "light") {
      return {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
            attribution: "&copy; OpenStreetMap Contributors",
          },
        },
        layers: [
          {
            id: "osm-tiles",
            type: "raster",
            source: "osm",
            minzoom: 0,
            maxzoom: 19,
          },
        ],
      };
    }
    return {
      version: 8,
      sources: {
        carto: {
          type: "raster",
          tiles: [
            "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
            "https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
            "https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
          ],
          tileSize: 256,
          attribution: "&copy; CartoDB & OpenStreetMap",
        },
      },
      layers: [
        {
          id: "carto-dark-tiles",
          type: "raster",
          source: "carto",
          minzoom: 0,
          maxzoom: 19,
        },
      ],
    };
  };

  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: getMapStyle(),
      center: initialCenter,
      zoom: initialZoom,
      attributionControl: false,
    });

    mapRef.current = map;

    map.on("load", () => {
      // 1. Inundation Layer Source & Layer
      map.addSource("inundation-source", {
        type: "geojson",
        data: INUNDATION_GEOJSON,
      });

      map.addLayer({
        id: "inundation-fill",
        type: "fill",
        source: "inundation-source",
        paint: {
          "fill-color": "#06b6d4",
          "fill-opacity": 0.35,
        },
      });

      map.addLayer({
        id: "inundation-stroke",
        type: "line",
        source: "inundation-source",
        paint: {
          "line-color": "#0891b2",
          "line-width": 2,
          "line-dasharray": [2, 1],
        },
      });

      // 2. H3 Hexgrid Source & Layer
      map.addSource("hexgrid-source", {
        type: "geojson",
        data: H3_RISK_HEXGRID_GEOJSON,
      });

      map.addLayer({
        id: "hexgrid-fill",
        type: "fill",
        source: "hexgrid-source",
        paint: {
          "fill-color": ["get", "fill_color"],
          "fill-opacity": 0.4,
        },
      });

      map.addLayer({
        id: "hexgrid-line",
        type: "line",
        source: "hexgrid-source",
        paint: {
          "line-line-color": "#ffffff",
          "line-width": 1.5,
          "line-opacity": 0.6,
        } as any,
      });

      // 3. Critical Infrastructure Source & Layer
      map.addSource("infrastructure-source", {
        type: "geojson",
        data: INFRASTRUCTURE_GEOJSON,
      });

      map.addLayer({
        id: "infrastructure-points",
        type: "circle",
        source: "infrastructure-source",
        paint: {
          "circle-radius": 7,
          "circle-color": [
            "match",
            ["get", "type"],
            "HOSPITAL",
            "#ef4444",
            "POWER_STATION",
            "#f59e0b",
            "BRIDGE",
            "#f97316",
            "#3b82f6",
          ],
          "circle-stroke-width": 2,
          "circle-stroke-color": "#ffffff",
        },
      });

      // 4. Rescue Fleet Source & Layer
      map.addSource("rescue-fleet-source", {
        type: "geojson",
        data: RESCUE_FLEET_GEOJSON,
      });

      map.addLayer({
        id: "rescue-fleet-points",
        type: "circle",
        source: "rescue-fleet-source",
        paint: {
          "circle-radius": 8,
          "circle-color": "#10b981",
          "circle-stroke-width": 2,
          "circle-stroke-color": "#064e3b",
        },
      });

      // Cursor tracking
      map.on("mousemove", (e) => {
        setCursorCoords({
          lat: Number(e.lngLat.lat.toFixed(4)),
          lng: Number(e.lngLat.lng.toFixed(4)),
        });
      });

      map.on("zoom", () => {
        setCurrentZoom(Number(map.getZoom().toFixed(1)));
      });

      // Interactive Click Popups
      const setupPopup = (layerId: string, titleField: string, descField: string) => {
        map.on("click", layerId, (e) => {
          if (!e.features || !e.features[0]) return;
          const feature = e.features[0];
          const props = feature.properties as any;
          const coordinates = (feature.geometry as any).coordinates.slice();

          new maplibregl.Popup()
            .setLngLat(coordinates)
            .setHTML(
              `<div class="p-1">
                <h4 class="font-bold text-xs font-mono text-cyan-400 uppercase tracking-wide">${props[titleField] || props.name || "Incident Asset"}</h4>
                <p class="text-xs text-slate-300 mt-1 leading-relaxed">${props[descField] || props.details || props.assigned_task || ""}</p>
                <div class="mt-2 pt-1 border-t border-slate-700 text-[10px] font-mono text-slate-400">
                  Status: <span class="text-emerald-400">${props.status || "ACTIVE"}</span>
                </div>
              </div>`
            )
            .addTo(map);

          if (onFeatureClick) onFeatureClick(props);
        });

        map.on("mouseenter", layerId, () => {
          map.getCanvas().style.cursor = "pointer";
        });
        map.on("mouseleave", layerId, () => {
          map.getCanvas().style.cursor = "";
        });
      };

      setupPopup("infrastructure-points", "name", "details");
      setupPopup("rescue-fleet-points", "name", "assigned_task");
    });

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Update Layer Visibility
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !map.isStyleLoaded()) return;

    if (map.getLayer("inundation-fill")) {
      map.setLayoutProperty("inundation-fill", "visibility", layers.inundation ? "visible" : "none");
      map.setLayoutProperty("inundation-stroke", "visibility", layers.inundation ? "visible" : "none");
    }
    if (map.getLayer("hexgrid-fill")) {
      map.setLayoutProperty("hexgrid-fill", "visibility", layers.riskHexgrid ? "visible" : "none");
      map.setLayoutProperty("hexgrid-line", "visibility", layers.riskHexgrid ? "visible" : "none");
    }
    if (map.getLayer("infrastructure-points")) {
      map.setLayoutProperty("infrastructure-points", "visibility", layers.infrastructure ? "visible" : "none");
    }
    if (map.getLayer("rescue-fleet-points")) {
      map.setLayoutProperty("rescue-fleet-points", "visibility", layers.rescueFleet ? "visible" : "none");
    }
  }, [layers]);

  const handleZoomIn = () => mapRef.current?.zoomIn();
  const handleZoomOut = () => mapRef.current?.zoomOut();
  const handleReset = () => {
    mapRef.current?.flyTo({
      center: initialCenter,
      zoom: initialZoom,
      pitch: 0,
      bearing: 0,
      essential: true,
    });
  };

  const toggleLayer = (key: keyof typeof layers) => {
    setLayers((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className={`relative rounded-2xl overflow-hidden border border-surface-border bg-[#070b12] shadow-2xl ${className}`}>
      {/* MapLibre DOM Container */}
      <div ref={mapContainer} className="w-full h-full min-h-[420px]" />

      {/* Top Left: Active Operational Map Badge */}
      <div className="absolute top-3 left-3 z-10 flex items-center gap-2">
        <div className="px-3 py-1.5 rounded-xl bg-[#090d16]/90 backdrop-blur-md border border-cyan-500/40 shadow-lg flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
          <span className="text-xs font-mono font-bold text-slate-100">
            Assam Barpeta Sector #4 • EPSG:4326
          </span>
        </div>
      </div>

      {/* Top Right: Layer Manager Toggle HUD */}
      <div className="absolute top-3 right-3 z-10 flex flex-col gap-1.5 max-w-[200px]">
        <div className="p-2.5 rounded-xl bg-[#090d16]/90 backdrop-blur-md border border-surface-border shadow-xl space-y-1.5 text-xs font-mono">
          <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-300 pb-1 border-b border-surface-border">
            <Layers className="w-3.5 h-3.5 text-cyan-400" />
            <span>GIS Operational Layers</span>
          </div>

          <button
            onClick={() => toggleLayer("inundation")}
            className={`w-full flex items-center justify-between px-2 py-1 rounded transition-colors ${
              layers.inundation ? "bg-cyan-500/20 text-cyan-300" : "text-slate-500"
            }`}
          >
            <span>Flood Inundation</span>
            {layers.inundation ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
          </button>

          <button
            onClick={() => toggleLayer("riskHexgrid")}
            className={`w-full flex items-center justify-between px-2 py-1 rounded transition-colors ${
              layers.riskHexgrid ? "bg-amber-500/20 text-amber-300" : "text-slate-500"
            }`}
          >
            <span>H3 Risk Hexgrid</span>
            {layers.riskHexgrid ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
          </button>

          <button
            onClick={() => toggleLayer("infrastructure")}
            className={`w-full flex items-center justify-between px-2 py-1 rounded transition-colors ${
              layers.infrastructure ? "bg-rose-500/20 text-rose-300" : "text-slate-500"
            }`}
          >
            <span>Hospitals & Power</span>
            {layers.infrastructure ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
          </button>

          <button
            onClick={() => toggleLayer("rescueFleet")}
            className={`w-full flex items-center justify-between px-2 py-1 rounded transition-colors ${
              layers.rescueFleet ? "bg-emerald-500/20 text-emerald-300" : "text-slate-500"
            }`}
          >
            <span>Rescue Fleet</span>
            {layers.rescueFleet ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
          </button>
        </div>
      </div>

      {/* Bottom Right: Zoom & Navigation Controls */}
      <div className="absolute bottom-10 right-3 z-10 flex flex-col gap-1.5">
        <div className="flex flex-col bg-[#090d16]/90 backdrop-blur-md rounded-xl border border-surface-border shadow-xl overflow-hidden">
          <button
            onClick={handleZoomIn}
            className="p-2 text-slate-300 hover:text-white hover:bg-slate-800 transition-colors border-b border-surface-border/60"
            title="Zoom In"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={handleZoomOut}
            className="p-2 text-slate-300 hover:text-white hover:bg-slate-800 transition-colors border-b border-surface-border/60"
            title="Zoom Out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={handleReset}
            className="p-2 text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
            title="Fit to Epicenter"
          >
            <Crosshair className="w-4 h-4 text-cyan-400" />
          </button>
        </div>
      </div>

      {/* Bottom Left: Live HUD Coordinates Inspector */}
      <div className="absolute bottom-3 left-3 z-10 flex items-center gap-2">
        <div className="px-3 py-1 rounded-lg bg-[#090d16]/90 backdrop-blur-md border border-surface-border text-[10px] font-mono text-slate-400 flex items-center gap-3 shadow-lg">
          <span>
            Cursor: <strong className="text-slate-200">{cursorCoords ? `${cursorCoords.lat}° N, ${cursorCoords.lng}° E` : "26.3216° N, 91.0063° E"}</strong>
          </span>
          <span>
            Zoom: <strong className="text-cyan-400">{currentZoom}x</strong>
          </span>
          <span className="text-emerald-400 font-bold">WGS84 GPS READY</span>
        </div>
      </div>
    </div>
  );
};
