# 🛰️ JeevanGrid Backend API Core

## 1. Overview
The JeevanGrid Backend is an asynchronous, high-performance API service built with **Python 3.11+ and FastAPI**. It serves as the central intelligence and operations engine, orchestrating geospatial queries, multi-criteria risk calculations, AI/ML forecasting, and linear optimization for emergency resource dispatch.

---

## 2. Directory Structure

```text
backend/
├── alembic/                  # Database migration scripts (Phase 3)
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── disasters.py   # Disaster incident CRUD & summaries
│   │       │   ├── gis.py         # GeoJSON vector layers & spatial queries
│   │       │   ├── health.py      # /health & /api/v1/health endpoints
│   │       │   ├── locations.py   # Critical infrastructure & shelters
│   │       │   ├── resources.py   # Emergency response units & dispatch
│   │       │   └── risk.py        # MCDA risk index & evaluation
│   │       └── router.py          # Unified v1 router aggregator
│   ├── core/
│   │   ├── config.py              # Pydantic Settings & environment variables
│   │   ├── exceptions.py          # Custom domain exception hierarchy
│   │   ├── handlers.py            # Global exception handlers & JSON formatters
│   │   └── logging.py             # Structured logger configuration
│   ├── db/                        # Database session & Base (Phase 3)
│   ├── models/                    # SQLAlchemy / GeoAlchemy ORM models (Phase 3)
│   ├── schemas/                   # Pydantic request/response validation schemas
│   │   ├── common.py              # ApiResponse, HealthResponse, ErrorResponse
│   │   ├── disaster.py            # Disaster schemas
│   │   ├── gis.py                 # GeoJSON schemas & bounding box queries
│   │   ├── location.py            # Critical infrastructure schemas
│   │   ├── resource.py            # Emergency units & dispatch schemas
│   │   └── risk.py                # MCDA risk schemas
│   ├── services/                  # Business logic services
│   │   ├── gis/                   # Spatial algorithms (Phase 5)
│   │   ├── ingestion/             # Telemetry adapters (Phase 6)
│   │   ├── ml/                    # Machine learning inference (Phase 8)
│   │   ├── optimization/          # MILP resource optimizer (Phase 9)
│   │   └── risk_engine/           # Multi-criteria risk calculator (Phase 7)
│   └── main.py                    # FastAPI application entry point & lifespan
├── requirements.txt               # Lean Python dependencies
└── tests/                         # Pytest test suite
    ├── conftest.py                # Test fixtures & TestClient
    ├── integration/               # API integration tests
    └── unit/                      # Configuration & unit tests
```

---

## 3. How to Run Locally

### Step 1: Install Dependencies
```bash
cd c:\Users\sumit\JeevanGrid1
pip install -r backend/requirements.txt
```

### Step 2: Configure Environment Variables
Copy the template file to `.env`:
```bash
cp backend/.env.example .env
```

### Step 3: Run the FastAPI Server
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at `http://127.0.0.1:8000`.

---

## 4. Interactive API Documentation & Health Checks

- **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Interactive Docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Root Health Check**: `GET http://127.0.0.1:8000/health`
- **v1 Health Check**: `GET http://127.0.0.1:8000/api/v1/health`
- **OpenAPI JSON**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 5. API V1 Route Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Root system health & subsystem readiness check |
| `GET` | `/api/v1/health` | API v1 health & readiness check |
| `GET` | `/api/v1/disasters` | List disaster events with status/type filtering |
| `GET` | `/api/v1/disasters/summary/overview` | Aggregated COP disaster metrics |
| `POST` | `/api/v1/disasters` | Register new disaster event |
| `GET` | `/api/v1/disasters/{id}` | Get disaster details by ID (404 handled) |
| `GET` | `/api/v1/locations/infrastructure` | List critical infrastructure facilities |
| `POST` | `/api/v1/locations/infrastructure` | Register new infrastructure asset |
| `GET` | `/api/v1/resources/units` | List active emergency response units |
| `POST` | `/api/v1/resources/units` | Register new response vehicle/team |
| `POST` | `/api/v1/resources/dispatch-plan` | Compute optimal dispatch plan |
| `GET` | `/api/v1/risk/categories` | List UNDRR operational risk tiers |
| `POST` | `/api/v1/risk/evaluate` | Trigger MCDA regional risk evaluation |
| `GET` | `/api/v1/gis/hazard-zones` | Retrieve GeoJSON hazard polygons |
| `POST` | `/api/v1/gis/query-bbox` | Query spatial layers by bounding box |
| `POST` | `/api/v1/gis/buffer-check` | Check infrastructure proximity within buffer |

---

## 6. Standard API Envelopes & Error Format

### Successful Response:
```json
{
  "success": true,
  "message": "Disaster events retrieved successfully.",
  "data": [],
  "timestamp": "2026-08-16T21:15:00.000000Z"
}
```

### Error Response (e.g. 404 Entity Not Found):
```json
{
  "success": false,
  "error_code": "ENTITY_NOT_FOUND",
  "message": "Disaster with ID '00000000-0000-0000-0000-000000000000' was not found.",
  "details": {
    "entity_name": "Disaster",
    "entity_id": "00000000-0000-0000-0000-000000000000"
  },
  "timestamp": "2026-08-16T21:15:00.000000Z"
}
```

---

## 7. Running Tests
Run the complete unit and integration test suite with `pytest`:
```bash
pytest -v
```
