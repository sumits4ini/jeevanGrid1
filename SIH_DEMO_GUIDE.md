# 🏆 JeevanGrid — SIH 2026 Live Demo & Presentation Guide

## 1. Executive Strategy & Judging Criteria Alignment

In Smart India Hackathon (SIH), judges evaluate dozens of projects in the Disaster Management track. Most teams present static web forms or simple Google Maps pins. **JeevanGrid wins by demonstrating an end-to-end, mathematically grounded, closed-loop operational workflow:**

```text
REAL DISASTER TELEMETRY ──► GIS SPATIAL FUSION ──► MCDA RISK & AI DEMAND ──► 1-CLICK MILP DISPATCH ──► AUDITED LIFE-SAVING ACTION
```

### Mapping to SIH Evaluation Criteria:
1. **Real-World Impact & Novelty**: Solves the real operational bottleneck (fragmented intelligence + uncoordinated dispatch) for NDMA/SDMAs.
2. **Technical Rigor & Complexity**: Combines PostGIS spatial SQL, H3 hexagonal indexing, LightGBM inference, and Mixed-Integer Linear Programming.
3. **Data Authenticity & Integrity**: Transparently separates real/simulated data; zero hallucinated AI predictions.
4. **User Experience & Feasibility**: Tactical high-contrast EOC dark-theme dashboard designed for high-stress decision-making.
5. **Robustness & Demo Resilience**: Dual-mode architecture (Live API + Deterministic Offline Playback) ensures 100% reliability regardless of venue Wi-Fi failure.

---

## 2. 5-Minute High-Impact Pitch Script

```text
==================================================================================================
TIME           PHASE                    WHAT TO SHOW ON SCREEN                   WHAT TO SAY
==================================================================================================
0:00 - 0:45    The Problem & Chaos      - Open dashboard with raw IMD radar     "During disasters, the bottleneck
                                          and unranked emergency calls.           is not detecting the event—it's
                                        - Highlight the fragmented data.         knowing WHO is at risk and WHERE
                                                                                 to send limited resources first."

0:45 - 1:45    GIS Spatial Fusion &     - Enable PostGIS Hazard Inundation      "JeevanGrid fuses satellite, radar,
               Cascade Analysis           layer and Critical Infrastructure.     and OSM data in real time. Notice
                                        - Click on Barpeta Civil Hospital:       how it instantly detects that Civil
                                          alert shows 'Access cutoff in 45m'.    Hospital will be cut off because
                                        - Zoom into H3 Hexagonal Grid.           Bridge B-12 is submerged."

1:45 - 2:45    MCDA Risk & AI Demand    - Open the Risk Analysis View.           "Using the UNDRR formulation, our
               Forecasting              - Show MCDA Score breakdown:             MCDA engine calculates risk across
                                          Hazard × Exposure × Vulnerability.     34,000 residents in Wards 4 & 7.
                                        - Show AI Demand Forecast:               Our AI model forecasts a deficit:
                                          "11 Boats & 4 ICUs needed".            11 boats needed, and Shelter #3
                                                                                 is already at 98% capacity."

2:45 - 4:00    The "Magic Moment":      - Click 'Compute Optimal Dispatch'.      "With one click, our MILP optimizer
               1-Click MILP Optimizer   - MILP solves in 320ms.                  solves multi-depot vehicle allocation.
               & Dynamic Routing        - Display turn-by-turn routes on map:    Notice the dynamic routing: ambulances
                                          Ambulances avoid flooded roads;         are routed around flooded bridges,
                                          Boats use the water corridor.          while NDRF boats navigate straight
                                        - Click 'Execute Dispatch Orders'.       through the water corridor."

4:00 - 5:00    Impact Summary &         - Summary metrics card:                  "Result: 41% reduction in response
               Technical Defense          - 41% faster response time             time, zero resource starvation, and
                                          - 0 duplicate unit assignments         100% auditability. JeevanGrid transforms
                                        - Open Swagger API / Architecture doc.   chaos into actionable intelligence."
==================================================================================================
```

---

## 3. Demo Scenario: "Assam Brahmaputra Flash Flood 2026"

### Baseline Scenario Context:
- **Location**: Barpeta District, Assam, India (`26.3216° N, 91.0063° E`).
- **Disaster Type**: Extreme Monsoon Flash Flood & River Inundation.
- **Affected Population**: ~85,000 residents across 6 low-lying wards.
- **Critical Infrastructure at Risk**:
  - *Barpeta Civil Hospital* (Primary trauma center, backup power at 6 hours).
  - *Bridge B-12 (National Highway link)*: Submerged by 0.65m floodwater.
  - *Power Substation #4*: Degraded, risk of blackout in Sector East.
- **Available Emergency Response Assets**:
  - 14 NDRF Motorized Inflatable Boats (Depot North & Depot South).
  - 8 Advanced Life Support (ALS) Ambulances.
  - 5 Mobile Food & Water Supply Trucks.
  - 4 Designated Evacuation Shelters.

---

## 4. Live Demo Resilience & Zero-Fail Protocols

### Rule 1: Always Test the Local Docker Stack First
Before presenting, verify that the local stack is running smoothly on `localhost`:
```bash
# Verify container health
docker compose ps

# Check API health endpoint
curl http://localhost:8000/api/v1/health
```

### Rule 2: Use Deterministic Simulation Playback
If external Wi-Fi is unstable or external APIs rate-limit:
- Set `ENABLE_DEMO_SIMULATION_MODE=true` in `.env`.
- The backend will replay the verified Assam Brahmaputra historical dataset with millisecond precision.

### Rule 3: Keep the EOC Dark Theme High-Contrast
- Ensure the projector or screen display is calibrated for high contrast.
- Critical hazard zones are color-coded in vivid Amber/Red (`#EF4444` / `#F59E0B`), and operational routes are rendered with luminous animated strokes.

---

## 5. Potential Judges' Q&A & Technical Defense

**Q1: "Is your AI model predicting the actual flood or just visualizing it?"**
> *Answer*: "We clearly decouple the layers. Inundation depth is derived from real hydrological gauges and DEM elevation models. Our AI (LightGBM & Ridge regression) specifically predicts the *operational consequences*: the 24-hour severity escalation trajectory and exact resource demands (boats, ambulances, rations) based on demographic vulnerability. If model confidence is $<70\%$, the system automatically falls back to deterministic PostGIS rules."

**Q2: "How does your routing know a road is flooded?"**
> *Answer*: "We intersect the OSM road network with our active PostGIS hazard depth polygons. Any road edge with water depth $>0.3\text{m}$ receives an infinite weight penalty in our NetworkX road graph, instantly forcing ambulance routes onto high-ground detours while opening aquatic routes for NDRF boats."

**Q3: "How is this different from standard government portals like NDMA or Bhuvan?"**
> *Answer*: "Existing portals are passive monitoring tools that show what happened in the past. JeevanGrid is an active decision-support system that tells commanders *what to do next*—optimizing resource allocation via linear programming and generating actionable dispatch orders."
