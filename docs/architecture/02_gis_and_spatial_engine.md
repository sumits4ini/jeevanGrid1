# 02. GIS and Spatial Intelligence Engine

## 1. Spatial Foundation & Coordinate Systems

- **Storage CRS**: `EPSG:4326` (WGS84 Latitude / Longitude) for universal data interoperability and standard GeoJSON compliance.
- **Projected Computation CRS**: `EPSG:3857` (Spherical / Web Mercator) for distance and buffer calculations in metric units (meters) and vector tile rendering.
- **Spatial Resolution & Indexing**: Uber H3 Hexagonal Hierarchical Spatial Index (Resolution 8: ~0.73 km² per hexagon, ~460m edge length) for uniform exposure, vulnerability, and population aggregation.

---

## 2. Spatial Entities & Layers

```text
Layer Category              Geometry Type           Attributes & Purpose
-----------------------------------------------------------------------------------------------------------------
1. Hazard Inundation Zone   Polygon / MultiPolygon  Hazard Type, Severity (1-5), Inundation Depth (m), Timestamp
2. Critical Infrastructure  Point                   Facility Type (Hospital, Power Substation, Water Plant, Bridge),
                                                    Bed Capacity, Generator Status, Operational Status
3. Population Hexgrid       Polygon (H3 Hex)        Population Count, Vulnerability Score (Elderly/Children %),
                                                    Calculated Risk Level (Low/Med/High/Critical)
4. Road Network & Bridges   LineString / MultiLine  Road Class, Flow Direction, Passability Status, Water Depth
5. Emergency Resources      Point (Moving/Static)   Type (NDRF, Ambulance, Boat, Supply Truck), Status, Capacity
6. Evacuation Centers       Point / Polygon         Shelter Name, Max Capacity, Current Occupancy, Relief Stocks
```

---

## 3. PostGIS Spatial Operations & Queries

JeevanGrid leverages native PostGIS 3.4 spatial SQL functions for high-speed deterministic geospatial queries:

### A. Infrastructure at Risk (Buffer & Intersect)
Find all critical infrastructure located within a 1,000-meter buffer of active hazard zones:
```sql
SELECT 
    ci.id,
    ci.name,
    ci.facility_type,
    ci.capacity,
    ST_Distance(ci.geom::geography, hz.geom::geography) AS distance_to_hazard_m
FROM critical_infrastructure ci
JOIN hazard_zones hz 
  ON ST_DWithin(ci.geom::geography, hz.geom::geography, 1000)
WHERE hz.is_active = true;
```

### B. Population Inundation Intersection
Aggregate affected population across overlapping hazard boundaries:
```sql
SELECT 
    hz.id AS disaster_zone_id,
    SUM(h3.population * (ST_Area(ST_Intersection(h3.geom, hz.geom)) / ST_Area(h3.geom))) AS estimated_affected_population
FROM h3_hex_grid h3
JOIN hazard_zones hz 
  ON ST_Intersects(h3.geom, hz.geom)
WHERE hz.id = :zone_id
GROUP BY hz.id;
```

---

## 4. Disaster-Aware Tactical Routing Graph

Standard turn-by-turn routing algorithms fail during disasters because they do not account for submerged roadways, destroyed bridges, and toxic hazard plumes.

JeevanGrid constructs a **Dynamic Weighted Road Graph**:
- Nodes: Road intersections and emergency depots.
- Edges: Road segments with edge weight $W_e$.

$$W_e = \text{Length}_e \times \text{RoadFactor}_e \times \text{HazardMultiplier}_e$$

Where:
- $\text{RoadFactor}_e = 1.0$ (Highway), $1.3$ (Primary), $1.8$ (Secondary), $2.5$ (Unpaved).
- If edge intersects a **Hazard Zone with Water Depth $> 0.3m$** (impassable for ambulances), $\text{HazardMultiplier}_e = \infty$ (Edge Severed).
- If edge intersects a **Hazard Zone with Water Depth $< 0.3m$**, $\text{HazardMultiplier}_e = 5.0$ (High friction / slow speed).
- NDRF rescue boats switch to a dual aquatic graph where flooded waterways become high-speed traversable edges.
