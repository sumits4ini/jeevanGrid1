# 01. JeevanGrid System Architecture

## 1. Executive Summary & Core Paradigm

**JeevanGrid** is an enterprise-grade disaster intelligence and emergency response platform designed to bridge the fatal gap between raw disaster telemetry and operational incident command decisions.

During extreme disaster events (e.g. urban flooding, flash floods, tropical cyclones, landslides), existing disaster management systems provide fragmented data:
- Meteorological feeds provide rainfall rasters.
- Hydrological sensors provide stage height readings.
- GIS portals display static base maps.
- NDRF / SDRF / Municipal field teams operate via asynchronous radio and unranked calls.

**JeevanGrid transforms this disjointed flow into a deterministic, closed-loop pipeline:**

```text
+-----------------------------------------------------------------------------+
|                               DISASTER TELEMETRY                            |
| (Rainfall Radar, River Gauges, Elevation DEM, OSM Infrastructure, Alerts)   |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                       GIS SPATIAL FUSION & INGESTION                        |
|  - PostGIS Spatial Aggregation (ST_Intersects, ST_DWithin)                  |
|  - Hexagonal Spatial Indexing (Uber H3 Res-8 / 460m)                        |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                    MULTI-CRITERIA RISK & VULNERABILITY                     |
|           Hazard (H) x Exposure (E) x Vulnerability (V) / Capacity (C)       |
|  - Inundation Depth + Critical Infrastructure Vulnerability Matrix          |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                         AI / ML FORECASTING ENGINE                          |
|  - Severity Classification (LightGBM)                                       |
|  - Resource Demand Forecasting (Multi-Output Regression)                    |
|  - Distress Signal NLP & Triage                                             |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                   OPERATIONS OPTIMIZATION & DISPATCH                        |
|  - Capacitated Resource Allocation (Mixed-Integer Linear Programming)       |
|  - Safe Evacuation & Rescue Routing (Obstacle-Penalized Network Graphs)     |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                  TACTICAL EMERGENCY COMMAND DASHBOARD (COP)                 |
|  - Interactive MapLibre Vector Map + Live Isochrones                        |
|  - 1-Click Operational Dispatch Order Generation                            |
+-----------------------------------------------------------------------------+
```

---

## 2. System Architecture Layers

JeevanGrid is structured as a **Modular Monolith** with clearly decoupled layers to ensure rapid development, strict type safety, predictable testing, and high reliability during high-stakes demonstrations and real-world deployment.

```text
+------------------------------------------------------------------------------+
| PRESENTATION LAYER (Next.js 14, TypeScript, Tailwind CSS, MapLibre GL)       |
|  - Command & Control COP Dashboard                                           |
|  - Interactive Spatial Map View (Layers: Hazards, Roads, Resources, Isochrones)
|  - Triage Priority Board & Tactical Dispatch Console                         |
|  - Scenario Simulation Controller (Time scrubber, parameter injection)       |
+------------------------------------------------------------------------------+
                                       | HTTP / REST (OpenAPI) / WebSocket (SSE)
                                       v
+------------------------------------------------------------------------------+
| APPLICATION GATEWAY & API LAYER (FastAPI, Python 3.11+, Pydantic v2)         |
|  - Auth & RBAC Security Middleware (JWT, Roles: Commander, Dispatcher, Viewer)
|  - Rate Limiting & Input Sanitization                                        |
|  - Endpoints: /disasters, /gis, /risk, /ml, /optimize, /simulation           |
+------------------------------------------------------------------------------+
                                       |
           +---------------------------+---------------------------+
           |                           |                           |
           v                           v                           v
+-----------------------+   +-----------------------+   +----------------------+
|   GIS & RISK ENGINE   |   |   AI/ML INFERENCE     |   | RESOURCE OPTIMIZER   |
| - Spatial Intersection|   | - Severity Classifier |   | - MILP Allocation    |
| - Isochrone Generation|   | - Demand Forecaster   |   | - Dijkstra/NetworkX  |
| - H3 Grid Aggregation |   | - Distress Triage     |   |   Safe Route Graph   |
+-----------------------+   +-----------------------+   +----------------------+
           |                           |                           |
           +---------------------------+---------------------------+
                                       |
                                       v
+------------------------------------------------------------------------------+
| PERSISTENCE & DATA LAYER                                                     |
|  - PostgreSQL 16 + PostGIS 3.4 (Relational + Geospatial Geometries)          |
|  - Redis 7.2 (Spatial Query Caching, Session Management, Real-time Pub/Sub)  |
|  - Local File/Artifact Store (DEM Geotiffs, Pretrained ML Model Weights)     |
+------------------------------------------------------------------------------+
```

---

## 3. Key Design Principles

1. **Deterministic Core with AI Augmentation**:
   - Critical path safety algorithms (safe routing, risk calculation) rely on deterministic mathematics (graph theory, PostGIS spatial analysis, linear programming).
   - Machine Learning models augment the system with trend forecasting and demand prediction, with fallback bounds to prevent hallucinated decisions.
2. **Zero Hardcoded Secrets**:
   - Strict 12-Factor App methodology. All configuration injected via `.env`.
3. **Graceful Degradation & Dual-Mode Telemetry**:
   - Real-time external APIs (IMD, GDACS, USGS) operate behind adapter interfaces with circuit breakers.
   - If external connections drop or rate-limit during emergency drills or hackathon evaluations, the system automatically falls back to high-fidelity, deterministic seedable simulation datasets without crashing.
4. **Sub-Second Spatial Response**:
   - Geospatial assets are indexed with GIST (Generalized Search Trees) and spatial partitions to guarantee < 500ms query times over tens of thousands of infrastructure nodes.
