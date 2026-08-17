"use client";

import React from "react";
import Link from "next/link";
import { AlertOctagon, Compass, Home, Shield } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center text-center px-4">
      <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-rose-500/20 to-red-600/30 border border-rose-500/40 flex items-center justify-center text-rose-400 mb-4 shadow-2xl animate-pulse">
        <AlertOctagon className="w-8 h-8" />
      </div>

      <div className="text-xs font-mono text-rose-400 uppercase tracking-widest font-bold">
        HTTP 404 • UNKNOWN INCIDENT SECTOR
      </div>

      <h1 className="text-2xl lg:text-3xl font-bold text-slate-100 mt-2">
        Operational Telemetry Route Not Found
      </h1>

      <p className="text-xs text-slate-400 max-w-md mt-2 leading-relaxed">
        The requested tactical coordinate or operational URL does not exist in the active JeevanGrid registry.
      </p>

      <div className="flex items-center gap-3 mt-6">
        <Link href="/">
          <Button size="md" variant="primary" icon={<Home className="w-4 h-4" />}>
            Return to Command Center
          </Button>
        </Link>
        <Link href="/gis">
          <Button size="md" variant="secondary" icon={<Compass className="w-4 h-4" />}>
            Open GIS Viewport
          </Button>
        </Link>
      </div>
    </div>
  );
}
