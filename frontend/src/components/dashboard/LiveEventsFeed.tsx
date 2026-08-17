"use client";

import React, { useState } from "react";
import {
  Activity,
  AlertTriangle,
  Bot,
  Compass,
  FileCheck,
  Flame,
  Radio,
  RefreshCw,
  Shield,
  Truck,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { useRealtimeOperations } from "@/hooks/useRealtimeOperations";
import { fetchOperationalEvents } from "@/services/realtimeService";
import { OperationalEvent } from "@/types/realtime";

interface LiveEventsFeedProps {
  initialEvents: OperationalEvent[];
}

export const LiveEventsFeed: React.FC<LiveEventsFeedProps> = ({ initialEvents }) => {
  const [events, setEvents] = useState<OperationalEvent[]>(initialEvents);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const { latestEvent } = useRealtimeOperations();

  // Listen for live events over WebSocket
  React.useEffect(() => {
    if (latestEvent) {
      setEvents((prev) => [latestEvent, ...prev.slice(0, 49)]);
    }
  }, [latestEvent]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      const data = await fetchOperationalEvents(20);
      setEvents(data);
    } catch {
      // Keep existing
    } finally {
      setIsRefreshing(false);
    }
  };

  const getEventIcon = (eventType: string) => {
    if (eventType.includes("DISASTER")) {
      return <Flame className="w-3.5 h-3.5 text-rose-400" />;
    } else if (eventType.includes("RISK")) {
      return <Bot className="w-3.5 h-3.5 text-cyan-400" />;
    } else if (eventType.includes("RESOURCE")) {
      return <Truck className="w-3.5 h-3.5 text-emerald-400" />;
    } else if (eventType.includes("PLAN")) {
      return <Compass className="w-3.5 h-3.5 text-amber-400" />;
    } else {
      return <Activity className="w-3.5 h-3.5 text-slate-400" />;
    }
  };

  return (
    <Card className="border-surface-border bg-surface-100/90 shadow-xl">
      <div className="flex items-center justify-between pb-3 border-b border-surface-border">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-cyan-400" />
          <h4 className="text-sm font-bold text-slate-100">Live Operational Telemetry Stream</h4>
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
        </div>

        <Button
          size="sm"
          variant="secondary"
          onClick={handleRefresh}
          disabled={isRefreshing}
          icon={<RefreshCw className={`w-3 h-3 ${isRefreshing ? "animate-spin" : ""}`} />}
        >
          Sync
        </Button>
      </div>

      <div className="mt-3 space-y-2.5 max-h-[360px] overflow-y-auto pr-1">
        {events.length === 0 ? (
          <div className="p-6 text-center text-xs text-slate-500 font-mono">
            No operational events recorded yet.
          </div>
        ) : (
          events.map((evt) => (
            <div
              key={evt.event_id}
              className="p-3 rounded-lg bg-surface-200/60 border border-surface-border/60 flex items-start justify-between gap-3 text-xs"
            >
              <div className="flex items-start gap-2.5">
                <div className="w-6 h-6 rounded bg-surface-100 border border-surface-border flex items-center justify-center shrink-0 mt-0.5">
                  {getEventIcon(evt.event_type)}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-200 font-mono">
                      {evt.event_type}
                    </span>
                    <Badge variant={evt.severity === "CRITICAL" ? "critical" : "default"} size="sm">
                      {evt.severity}
                    </Badge>
                  </div>
                  <span className="text-[11px] text-slate-400 mt-0.5 block">
                    Source: <strong className="text-cyan-400">{evt.source}</strong> • Entity: {evt.entity_id}
                  </span>
                </div>
              </div>

              <span className="text-[10px] text-slate-500 font-mono shrink-0">
                {new Date(evt.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))
        )}
      </div>
    </Card>
  );
};
