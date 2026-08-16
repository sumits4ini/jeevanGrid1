# 🌐 JeevanGrid
### *Next-Generation Disaster Intelligence & Autonomous Emergency Response Operations Platform*

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostGIS](https://img.shields.io/badge/GIS-PostGIS%203.4-336791.svg?logo=postgresql&logoColor=white)](https://postgis.net)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-000000.svg?logo=next.js&logoColor=white)](https://nextjs.org)
[![MapLibre](https://img.shields.io/badge/Maps-MapLibre%20GL-blue.svg?logo=mapbox&logoColor=white)](https://maplibre.org)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Phase-Phase%200%20Complete-brightgreen.svg)]()

---

## 📌 Executive Overview

During extreme disasters (floods, cyclones, landslides, earthquakes), disaster management authorities face severe **information fragmentation** across weather forecasts, flood gauges, spatial maps, and unranked emergency calls. 

**JeevanGrid** solves the critical operational question:
> **"What is happening, who is at risk, what resources are available, and what should authorities do next?"**

JeevanGrid bridges the gap between raw spatial telemetry and real-time life-saving decisions by combining **GIS Spatial Analytics**, **Multi-Criteria Risk Indexing (MCDA)**, **LightGBM/AI Forecasting**, and **Mixed-Integer Linear Programming (MILP) Resource Optimization** into a unified Common Operational Picture (COP).

---

## 🏛️ System Architecture

```text
  [ Disaster Telemetry ] ---> [ PostGIS Spatial Fusion ] ---> [ MCDA Risk & AI Engine ]
                                                                      |
  [ Tactical EOC Command ] <--- [ MILP Resource Optimizer ] <---------+
```

For comprehensive architectural specifications, refer to the documentation:
- [01. System Architecture](docs/architecture/01_system_architecture.md)
- [02. GIS and Spatial Intelligence Engine](docs/architecture/02_gis_and_spatial_engine.md)
- [03. AI/ML, Risk Analysis & Optimization Engine](docs/architecture/03_ai_ml_and_risk_engine.md)
- [04. Database Schema & API Specification](docs/architecture/04_database_and_api_spec.md)
- [05. SIH 2026 Live Demo Playbook](docs/architecture/05_sih_demo_playbook.md)

---

## 🛠️ Technology Stack

| Layer | Technologies | Rationale |
| :--- | :--- | :--- |
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, MapLibre GL JS, TanStack Query | Ultra-fast vector map rendering, high-contrast dark theme, strict typing |
| **Backend API** | Python 3.11+, FastAPI, Pydantic v2, Async SQLAlchemy | Async performance, native OpenAPI documentation, scientific ecosystem |
| **Geospatial & DB** | PostgreSQL 16 + PostGIS 3.4, Shapely, PyProj, GeoPandas, Uber H3 | Industry-standard spatial SQL indexing (GIST) and topological queries |
| **AI / ML** | Scikit-learn, LightGBM, ONNX Runtime | Fast, interpretable inference with zero bloat and verified baseline metrics |
| **Optimization** | PuLP / SciPy Linear Programming, NetworkX | Exact mathematical optimization for capacitated multi-depot vehicle routing |
| **Caching & Bus** | Redis 7.2 | Sub-millisecond caching of hot GeoJSON layers and real-time alert dispatch |
| **DevOps** | Docker, Docker Compose | Consistent local and cloud deployment with 1-command startup |

---

## 📂 Project Structure

```text
JeevanGrid/
├── .env.example              # Environment variables template
├── .gitignore                # Production ignore rules
├── CONTRIBUTING.md           # Contribution guidelines & branching model
├── LICENSE                   # Apache 2.0 open-source license
├── README.md                 # Project README
├── ai_ml/                    # Machine Learning models, pipelines & notebooks
│   ├── models/               # Serialized model weights (.joblib, .onnx)
│   ├── notebooks/            # Exploratory analysis & training benchmarks
│   └── pipelines/            # Feature transformation & inference pipelines
├── backend/                  # FastAPI Application Core
│   ├── alembic/              # Database migration scripts
│   ├── app/
│   │   ├── api/              # RESTful API route definitions (v1)
│   │   ├── core/             # Application config, logging & security
│   │   ├── db/               # Database session & base models
│   │   ├── models/           # SQLAlchemy / GeoAlchemy ORM entities
│   │   ├── schemas/          # Pydantic data validation schemas
│   │   └── services/         # Business logic (GIS, Ingestion, Risk, MILP, ML)
│   └── tests/                # Pytest unit and integration test suite
├── data/                     # Geospatial and scenario data repository
│   ├── mock/                 # Deterministic offline scenario datasets
│   ├── processed/            # Aggregated H3 grids and cleaned vectors
│   ├── raw/                  # Raw sensor and GIS source files
│   └── schemas/              # Data contract and GeoJSON schemas
├── docker/                   # Dockerfiles and Compose configurations
├── docs/                     # Comprehensive technical documentation
│   └── architecture/         # Architectural blueprint documents
└── frontend/                 # Next.js 14 Web Application
    └── src/
        ├── app/              # Next.js App Router pages
        ├── components/       # UI Components (Map, Dashboard, Analytics, Common)
        ├── hooks/            # Custom React hooks (Geo, WebSocket, State)
        ├── services/         # API client service layer
        ├── types/            # TypeScript interfaces & GeoJSON types
        └── utils/            # GIS calculations, formatters, styling helpers
```

---

## 🚀 Development Roadmap (Phases 0 to 14)

- [x] **Phase 0**: Requirements Analysis & System Architecture Specification *(Current)*
- [ ] **Phase 1**: Repository Setup & Core Documentation Baseline
- [ ] **Phase 2**: Backend Foundation (FastAPI, Config, Logging, Healthchecks)
- [ ] **Phase 3**: Database Architecture & PostGIS Spatial Migration
- [ ] **Phase 4**: Frontend Foundation (Next.js, Tailwind, Design System)
- [ ] **Phase 5**: GIS Map Viewport & Multi-Layer Vector Visualizer
- [ ] **Phase 6**: Disaster Data Ingestion & Resilient Telemetry Adapters
- [ ] **Phase 7**: Multi-Criteria Risk & Vulnerability Indexing Engine
- [ ] **Phase 8**: AI/ML Forecasting & Severity Classification Suite
- [ ] **Phase 9**: Mixed-Integer Linear Programming (MILP) Resource Optimizer
- [ ] **Phase 10**: Tactical Emergency Command & Control (COP) Dashboard
- [ ] **Phase 11**: End-to-End Automated Testing & Validation Suite
- [ ] **Phase 12**: Security Audit, RBAC & Hardening
- [ ] **Phase 13**: Dockerization & Cloud Deployment Orchestration
- [ ] **Phase 14**: SIH 2026 Final Demo Rehearsal & Live Presentation Artifacts

---

## ⚖️ License
Distributed under the **Apache 2.0 License**. See [`LICENSE`](LICENSE) for more details.
