# 05. SIH 2026 Live Demo Playbook & Presentation Strategy

## 1. The Core Narrative Arc (5-Minute Winning Pitch)

Judges evaluate hundreds of generic "disaster management" projects that only display basic static maps or simple form inputs. **JeevanGrid wins by demonstrating an end-to-end closed loop from fragmented chaos to verified life-saving dispatch:**

```text
[Minute 0-1]: The Crisis & Chaos
- Scenario: Extreme Category-4 Cyclone & Brahmaputra Flash Flood Hits District Barpeta, Assam.
- Problem: Telemetry arrives in fragments (radar, river gauges, frantic WhatsApp distress calls).
- The Commander's Dilemma: "Where do I send my 14 rescue boats and 6 mobile ICUs first?"

[Minute 1-2]: Spatial Fusion & Cascade Discovery
- JeevanGrid ingests live telemetry + OpenStreetMap infrastructure.
- PostGIS spatial buffer automatically reveals:
  * Hospital 'Civil Hospital Barpeta' will lose access in 45 minutes due to Submerged Bridge B-12.
  * 3 Low-lying Wards (Ward 4, 7, 9) have 34,000 vulnerable residents in the critical path.

[Minute 2-3]: Multi-Criteria Risk & AI Demand Forecasting
- Risk Engine calculates the composite MCDA score across H3 Hexagonal cells.
- AI Model forecasts:
  * Exact rescue boat requirement: 11 Boats needed at Sector East.
  * Evacuation shelter shortage: Shelter #3 is at 98% capacity; redirect to Shelter #7.

[Minute 3-4]: The 'Magic Moment' - 1-Click Operations Optimizer (MILP)
- Incident Commander clicks **"Compute Optimal Dispatch Plan"**.
- Mixed-Integer Linear Program solves the vehicle-to-demand allocation in 320 milliseconds.
- Dynamic Road Graph recalculates turn-by-turn routing, routing ambulances *around* flooded roads and dispatching NDRF boats straight through the water corridor.
- Commander reviews and clicks **"Execute Dispatch Orders"** (Broadcasts alerts to field units).

[Minute 4-5]: Impact Summary & Technical Rigor
- Summary metric panel shows:
  * Estimated response time reduced by 41%.
  * Zero resource collision/starvation across sectors.
  * Full traceability and audit logging.
```

---

## 2. Bulletproof Demo Resilience Tactics

1. **Dual-Mode Data Switch**:
   - `Live Mode`: Polls live GDACS / USGS / OpenWeather APIs.
   - `Simulation / Playback Mode`: Replays high-resolution, deterministic, real-world historical event logs with realistic time-scrubbing (0x to 10x speed).
2. **Zero Internet Failure Risk**:
   - Can run 100% locally on localhost via Docker Compose with local PostGIS and pre-cached OpenStreetMap vector tiles.
3. **No Phantom AI**:
   - Every AI prediction shows its underlying feature attribution, input vector, and confidence interval.
