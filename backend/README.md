# 🛰️ JeevanGrid Backend API Core

## 1. Overview
The JeevanGrid Backend is an asynchronous, high-performance API service built with **Python 3.11+ and FastAPI**. It serves as the central intelligence and operations engine, orchestrating geospatial queries, multi-criteria risk calculations, AI/ML forecasting, and linear optimization for emergency resource dispatch.

---

## 2. Directory Structure

```text
backend/
├── alembic.ini                # Local alembic configuration
├── alembic/                  # Database migration scripts
│   ├── env.py                # Alembic environment with PostGIS & SQLAlchemy 2.0
│   ├── script.py.mako        # Migration template
│   └── versions/
│       └── 0001_initial_postgis_schema.py # Initial PostGIS tables & spatial indexes
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── disasters.py   # Disaster incident CRUD & summaries
│   │       │   ├── gis.py         # GeoJSON vector layers & spatial queries
│   │       │   ├── health.py      # /health & /api/v1/health endpoints with DB status
│   │       │   ├── locations.py   # Critical infrastructure & shelters
│   │       │   ├── resources.py   # Emergency response units & dispatch
│   │       │   └── risk.py        # MCDA risk index & evaluation
│   │       └── router.py          # Unified v1 router aggregator
│   ├── core/
│   │   ├── config.py              # Pydantic Settings & environment variables
│   │   ├── exceptions.py          # Custom domain exception hierarchy
│   │   ├── handlers.py            # Global exception handlers & JSON formatters
│   │   └── logging.py             # Structured logger configuration
│   ├── db/                        # Database session & Base
│   │   ├── base.py                # Declarative Base & TimestampMixin
│   │   └── session.py             # Async/sync engine, sessionmaker & DB health checker
│   ├── models/                    # SQLAlchemy / GeoAlchemy ORM models
│   │   ├── __init__.py            # Model registry export
│   │   ├── disaster.py            # Disaster entity with PostGIS Point geometry
│   │   ├── location.py            # CriticalInfrastructure entity with PostGIS Point
│   │   ├── resource.py            # ResponseUnit entity with Point & JSONB payload
│   │   └── risk_zone.py           # HazardZone entity with PostGIS MultiPolygon
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
    ├── integration/               # API & DB integration tests
    │   ├── test_db_connectivity.py
    │   ├── test_health_api.py
    │   └── test_routers_v1.py
    └── unit/                      # Configuration & unit tests
        ├── test_alembic_setup.py
        ├── test_config.py
        ├── test_db_config.py
        ├── test_exceptions.py
        └── test_models.py
```

---

## 3. Database & PostGIS Setup

JeevanGrid requires **PostgreSQL 16+** with the **PostGIS 3.4+** spatial extension.

### Option A: Local Docker (Recommended)
Start PostgreSQL + PostGIS container:
```bash
docker run -d --name jeevangrid_postgres \
  -e POSTGRES_DB=jeevangrid_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgis/postgis:16-3.4
```

### Option B: Local PostgreSQL Installation
1. Create the database:
```sql
CREATE DATABASE jeevangrid_db;
```
2. Enable PostGIS:
```sql
\c jeevangrid_db
CREATE EXTENSION IF NOT EXISTS postgis;
```

---

## 4. Running Alembic Database Migrations

Run database migrations to apply the initial schema with PostGIS extension, spatial tables, and GIST indexes:

```bash
# From repository root:
alembic upgrade head

# Or from within backend/ directory:
cd backend
alembic upgrade head
```

To rollback a migration:
```bash
alembic downgrade -1
```

---

## 5. How to Run Locally

### Step 1: Install Dependencies
```bash
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

## 6. Interactive API Documentation & Health Checks

- **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Interactive Docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Root Health Check**: `GET http://127.0.0.1:8000/health`
- **v1 Health Check**: `GET http://127.0.0.1:8000/api/v1/health`

---

## 7. Running Tests
Run the complete unit and integration test suite with `pytest`:
```bash
python -m pytest backend/tests -v
```
