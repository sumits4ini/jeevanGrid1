import React from "react";
import { cn } from "@/lib/utils";

export type StatusType = "healthy" | "ready" | "configured" | "degraded" | "offline" | "critical";

export const StatusIndicator: React.FC<{
  status: StatusType;
  label?: string;
  className?: string;
}> = ({ status, label, className }) => {
  const statusConfig: Record<StatusType, { bg: string; text: string; labelDefault: string }> = {
    healthy: { bg: "bg-emerald-500", text: "text-emerald-600 dark:text-emerald-400", labelDefault: "Healthy" },
    ready: { bg: "bg-cyan-500 dark:bg-cyan-400", text: "text-cyan-600 dark:text-cyan-400", labelDefault: "Ready" },
    configured: { bg: "bg-blue-500 dark:bg-blue-400", text: "text-blue-600 dark:text-blue-400", labelDefault: "Configured" },
    degraded: { bg: "bg-amber-500 dark:bg-amber-400", text: "text-amber-600 dark:text-amber-400", labelDefault: "Degraded" },
    offline: { bg: "bg-slate-400 dark:bg-slate-500", text: "text-slate-600 dark:text-slate-400", labelDefault: "Offline" },
    critical: { bg: "bg-rose-500", text: "text-rose-600 dark:text-rose-400", labelDefault: "Critical" },
  };

  const current = statusConfig[status] || statusConfig.offline;

  return (
    <div className={cn("inline-flex items-center gap-2", className)}>
      <span className="relative flex h-2 w-2">
        {status === "healthy" || status === "critical" ? (
          <span className={cn("animate-ping absolute inline-flex h-full w-full rounded-full opacity-75", current.bg)} />
        ) : null}
        <span className={cn("relative inline-flex rounded-full h-2 w-2", current.bg)} />
      </span>
      {label !== undefined ? (
        <span className={cn("text-xs font-medium", current.text)}>{label || current.labelDefault}</span>
      ) : null}
    </div>
  );
};
