"use client";

import React, { useEffect, useState } from "react";
import { Bell, Play, RefreshCw, ShieldAlert, User } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export const Header: React.FC = () => {
  const [timeStr, setTimeStr] = useState<string>("");

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
            DEFCON 2 • HIGH ALERT
          </Badge>
          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-surface-200 border border-surface-border text-xs text-slate-300 font-mono">
            <Play className="w-3 h-3 text-cyan-400 fill-cyan-400" />
            <span>Scenario: Assam Brahmaputra 2026</span>
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

        {/* Notifications Bell */}
        <button
          className="relative p-2 rounded-lg bg-surface-200 border border-surface-border text-slate-300 hover:text-slate-100 hover:bg-surface-100 transition-colors"
          title="Critical Alerts (3 Unacknowledged)"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 text-[10px] font-bold flex items-center justify-center text-white ring-2 ring-background">
            3
          </span>
        </button>

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
