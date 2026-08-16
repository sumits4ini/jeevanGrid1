# 🗺️ JeevanGrid GIS Engine & Geospatial Intelligence Core

## 1. Overview
The **JeevanGrid GIS Engine** provides a high-performance, mathematically rigorous geospatial intelligence foundation for multi-hazard disaster response. It unifies PostGIS spatial SQL indexing, Shapely computational geometry, PyProj coordinate transformations, and GeoJSON serialization into a modular, testable pipeline.

---

## 2. Package Architecture

```text
gis_engine/
├── geometry/
│   ├── validation.py      # WGS84 coordinate bounds, GeoJSON validation & Shapely converters
│   ├── operations.py      # Bounding box, centroid, geodesic area, line length & unions
│   └── transforms.py      # EPSG:4326 <-> EPSG:3857 transforms, Haversine distance, metric buffers
├── layers/
│   ├── base.py            # BaseGISLayer abstract class with GeoJSON serialization
│   ├── disaster.py        # DisasterLayer (Point epicenters & alerts)
│   ├── hazard_zone.py     # HazardZoneLayer (MultiPolygon flood inundation perimeters)
│   ├── location.py        # LocationLayer (Hospitals, power substations, bridges, shelters)
│   ├── resource.py        # ResourceLayer (NDRF boats, ambulances, supply trucks)
│   └── registry.py        # LayerRegistry (Dynamic registration & multi-layer querying)
├── spatial/
│   ├── queries.py         # Reusable PostGIS / SQLAlchemy expressions (ST_Intersects, ST_DWithin)
│   ├── proximity.py       # Distance ranking and radius search algorithms
│   └── intersections.py   # Polygon-polygon and polygon-point spatial intersection evaluation
├── schemas/
│   ├── geometry.py        # Pydantic models for Point, Polygon, MultiPolygon, BoundingBox
│   └── layer.py           # LayerMetadata, NearbyQueryRequest, SpatialIntersectionRequest
└── services/
    └── gis_service.py     # High-level GIS service coordinating DB queries and fallbacks
```

---

## 3. Supported Geometry Types & Standards

- **Standard Coordinate Reference System**: `EPSG:4326` (WGS84 Latitude/Longitude) for storage and GeoJSON output.
- **Projected Computation CRS**: `EPSG:3857` (Spherical / Web Mercator) for metric buffering and surface area calculation.
- **Supported Geometries**:
  - `Point`: `[lng, lat]`
  - `LineString`: `[[lng, lat], [lng, lat], ...]`
  - `Polygon`: `[[[lng, lat], ...]]` (Enforces boundary closure and orientation)
  - `MultiPoint`, `MultiLineString`, `MultiPolygon`, and `GeometryCollection`.

---

## 4. Key Spatial Capabilities

1. **Metric Buffer Calculation**:
   - Accurately projects WGS84 geometries into EPSG:3857 meters, applies buffer $r$ in meters, and re-projects back to WGS84 without polar distortion.
2. **Proximity & Distance Ranking**:
   - Geodesic Haversine distance formula with sub-millisecond calculation over thousands of candidate points.
3. **Multi-Layer Spatial Intersection**:
   - Evaluates which critical hospitals, bridges, or rescue teams intersect an active flood inundation polygon or its buffer zone.
4. **PostGIS Query Helpers**:
   - `build_bbox_intersects_clause`: Translates bounding boxes into `ST_MakeEnvelope` and `ST_Intersects`.
   - `build_point_radius_dwithin_clause`: Generates geodesic `ST_DWithin` queries cast to `geography`.

---

## 5. API Endpoints Matrix

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/gis/layers` | List metadata and feature counts for all active GIS layers |
| `GET` | `/api/v1/gis/layers/{layer_name}` | Get GeoJSON FeatureCollection for a layer with optional bounding box filter |
| `GET` | `/api/v1/gis/features` | Query GeoJSON features across multiple layers (`?layers=infrastructure&layers=hazard_zones`) |
| `GET` | `/api/v1/gis/nearby` | Find facilities and response units within a radius (`?lat=26.32&lng=91.00&radius=5000`) |
| `POST` | `/api/v1/gis/intersections` | Evaluate polygon intersection against critical infrastructure |
| `GET` | `/api/v1/gis/hazard-zones` | Backward-compatible active hazard polygons endpoint |
| `POST` | `/api/v1/gis/query-bbox` | Backward-compatible bounding box spatial filter |
| `POST` | `/api/v1/gis/buffer-check` | Backward-compatible facility proximity check |

---

## 6. Running Tests
Run the dedicated GIS Engine test suite:
```bash
python -m pytest tests/gis_engine -v
```
Or run the full project test suite:
```bash
pytest -v
```
