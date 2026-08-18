"use client";

import React, { Suspense } from "react";
import { GISMap } from "@/components/gis/GISMap";

export const MapPlaceholder: React.FC = () => {
  return (
    <div className="w-full h-[460px] rounded-2xl overflow-hidden shadow-2xl border border-surface-border">
      <Suspense
        fallback={
          <div className="w-full h-full flex items-center justify-center bg-surface-300 text-xs font-mono text-slate-500 dark:text-slate-400">
            Initializing MapLibre GL JS Engine...
          </div>
        }
      >
        <GISMap initialCenter={[91.0063, 26.3216]} initialZoom={11.5} />
      </Suspense>
    </div>
  );
};
