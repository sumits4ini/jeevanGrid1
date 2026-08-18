"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  Compass,
  Cpu,
  Layers,
  MapPin,
  Menu,
  Radio,
  Settings,
  Shield,
  Truck,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/Badge";

interface NavItem {
  label: string;
  href: string;
  icon: React.ElementType;
  badge?: string;
  badgeVariant?: "default" | "critical" | "warning" | "success" | "brand";
}

const NAV_ITEMS: NavItem[] = [
  { label: "Command Dashboard", href: "/", icon: Activity },
  { label: "Disaster Intelligence", href: "/disasters", icon: AlertTriangle, badge: "2 Active", badgeVariant: "critical" },
  { label: "GIS / Map Viewport", href: "/gis", icon: Layers, badge: "Vector", badgeVariant: "brand" },
  { label: "Risk Zones (MCDA)", href: "/risk-zones", icon: MapPin, badge: "H3 Hex", badgeVariant: "warning" },
  { label: "Emergency Resources", href: "/resources", icon: Truck, badge: "18 Avail", badgeVariant: "success" },
  { label: "MILP Optimization", href: "/milp", icon: Compass },
  { label: "System Telemetry", href: "/telemetry", icon: Cpu, badge: "Ready", badgeVariant: "default" },
  { label: "Settings & Config", href: "/settings", icon: Settings },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setMobileOpen(true)}
        className="lg:hidden fixed top-3 left-3 z-50 p-2 rounded-lg bg-surface-100 border border-surface-border text-foreground shadow-md"
        aria-label="Open Navigation Menu"
      >
        <Menu className="w-5 h-5" />
      </button>

      {/* Mobile Backdrop */}
      {mobileOpen && (
        <div
          onClick={() => setMobileOpen(false)}
          className="lg:hidden fixed inset-0 z-40 bg-black/60 backdrop-blur-sm transition-opacity"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={cn(
          "fixed top-0 left-0 z-40 h-screen bg-surface-300 border-r border-surface-border flex flex-col justify-between transition-all duration-300 ease-in-out shadow-xl",
          collapsed ? "w-20" : "w-64",
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        {/* Top Branding Section */}
        <div>
          <div className="h-16 flex items-center justify-between px-4 border-b border-surface-border">
            <Link href="/" className="flex items-center gap-3 overflow-hidden">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-700 flex items-center justify-center text-white shadow-lg shadow-cyan-950/30 shrink-0">
                <Shield className="w-5 h-5" />
              </div>
              {!collapsed && (
                <div className="flex flex-col min-w-0">
                  <span className="text-sm font-bold tracking-wider text-foreground flex items-center gap-1.5">
                    JEEVAN<span className="text-cyan-500 dark:text-cyan-400">GRID</span>
                  </span>
                  <span className="text-[10px] uppercase font-mono tracking-widest text-slate-500 dark:text-slate-400">
                    Disaster Intel EOC
                  </span>
                </div>
              )}
            </Link>

            {/* Mobile Close Button */}
            <button
              onClick={() => setMobileOpen(false)}
              className="lg:hidden text-slate-500 hover:text-foreground"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Operational Status Pill in Sidebar */}
          {!collapsed && (
            <div className="mx-3 my-3 p-2.5 rounded-lg bg-surface-200 border border-surface-border">
              <div className="flex items-center justify-between text-[11px]">
                <span className="text-slate-500 dark:text-slate-400 font-mono">INCIDENT EOC</span>
                <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  ONLINE
                </span>
              </div>
              <p className="text-[11px] text-foreground font-semibold mt-1 truncate">
                Assam Barpeta Sector #4
              </p>
            </div>
          )}

          {/* Navigation Links */}
          <nav className="p-2 space-y-1">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive =
                pathname === item.href ||
                (item.href === "/risk-zones" && pathname === "/risk") ||
                (item.href === "/milp" && pathname === "/optimization") ||
                (item.href === "/telemetry" && pathname === "/health");

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all group relative",
                    isActive
                      ? "bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border border-cyan-500/30 shadow-sm font-semibold"
                      : "text-slate-600 dark:text-slate-400 hover:text-foreground hover:bg-surface-200"
                  )}
                >
                  <Icon className={cn("w-4 h-4 shrink-0", isActive ? "text-cyan-600 dark:text-cyan-400" : "text-slate-500 dark:text-slate-400 group-hover:text-foreground")} />
                  {!collapsed && (
                    <span className="flex-1 truncate">{item.label}</span>
                  )}
                  {!collapsed && item.badge && (
                    <Badge variant={item.badgeVariant || "default"} size="sm">
                      {item.badge}
                    </Badge>
                  )}
                  {collapsed && (
                    <div className="absolute left-full ml-2 px-2 py-1 bg-surface-100 text-foreground text-xs rounded-md shadow-lg border border-surface-border whitespace-nowrap opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-opacity z-50">
                      {item.label}
                    </div>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Bottom Section: Collapse Toggle & Version */}
        <div className="p-3 border-t border-surface-border">
          <div className="flex items-center justify-between">
            {!collapsed && (
              <div className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                SIH 2026 • v1.0.0-Release
              </div>
            )}
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="hidden lg:flex items-center justify-center p-1.5 rounded-lg text-slate-500 hover:text-foreground hover:bg-surface-200 transition-colors"
              title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            >
              {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </aside>
    </>
  );
};
