"use client";

import React, { useEffect, useState } from "react";
import { Play, User } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { NotificationCenterModal } from "@/components/dashboard/NotificationCenterModal";
import { useRealtimeOperations } from "@/hooks/useRealtimeOperations";

export const Header: React.FC = () => {
  const [timeStr, setTimeStr] = useState<string>("");
  const { status: wsStatus } = useRealtimeOperations();

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

  return (
    <header className="h-16 bg-[#080d17]/90 backdrop-blur-md border-b border-surface-border sticky top-0 z-30 px-4 lg:px-6 flex items-center justify-between gap-4">
      {/* Left: Operational Alert Status & Scenario Info */}
      <div className="flex items-center gap-3 pl-10 lg:pl-0">
        <div className="flex items-center gap-2">
          <Badge variant="critical" size="md" dot>
            DEFCON 1 • CRITICAL SURGE
          </Badge>
          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-surface-200 border border-surface-border text-xs text-slate-300 font-mono">
            <Play className="w-3 h-3 text-cyan-400 fill-cyan-400" />
            <span>Scenario: Assam Brahmaputra 2026</span>
          </div>
          <div className="hidden md:flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[10px] font-mono text-emerald-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>{wsStatus === "CONNECTED" ? "WS/1.1 LIVE" : "RECONNECTING"}</span>
          </div>
        </div>
      </div>

      {/* Right: Telemetry Clock, Notifications & Commander Profile */}
      <div className="flex items-center gap-3">
        {/* Real-time Clock */}
        <div className="hidden md:flex flex-col text-right">
          <span className="text-xs font-mono font-semibold text-slate-200 tracking-wider">
            {timeStr || "12:00:00 IST"}
          </span>
          <span className="text-[10px] text-slate-500 font-mono">DISASTER CLOCK</span>
        </div>

        <div className="h-6 w-px bg-surface-border hidden md:block" />

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
            <span className="text-xs font-semibold text-slate-200 leading-tight">
              DEOC Commander
            </span>
            <span className="text-[10px] text-slate-400 font-mono">
              Barpeta District
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};
