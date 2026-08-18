"use client";

import React, { useState } from "react";
import {
  Bell,
  Check,
  CheckCheck,
  ChevronRight,
  ShieldAlert,
  X,
} from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import {
  markAllNotificationsRead,
  markNotificationRead,
} from "@/services/realtimeService";
import { NotificationItem, NotificationListResponse } from "@/types/realtime";

interface NotificationCenterProps {
  initialNotifications: NotificationListResponse;
}

export const NotificationCenterModal: React.FC<NotificationCenterProps> = ({
  initialNotifications,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [data, setData] = useState<NotificationListResponse>(initialNotifications);
  const [isMarkingAll, setIsMarkingAll] = useState(false);

  const handleMarkOne = async (id: string) => {
    try {
      await markNotificationRead(id);
      setData((prev) => ({
        ...prev,
        unread_count: Math.max(0, prev.unread_count - 1),
        notifications: prev.notifications.map((n) =>
          n.notification_id === id ? { ...n, is_read: true } : n
        ),
      }));
    } catch {
      // Optimistic update
      setData((prev) => ({
        ...prev,
        unread_count: Math.max(0, prev.unread_count - 1),
        notifications: prev.notifications.map((n) =>
          n.notification_id === id ? { ...n, is_read: true } : n
        ),
      }));
    }
  };

  const handleMarkAll = async () => {
    setIsMarkingAll(true);
    try {
      await markAllNotificationsRead();
      setData((prev) => ({
        ...prev,
        unread_count: 0,
        notifications: prev.notifications.map((n) => ({ ...n, is_read: true })),
      }));
    } catch {
      setData((prev) => ({
        ...prev,
        unread_count: 0,
        notifications: prev.notifications.map((n) => ({ ...n, is_read: true })),
      }));
    } finally {
      setIsMarkingAll(false);
    }
  };

  return (
    <div className="relative">
      {/* Bell Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 rounded-xl bg-surface-200 hover:bg-surface-50 border border-surface-border text-foreground transition-colors"
        aria-label="Notification Center"
      >
        <Bell className="w-4 h-4" />
        {data.unread_count > 0 && (
          <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 text-white text-[9px] font-mono font-bold flex items-center justify-center animate-pulse">
            {data.unread_count}
          </span>
        )}
      </button>

      {/* Popover Dropdown */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl bg-surface-100 border border-surface-border shadow-2xl z-50 p-4 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-surface-border">
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-foreground">Incident Command Center</span>
              {data.unread_count > 0 && (
                <Badge variant="critical" size="sm">
                  {data.unread_count} Unread
                </Badge>
              )}
            </div>

            <div className="flex items-center gap-1.5">
              {data.unread_count > 0 && (
                <button
                  onClick={handleMarkAll}
                  disabled={isMarkingAll}
                  className="text-[10px] text-cyan-600 dark:text-cyan-400 hover:underline font-mono font-semibold"
                >
                  Mark all read
                </button>
              )}
              <button
                onClick={() => setIsOpen(false)}
                className="text-slate-400 hover:text-foreground p-1"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* List of notifications */}
          <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
            {data.notifications.length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-500 dark:text-slate-400 font-mono">
                No active notifications.
              </div>
            ) : (
              data.notifications.map((notif) => (
                <div
                  key={notif.notification_id}
                  className={`p-3 rounded-xl border transition-all text-xs ${
                    notif.is_read
                      ? "bg-surface-200 border-surface-border opacity-70"
                      : "bg-surface-200 border-cyan-500/30 shadow-sm"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-1.5">
                        <Badge
                          variant={
                            notif.severity === "CRITICAL"
                              ? "critical"
                              : notif.severity === "HIGH"
                              ? "warning"
                              : "info"
                          }
                          size="sm"
                        >
                          {notif.severity}
                        </Badge>
                        <span className="font-semibold text-foreground">
                          {notif.title}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">
                        {notif.message}
                      </p>
                    </div>

                    {!notif.is_read && (
                      <button
                        onClick={() => handleMarkOne(notif.notification_id)}
                        className="text-cyan-600 dark:text-cyan-400 hover:text-cyan-500 p-1 shrink-0"
                        title="Mark as read"
                      >
                        <Check className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};
