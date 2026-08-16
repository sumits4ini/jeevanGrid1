# 04. Database Architecture & API Specification

## 1. Relational & Spatial Database Schema (PostgreSQL + PostGIS)

```text
Table: disasters
- id: UUID (PK)
- name: VARCHAR(100) (e.g. "Cyclone Vardah 2026", "Assam Flash Flood")
- disaster_type: ENUM ('FLOOD', 'CYCLONE', 'LANDSLIDE', 'EARTHQUAKE', 'URBAN_FIRE')
- severity_level: INT (1 to 5)
- status: ENUM ('ACTIVE', 'CONTAINED', 'RESOLVED', 'SIMULATED')
- epicentre: GEOMETRY(Point, 4326)
- created_at: TIMESTAMPTZ
- updated_at: TIMESTAMPTZ

Table: hazard_zones
- id: UUID (PK)
- disaster_id: UUID (FK -> disasters.id)
- polygon_geom: GEOMETRY(MultiPolygon, 4326)
- inundation_depth_m: FLOAT
- hazard_intensity: FLOAT (0.0 - 1.0)
- is_active: BOOLEAN
- recorded_at: TIMESTAMPTZ

Table: critical_infrastructure
- id: UUID (PK)
- name: VARCHAR(150)
- facility_type: ENUM ('HOSPITAL', 'POWER_SUBSTATION', 'WATER_TREATMENT', 'BRIDGE', 'COMM_TOWER', 'SHELTER')
- location: GEOMETRY(Point, 4326)
- operational_status: ENUM ('OPERATIONAL', 'DEGRADED', 'FAILED', 'CUT_OFF')
- max_capacity: INT
- current_occupancy: INT
- backup_power_hours: FLOAT
- contact_phone: VARCHAR(30)

Table: response_units (NDRF, SDRF, Ambulances, Food Logistics)
- id: UUID (PK)
- unit_code: VARCHAR(50) (e.g. "NDRF-BN-01", "AMB-DIST-14")
- unit_type: ENUM ('NDRF_TEAM', 'AMBULANCE', 'RESCUE_BOAT', 'FOOD_WATER_TRUCK', 'MOBILE_GENERATOR')
- current_location: GEOMETRY(Point, 4326)
- status: ENUM ('AVAILABLE', 'DISPATCHED', 'ON_MISSION', 'MAINTENANCE')
- assigned_incident_id: UUID (Nullable, FK -> incidents.id)
- capacity_payload: JSONB (e.g. {"beds": 2, "water_litres": 5000, "boat_seats": 12})

Table: distress_reports
- id: UUID (PK)
- disaster_id: UUID (FK -> disasters.id)
- location: GEOMETRY(Point, 4326)
- raw_message: TEXT
- triage_priority: ENUM ('P1_CRITICAL', 'P2_HIGH', 'P3_MEDIUM', 'P4_LOW')
- victims_count: INT
- verification_status: ENUM ('UNVERIFIED', 'VERIFIED_AI', 'VERIFIED_OFFICER', 'RESOLVED', 'FALSE_ALARM')
- reported_at: TIMESTAMPTZ

Table: dispatch_allocations
- id: UUID (PK)
- disaster_id: UUID (FK -> disasters.id)
- target_zone_id: UUID (FK -> hazard_zones.id)
- unit_id: UUID (FK -> response_units.id)
- recommended_route_geojson: JSONB
- estimated_eta_minutes: FLOAT
- dispatch_status: ENUM ('RECOMMENDED', 'APPROVED', 'EN_ROUTE', 'COMPLETED', 'ABORTED')
- created_at: TIMESTAMPTZ
```

---

## 2. API Specification (RESTful OpenAPI 3.0 & SSE/WS)

### Core Endpoints Matrix:

```text
HTTP Method  Endpoint                            Description
-----------------------------------------------------------------------------------------------------------------
POST         /api/v1/auth/login                  Authenticate incident commanders & operators (JWT output)
GET          /api/v1/disasters                   List active & past disasters with spatial filters
GET          /api/v1/disasters/{id}/summary      Get aggregated COP executive metrics (Casualties at risk, active units)
GET          /api/v1/gis/hazard-zones/{id}       Return GeoJSON MultiPolygon layers with depth attributes
GET          /api/v1/gis/infrastructure          Query infrastructure points within bbox / buffer radius
POST         /api/v1/risk/evaluate               Trigger MCDA & ML risk assessment on selected spatial boundary
POST         /api/v1/optimize/dispatch-plan      Compute optimal MILP resource allocation & safe evacuation routes
GET          /api/v1/resources/units             List all live emergency vehicles and response battalions
POST         /api/v1/distress/submit             Ingest public / field distress signal and run AI triage
POST         /api/v1/simulation/tick             Advance simulation clock for scenario replay / SIH live demo
WS / SSE     /api/v1/stream/alerts               Real-time WebSocket / Server-Sent Events stream for live alerts
```
