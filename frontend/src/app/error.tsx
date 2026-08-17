"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { AlertOctagon, Home, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorBoundary({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log client error safely without exposing credentials
    console.error("JeevanGrid Application Error:", error.message);
  }, [error]);

  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center text-center px-4">
      <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-rose-500/20 to-red-600/30 border border-rose-500/40 flex items-center justify-center text-rose-400 mb-4 shadow-2xl animate-pulse">
        <AlertOctagon className="w-8 h-8" />
      </div>

      <div className="text-xs font-mono text-rose-400 uppercase tracking-widest font-bold">
        EOC SYSTEM EXCEPTION INTERCEPTED
      </div>

      <h1 className="text-2xl lg:text-3xl font-bold text-slate-100 dark:text-slate-100 light:text-slate-900 mt-2">
        Operational Viewport Encountered an Issue
      </h1>

      <p className="text-xs text-slate-400 max-w-md mt-2 leading-relaxed">
        {error.message || "An unexpected error occurred while rendering telemetry components. Pre-cached data remains secure."}
      </p>

      <div className="flex items-center gap-3 mt-6">
        <Button
          size="md"
          variant="primary"
          onClick={() => reset()}
          icon={<RefreshCw className="w-4 h-4" />}
        >
          Retry Viewport
        </Button>
        <Link href="/">
          <Button size="md" variant="secondary" icon={<Home className="w-4 h-4" />}>
            Return to Command Center
          </Button>
        </Link>
      </div>
    </div>
  );
}
