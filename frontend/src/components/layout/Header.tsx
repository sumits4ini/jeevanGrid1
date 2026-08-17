"use client";

import React, { useEffect, useState } from "react";
import {
  Moon,
  Play,
  RefreshCw,
  Search,
  Sun,
  User,
  Wifi,
  WifiOff,
} from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { NotificationCenterModal } from "@/components/dashboard/NotificationCenterModal";
import { GlobalSearchModal } from "@/components/layout/GlobalSearchModal";
import { useTheme } from "@/context/ThemeContext";
import { useEOC } from "@/context/EOCContext";

export const Header: React.FC = () => {
  const [timeStr, setTimeStr] = useState<string>("");
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const {
    connectionStatus,
    secondsSinceSync,
    isRefreshing,
    refreshAll,
    operationsStatus,
  } = useEOC();

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(
        now.toLocaleTimeString("en-IN", {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: false,
          timeZone: "Asia/Kolkata",
        }) + " IST"
      );
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // Global Ctrl+K Listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        setIsSearchOpen((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <>
      <header className="h-16 bg-[#080d17]/90 dark:bg-[#080d17]/90 light:bg-white/90 backdrop-blur-md border-b border-surface-border sticky top-0 z-30 px-4 lg:px-6 flex items-center justify-between gap-4">
        {/* Left: Operational Alert Status & Scenario Info */}
        <div className="flex items-center gap-3 pl-10 lg:pl-0">
          <div className="flex items-center gap-2">
            <Badge variant="critical" size="md" dot>
              {operationsStatus.system_readiness_status === "CRITICAL_DEFCON_1"
                ? "DEFCON 1 • CRITICAL SURGE"
                : "DEFCON 2 • HIGH ALERT"}
            </Badge>

            <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-surface-200 border border-surface-border text-xs text-slate-300 dark:text-slate-300 light:text-slate-700 font-mono">
              <Play className="w-3 h-3 text-cyan-400 fill-cyan-400" />
              <span>Assam Brahmaputra 2026</span>
            </div>

            {/* Live Connection Status Badge */}
            <div
              className={`hidden md:flex items-center gap-1.5 px-2 py-0.5 rounded-full border text-[10px] font-mono ${
                connectionStatus === "CONNECTED"
                  ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                  : connectionStatus === "RECONNECTING"
                  ? "bg-amber-500/10 border-amber-500/30 text-amber-400"
                  : "bg-rose-500/10 border-rose-500/30 text-rose-400"
              }`}
            >
              <span
                className={`w-1.5 h-1.5 rounded-full ${
                  connectionStatus === "CONNECTED"
                    ? "bg-emerald-400 animate-pulse"
                    : connectionStatus === "RECONNECTING"
                    ? "bg-amber-400 animate-ping"
                    : "bg-rose-400"
                }`}
              />
              <span>
                {connectionStatus === "CONNECTED"
                  ? "WS/1.1 LIVE STREAM"
                  : connectionStatus === "RECONNECTING"
                  ? "RECONNECTING..."
                  : "OFFLINE SYNC"}
              </span>
            </div>
          </div>
        </div>

        {/* Right: OmniSearch, Refresh, Telemetry Clock, Theme, Notifications & Commander Profile */}
        <div className="flex items-center gap-2.5">
          {/* Omni Global Search Trigger */}
          <button
            onClick={() => setIsSearchOpen(true)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-surface-200 hover:bg-surface-100 border border-surface-border text-xs font-mono text-slate-300 transition-colors"
            title="Search Incidents, Assets, Coordinates (Ctrl+K)"
          >
            <Search className="w-3.5 h-3.5 text-cyan-400" />
            <span className="hidden md:inline">Search EOC</span>
            <kbd className="hidden md:inline-block px-1.5 py-0.2 rounded bg-surface-100 text-[9px] text-slate-400 border border-surface-border">
              Ctrl+K
            </kbd>
          </button>

          {/* Manual Telemetry Sync Button */}
          <button
            onClick={() => refreshAll()}
            disabled={isRefreshing}
            className="p-2 rounded-xl bg-surface-200 hover:bg-surface-100 border border-surface-border text-slate-300 hover:text-cyan-400 transition-colors"
            title={`Last synced ${secondsSinceSync}s ago. Click to refresh.`}
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? "animate-spin text-cyan-400" : ""}`} />
          </button>

          {/* Real-time Clock */}
          <div className="hidden lg:flex flex-col text-right">
            <span className="text-xs font-mono font-semibold text-slate-200 dark:text-slate-200 light:text-slate-800 tracking-wider">
              {timeStr || "12:00:00 IST"}
            </span>
            <span className="text-[10px] text-slate-500 font-mono">
              SYNCED {secondsSinceSync}S AGO
            </span>
          </div>

          <div className="h-6 w-px bg-surface-border hidden md:block" />

          {/* Theme Toggle Button */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-xl bg-surface-200 border border-surface-border text-slate-300 hover:text-slate-100 hover:bg-surface-100 transition-colors"
            title={`Switch to ${theme === "dark" ? "Light" : "Dark"} Mode`}
            aria-label="Toggle Theme"
          >
            {theme === "dark" ? (
              <Sun className="w-4 h-4 text-amber-400" />
            ) : (
              <Moon className="w-4 h-4 text-indigo-400" />
            )}
          </button>

          {/* In-App Notification Center */}
          <NotificationCenterModal
            initialNotifications={{
              total_notifications: 3,
              unread_count: 2,
              notifications: [
                {
                  notification_id: "notif-01",
                  recipient_role: "EOC_COMMANDER",
                  title: "Severe Flood Inundation Alert — Barpeta Sector East",
                  message: "Water levels exceeded 1.25m benchmark at Ward 4 residential cluster.",
                  severity: "CRITICAL",
                  related_alert_id: "alert-01",
                  is_read: false,
                  created_at: new Date().toISOString(),
                },
                {
                  notification_id: "notif-02",
                  recipient_role: "DISPATCHER",
                  title: "NDRF Rescue Fleet Dispatched",
                  message: "Boats Alpha-1 and Alpha-2 mobilized to eastern riverine slipway.",
                  severity: "INFO",
                  is_read: false,
                  created_at: new Date().toISOString(),
                },
                {
                  notification_id: "notif-03",
                  recipient_role: "ALL",
                  title: "Hospital Backup Power Reserve Alert",
                  message: "Civil Hospital primary substation on backup fuel reserves (6h remaining).",
                  severity: "HIGH",
                  related_alert_id: "alert-02",
                  is_read: true,
                  created_at: new Date().toISOString(),
                  read_at: new Date().toISOString(),
                },
              ],
            }}
          />

          {/* Incident Commander User Pill */}
          <div className="flex items-center gap-2 pl-2 border-l border-surface-border">
            <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-cyan-400">
              <User className="w-4 h-4" />
            </div>
            <div className="hidden lg:flex flex-col text-left">
              <span className="text-xs font-semibold text-slate-200 dark:text-slate-200 light:text-slate-800 leading-tight">
                DEOC Commander
              </span>
              <span className="text-[10px] text-slate-400 font-mono">
                Barpeta District
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Global Search Modal */}
      <GlobalSearchModal isOpen={isSearchOpen} onClose={() => setIsSearchOpen(false)} />
    </>
  );
};
