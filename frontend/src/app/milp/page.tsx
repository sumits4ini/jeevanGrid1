"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Activity,
  CheckCircle2,
  Compass,
  Cpu,
  FileCheck,
  Layers,
  MapPin,
  RefreshCw,
  Shield,
  Truck,
  Zap,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { ResponsePlanCard } from "@/components/dashboard/ResponsePlanCard";
import { fetchResponsePlan } from "@/services/optimizationService";
import { ResponsePlanResponse } from "@/types/optimization";

export default function MILPOptimizationPage() {
  const [plan, setPlan] = useState<ResponsePlanResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchResponsePlan()
      .then((data) => {
        setPlan(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6 pb-12">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-surface-100 border border-surface-border shadow-xl">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse" />
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-slate-100 dark:text-slate-100 light:text-slate-900">
              MILP Response Optimization & Dispatch Solver
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Deterministic Mixed-Integer Linear Programming resource allocation and multi-incident transit routing
          </p>
        </div>

        <Link href="/gis">
          <Button size="sm" variant="primary" icon={<Layers className="w-3.5 h-3.5" />}>
            View Routes on GIS Map
          </Button>
        </Link>
      </div>

      {/* MILP Solver Mathematical Formulation Card */}
      <Card className="border-cyan-500/30 bg-surface-100 p-5 space-y-3 shadow-xl">
        <div className="flex items-center gap-2 text-xs font-bold text-slate-200 font-mono">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <span>MILP Objective Function & Constraint Formulation</span>
        </div>
        <div className="p-3.5 rounded-xl bg-surface-200 border border-surface-border text-xs font-mono text-cyan-300 space-y-1.5 overflow-x-auto">
          <div>{"min Z = ∑ ∑ ( c_ij · x_ij + w_i · Shortage_i )"}</div>
          <div className="text-[11px] text-slate-400 pt-1">
            {"Subject to: Capacity constraints ∑ x_ij ≤ Cap_j, demand balance ∑ x_ij + Shortage_i = D_i, and x_ij ∈ {0, 1}."}
          </div>
        </div>
      </Card>

      {/* Main Response Plan Card */}
      {plan && <ResponsePlanCard initialPlan={plan} />}
    </div>
  );
}
