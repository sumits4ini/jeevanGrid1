"use client";

import React from "react";
import { Activity, Radio, Shield } from "lucide-react";

export default function Loading() {
  return (
    <div className="space-y-6 pb-12 animate-pulse">
      {/* Top Banner Skeleton */}
      <div className="h-24 rounded-2xl bg-surface-100/60 border border-surface-border p-5 flex items-center justify-between" />

      {/* KPI Overview Strip Skeleton */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="h-20 rounded-xl bg-surface-100/60 border border-surface-border" />
        ))}
      </div>

      {/* Main Grid Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        <div className="lg:col-span-8 space-y-6">
          <div className="h-[460px] rounded-2xl bg-surface-100/60 border border-surface-border" />
          <div className="h-64 rounded-2xl bg-surface-100/60 border border-surface-border" />
        </div>
        <div className="lg:col-span-4 space-y-6">
          <div className="h-80 rounded-2xl bg-surface-100/60 border border-surface-border" />
          <div className="h-64 rounded-2xl bg-surface-100/60 border border-surface-border" />
        </div>
      </div>
    </div>
  );
}
