import { describe, it, expect } from "vitest";
import { fetchResponsePlan } from "@/services/optimizationService";

describe("MILP Optimization Service Client", () => {
  it("returns Pareto-optimal response plan and dispatch routes", async () => {
    const plan = await fetchResponsePlan();
    expect(plan).toBeDefined();
    expect(plan.plan_id).toBeDefined();
    expect(plan.plan_summary).toBeDefined();
    expect(plan.plan_summary.total_incidents).toBeGreaterThanOrEqual(1);
    expect(plan.plan_summary.total_units_allocated).toBeGreaterThanOrEqual(1);
    expect(plan.allocations).toBeInstanceOf(Array);
    expect(plan.deployment_sequence).toBeInstanceOf(Array);

    if (plan.deployment_sequence.length > 0) {
      const order = plan.deployment_sequence[0];
      expect(order.deployment_order).toBeGreaterThanOrEqual(1);
      expect(order.resource_code).toBeDefined();
      expect(order.staging_point).toBeDefined();
      expect(order.estimated_eta_minutes).toBeGreaterThan(0);
    }
  });
});
