"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  AlertTriangle,
  Anchor,
  Compass,
  Crosshair,
  Hospital,
  Layers,
  MapPin,
  Search,
  Shield,
  Truck,
  X,
} from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { useEOC } from "@/context/EOCContext";

interface SearchResultItem {
  id: string;
  title: string;
  category: "INCIDENT" | "RESOURCE" | "RISK_HEX" | "INFRASTRUCTURE";
  subtitle: string;
  url: string;
  icon: React.ElementType;
}

interface GlobalSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const GlobalSearchModal: React.FC<GlobalSearchModalProps> = ({ isOpen, onClose }) => {
  const router = useRouter();
  const { disasters, resources, riskZones } = useEOC();
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);

  // Compile searchable entities from EOC state
  const allItems: SearchResultItem[] = [
    ...disasters.map((d) => ({
      id: d.id,
      title: d.name,
      category: "INCIDENT" as const,
      subtitle: `Level ${d.severity_level} ${d.type} • ${d.affected_population.toLocaleString()} exposed`,
      url: `/gis?incident=${d.id}&lat=${d.latitude}&lng=${d.longitude}`,
      icon: AlertTriangle,
    })),
    ...resources.map((r) => ({
      id: r.id,
      title: `${r.name} [${r.unit_code}]`,
      category: "RESOURCE" as const,
      subtitle: `${r.unit_type} • Status: ${r.status} • ${r.capacity}`,
      url: `/gis?resource=${r.id}&lat=${r.latitude}&lng=${r.longitude}`,
      icon: r.unit_type === "RESCUE_BOAT" ? Anchor : Truck,
    })),
    ...riskZones.map((h) => ({
      id: h.hex_id,
      title: `${h.location_name} (H3: ${h.hex_id})`,
      category: "RISK_HEX" as const,
      subtitle: `Risk Tier: ${h.tier} (${h.risk_score}) • Inundation ${h.inundation_depth_m}m`,
      url: `/gis?hex=${h.hex_id}&lat=${h.latitude}&lng=${h.longitude}`,
      icon: MapPin,
    })),
    {
      id: "loc-hosp-01",
      title: "Barpeta District Civil Hospital",
      category: "INFRASTRUCTURE" as const,
      subtitle: "Trauma Facility • 350 Beds • Backup Power Reserve (6h)",
      url: "/gis?lat=26.3260&lng=91.0110",
      icon: Hospital,
    },
    {
      id: "loc-power-04",
      title: "Barpeta East Substation #4",
      category: "INFRASTRUCTURE" as const,
      subtitle: "33/11 kV Grid Node • Status: Offline/Submerged",
      url: "/gis?lat=26.3180&lng=91.0280",
      icon: Shield,
    },
  ];

  const results = query
    ? allItems.filter(
        (item) =>
          item.title.toLowerCase().includes(query.toLowerCase()) ||
          item.subtitle.toLowerCase().includes(query.toLowerCase()) ||
          item.id.toLowerCase().includes(query.toLowerCase())
      )
    : allItems.slice(0, 6);

  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  // Global Ctrl+K Keyboard Listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        onClose(); // Toggle
      }
      if (!isOpen) return;

      if (e.key === "Escape") {
        onClose();
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedIndex((prev) => (prev < results.length - 1 ? prev + 1 : 0));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((prev) => (prev > 0 ? prev - 1 : results.length - 1));
      } else if (e.key === "Enter" && results[selectedIndex]) {
        e.preventDefault();
        handleSelect(results[selectedIndex]);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, results, selectedIndex]);

  const handleSelect = (item: SearchResultItem) => {
    router.push(item.url);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="w-full max-w-2xl rounded-2xl bg-surface-100 border border-surface-border shadow-2xl overflow-hidden flex flex-col">
        {/* Search Header */}
        <div className="p-4 border-b border-surface-border flex items-center gap-3">
          <Search className="w-5 h-5 text-cyan-400 shrink-0" />
          <input
            type="text"
            autoFocus
            placeholder="Search active incidents, rescue units, H3 hex cells, facilities..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 bg-transparent text-sm text-slate-100 placeholder-slate-500 focus:outline-none font-mono"
          />
          <kbd className="hidden sm:inline-block px-2 py-0.5 rounded bg-surface-200 text-[10px] font-mono text-slate-400 border border-surface-border">
            ESC
          </kbd>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-slate-200">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Results List */}
        <div className="p-2 max-h-96 overflow-y-auto space-y-1">
          {results.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-400 font-mono">
              No matching EOC assets, incidents, or H3 hex cells found for &quot;{query}&quot;.
            </div>
          ) : (
            results.map((item, idx) => {
              const Icon = item.icon;
              const isSelected = idx === selectedIndex;
              return (
                <div
                  key={item.id}
                  onClick={() => handleSelect(item)}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`p-3 rounded-xl flex items-center justify-between gap-3 cursor-pointer transition-colors ${
                    isSelected
                      ? "bg-cyan-500/10 border border-cyan-500/40 text-slate-100"
                      : "text-slate-300 hover:bg-surface-200"
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                        item.category === "INCIDENT"
                          ? "bg-rose-500/20 text-rose-400"
                          : item.category === "RESOURCE"
                          ? "bg-emerald-500/20 text-emerald-400"
                          : item.category === "RISK_HEX"
                          ? "bg-amber-500/20 text-amber-400"
                          : "bg-cyan-500/20 text-cyan-400"
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold font-mono truncate">{item.title}</span>
                      </div>
                      <p className="text-[11px] text-slate-400 truncate mt-0.5">{item.subtitle}</p>
                    </div>
                  </div>

                  <Badge
                    variant={
                      item.category === "INCIDENT"
                        ? "critical"
                        : item.category === "RESOURCE"
                        ? "success"
                        : item.category === "RISK_HEX"
                        ? "warning"
                        : "brand"
                    }
                    size="sm"
                  >
                    {item.category}
                  </Badge>
                </div>
              );
            })
          )}
        </div>

        {/* Footer info */}
        <div className="p-3 bg-surface-200 border-t border-surface-border flex items-center justify-between text-[10px] font-mono text-slate-400">
          <span>Navigate with ↑ ↓ and Press Enter to Focus on Map</span>
          <span className="text-cyan-400 font-semibold">JeevanGrid OmniSearch</span>
        </div>
      </div>
    </div>
  );
};
