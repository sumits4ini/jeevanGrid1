# 🏛️ JeevanGrid System Architecture Specification

## 1. Executive Summary & Core Mission
**JeevanGrid** is a Next-Generation Disaster Intelligence and Emergency Response Platform engineered to solve the critical operational bottleneck during multi-hazard crises:

> **"What is happening, who and what is at risk, what resources are available, and what should authorities do next?"**

During floods, cyclones, landslides, and earthquakes, disaster management authorities (NDMA, SDMAs, District Emergency Operations Centers - DEOCs) are overwhelmed by fragmented, unstandardized telemetry. JeevanGrid synthesizes spatial sensor data, weather feeds, OpenStreetMap infrastructure, and distress signals into an actionable, priority-weighted **Common Operational Picture (COP)** with closed-loop automated resource optimization.

---

## 2. End-to-End Operational Pipeline

```text
+─────────────────────────────────────────────────────────────────────────────+
|                             DISASTER TELEMETRY                              |
|  - Meteorological radar & precipitation (IMD / NOAA / OpenWeather)          |
|  - Hydrological river stage & water level sensors (CWC)                    |
|  - Geospatial infrastructure & road networks (OpenStreetMap / State GIS)    |
|  - Real-time citizen & first responder distress reports                     |
+─────────────────────────────────────────────────────────────────────────────+
                                       │
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|                       GIS SPATIAL FUSION & INGESTION                        |
|  - PostGIS Spatial Aggregation (ST_Intersects, ST_DWithin, ST_Buffer)       |
|  - Hexagonal Discrete Spatial Indexing (Uber H3 Res-8 / ~460m edge)         |
|  - Standardized coordinate transformations (EPSG:4326 <-> EPSG:3857)        |
+─────────────────────────────────────────────────────────────────────────────+
                                       │
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|               MULTI-CRITERIA RISK & VULNERABILITY ENGINE (MCDA)             |
|       Risk = [ Hazard (H) × Exposure (E) × Vulnerability (V) ] / Capacity (C)|
|  - Inundation depth, demographic vulnerability, low-lying slope factors     |
|  - Real-time critical infrastructure vulnerability radius                   |
+─────────────────────────────────────────────────────────────────────────────+
                                       │
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|                         AI / ML FORECASTING ENGINE                          |
|  - LightGBM Severity & Disaster Escalation Classifier                       |
|  - Multi-Output Ridge/XGBoost Resource Demand Forecaster                    |
|  - DistilBERT / NLP Citizen Distress Signal Triage Engine                   |
+─────────────────────────────────────────────────────────────────────────────+
                                       │
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|                    OPERATIONS & LOGISTICS OPTIMIZER                         |
|  - Capacitated Multi-Depot Resource Allocation (Mixed-Integer Linear Prog.) |
|  - Obstacle-Penalized Dynamic Road Network Graph (NetworkX / Dijkstra)      |
|  - Dynamic water barrier severance (>0.3m water depth blocks ambulances)   |
+─────────────────────────────────────────────────────────────────────────────+
                                       │
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|                 TACTICAL COMMAND & CONTROL DASHBOARD (COP)                  |
|  - GPU-accelerated MapLibre GL Vector Map with dynamic layer toggles        |
|  - 1-Click Operational Dispatch Order Generation                            |
|  - Time-scrubbing historical scenario simulator for drills & evaluation     |
+─────────────────────────────────────────────────────────────────────────────+
```

---

## 3. Modular Monolith Layered Architecture

JeevanGrid is built as a **Modular Monolith** to maximize developer productivity, minimize deployment complexity, ensure sub-second response times, and prevent distributed microservice failure modes during disaster operations.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ PRESENTATION TIER (Next.js 14, TypeScript, Tailwind CSS, MapLibre GL JS)    │
│  - Incident Commander COP Dashboard                                         │
│  - Dynamic Multi-Layer GIS Map (Inundation, Infrastructure, Isochrones)     │
│  - Triage Priority Board & Tactical Dispatch Console                        │
│  - Historical Scenario Simulation Player (Tick / Scrub / Speed Control)     │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼  RESTful JSON (OpenAPI 3.0) / SSE Alerts
┌─────────────────────────────────────────────────────────────────────────────┐
│ APPLICATION & API GATEWAY TIER (FastAPI, Python 3.11+, Pydantic v2)         │
│  - OAuth2 / JWT Authentication & Role-Based Access Control (RBAC)           │
│  - Rate Limiting, Input Sanitization & Geospatial Polygon Validation        │
│  - API Versioning: /api/v1/disasters, /gis, /risk, /optimize, /distress     │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│   GIS & SPATIAL ENGINE  │  │   RISK & AI/ML ENGINE   │  │   RESOURCE OPTIMIZER    │
│ - PostGIS 3.4 Spatial   │  │ - UNDRR MCDA Calculator │  │ - MILP Solver (PuLP)    │
│ - Shapely / PyProj / H3 │  │ - LightGBM Severity Pred│  │ - Dynamic Road Network  │
│ - Topological Graphs    │  │ - Demand Forecaster     │  │   Safe Path Finder      │
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘
        │                              │                              │
        └──────────────────────────────┼──────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ DATA & PERSISTENCE TIER                                                     │
│  - PostgreSQL 16 + PostGIS 3.4 (Relational + Geospatial GIST Indexed)       │
│  - Redis 7.2 (Spatial Query Caching, Session Store, Live Alert Pub/Sub)     │
│  - File / Artifact Store (DEM Rasters, Trained ML Model Weights, Schemas)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Subsystem Deep-Dives

### 4.1 GIS & Spatial Intelligence Engine
- **Coordinate Reference Systems**:
  - `EPSG:4326` (WGS84 Lat/Lng) for universal storage and GeoJSON serialization.
  - `EPSG:3857` (Spherical Mercator) for distance/buffer math in meters and MapLibre tile rendering.
- **Spatial Indexing**: Uber H3 Hexagonal Grid (Resolution 8: ~0.73 km² per cell). This creates continuous, equidistant spatial bins that prevent rectangular raster boundary bias.
- **Topological Road Routing Graph**: Road vectors are represented as a weighted graph $G(V, E)$. When flood depth exceeds 0.3m on a road segment, its edge weight is set to $\infty$ for standard ground vehicles, while activating aquatic navigation routes for NDRF motorboats.

### 4.2 Multi-Criteria Risk Engine (MCDA)
JeevanGrid implements the **UNDRR Disaster Risk Equation**:
$$\text{Risk Index} = \frac{\text{Hazard Intensity } (H) \times \text{Exposure } (E) \times \text{Vulnerability } (V)}{\text{Coping Capacity } (C)}$$

All parameters are normalized into $[0.0, 1.0]$. The composite score categorizes each H3 hexagon into:
- **0.00 – 0.25**: Low (Green - Monitor)
- **0.25 – 0.50**: Moderate (Yellow - Advisory / Standby)
- **0.50 – 0.75**: High (Orange - Pre-evacuate & Pre-position Supplies)
- **0.75 – 1.00**: Critical (Red - Immediate Emergency Rescue Dispatch)

### 4.3 AI / Machine Learning Engine
- **Severity Prediction**: Gradient-boosted trees (LightGBM) trained on historical precipitation, river gauges, soil moisture, and topographic elevation.
- **Demand Forecasting**: Multi-target regression estimating required rescue boats, ambulances, medical kits, and food/water rations based on affected population size and demographic vulnerability.
- **Integrity Rule**: Every AI output includes confidence bounds. If prediction confidence drops below 70%, the system automatically engages deterministic MCDA rules.

### 4.4 Operations & Resource Optimizer (MILP)
Emergency dispatch is formulated as a Mixed-Integer Linear Program (MILP):
- **Objective**: Maximize total priority-weighted lives saved minus travel time penalties.
- **Constraints**: Vehicle capacity limits, depot supply ceilings, road traversability restrictions, and maximum response shift durations.

---

## 5. Security & Governance Architecture
- **Authentication**: JWT Bearer tokens with HMAC-SHA256 signature and short expiration.
- **Authorization**: Role-Based Access Control (RBAC):
  - `COMMANDER`: Full dispatch approval, scenario injection, system configuration.
  - `DISPATCHER`: Resource status updates, distress report verification.
  - `VIEWER`: Read-only Common Operational Picture.
- **Input Sanitization**: Strict Pydantic v2 schemas and GeoJSON polygon vertex limits to protect against DoS attacks.
- **Zero Secrets Rule**: Enforced by `.gitignore`, `.env.example`, and environment variable injection.

---

## 6. Detailed Architectural References
For component-level specifications, see:
- [01. System Architecture Details](docs/architecture/01_system_architecture.md)
- [02. GIS and Spatial Intelligence Engine](docs/architecture/02_gis_and_spatial_engine.md)
- [03. AI/ML, Risk Analysis & Optimization Engine](docs/architecture/03_ai_ml_and_risk_engine.md)
- [04. Database Schema & API Specification](docs/architecture/04_database_and_api_spec.md)
- [05. SIH 2026 Live Demo Playbook](docs/architecture/05_sih_demo_playbook.md)
