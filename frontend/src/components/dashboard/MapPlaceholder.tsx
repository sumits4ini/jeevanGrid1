"use client";

import React from "react";
import { GISMap } from "@/components/gis/GISMap";

export const MapPlaceholder: React.FC = () => {
  return (
    <div className="w-full h-[460px] rounded-2xl overflow-hidden shadow-2xl border border-surface-border">
      <GISMap initialCenter={[91.0063, 26.3216]} initialZoom={11.5} />
    </div>
  );
};
