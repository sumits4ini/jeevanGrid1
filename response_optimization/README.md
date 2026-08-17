# ⚡ JeevanGrid Emergency Response Optimization & Resource Allocation Core

## 1. Overview
The **JeevanGrid Response Optimization Engine** transforms multi-hazard spatial intelligence and AI risk predictions into actionable, explainable, and constraint-compliant emergency deployment plans.

---

## 2. Architecture & Design Principles

```text
response_optimization/
├── algorithms/
│   ├── priority.py        # MCDA multi-factor incident priority ranking
│   ├── suitability.py     # Deterministic resource-to-hazard suitability scoring
│   └── allocation.py      # Capacitated greedy allocation & shortage identification
├── routing/
│   ├── base.py            # BaseRoutingProvider abstract interface
│   ├── factory.py         # Routing provider factory
│   └── local_provider.py  # Geodesic WGS84 routing with terrain & vehicle speed modeling
├── schemas/
│   ├── allocation.py       # Pydantic schemas for assignments and shortages
│   ├── incident_priority.py # IncidentItem and PrioritizedIncident schemas
│   ├── response_plan.py    # ResponsePlanRequest and ResponsePlanResponse schemas
│   └── routing.py          # RoutingRequest and RoutingResponse schemas
└── services/
    ├── allocation_service.py # Fleet allocation coordinator
    ├── optimization_service.py # High-level Response Plan orchestrator
    ├── routing_service.py    # Distance & ETA calculator
    └── scoring_service.py    # Prioritization and suitability scorer
```

---

## 3. Mathematical Formulations & Algorithms

### A. Incident Priority Scoring (MCDA)
$$\text{Priority Score} = w_{\text{sev}} S_{\text{sev}} + w_{\text{risk}} S_{\text{risk}} + w_{\text{pop}} S_{\text{pop}} + w_{\text{geo}} S_{\text{geo}} + w_{\text{urg}} S_{\text{urg}} + w_{\text{short}} S_{\text{short}}$$

Where:
- $S_{\text{sev}} = \frac{\text{Severity Level}}{5}$
- $S_{\text{pop}} = \min\left(1.0, \frac{\log_{10}(\max(10, \text{Pop}))}{6}\right)$
- $S_{\text{geo}} = \min\left(1.0, \frac{\text{Inundation Depth (m)}}{2.5}\right)$
- Classification: $\ge 0.75 \implies \text{CRITICAL}$, $0.50 - 0.74 \implies \text{HIGH}$, $0.25 - 0.49 \implies \text{MEDIUM}$, $< 0.25 \implies \text{LOW}$.

### B. Resource Suitability Scoring
$$\text{Suitability} = 0.40 \cdot \text{TypeMatch} + 0.35 \cdot \text{Proximity} + 0.15 \cdot \text{Availability} + 0.10 \cdot \text{UrgencyFit}$$

Where:
- $\text{TypeMatch}$: Compatibility weight between asset type (e.g. `RESCUE_BOAT`, `AMBULANCE`) and disaster category (`FLOOD`, `CYCLONE`, `EARTHQUAKE`).
- $\text{Proximity} = 1.0 - \min\left(1.0, \frac{\text{Distance (km)}}{\text{Max Radius}}\right)$.

### C. Capacitated Allocation & Shortage Detection
1. Incidents are sorted in descending order by MCDA priority score.
2. For each incident and required resource type, candidate units within range are ranked by suitability.
3. Units are assigned up to demand quotas without double-allocating any committed asset.
4. Any unmet demand is explicitly flagged as a `ResourceShortage` with mutual aid recommendations.

---

## 4. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/optimization/prioritize-incidents` | MCDA priority ranking across disaster incidents |
| `POST` | `/api/v1/optimization/allocate-resources` | Capacitated resource matching & shortage detection |
| `POST` | `/api/v1/optimization/response-plan` | End-to-end tactical response plan generation |
| `GET` | `/api/v1/optimization/resource-status` | Fleet availability counts and readiness percentage |
| `GET` | `/api/v1/optimization/incidents/{incident_id}/resources` | Nearby suited response units for a specific incident |

---

## 5. Running Tests

```bash
# Run the dedicated Phase 7 optimization test suite
python -m pytest backend/tests/optimization -v

# Run the complete test suite (Backend + Database + GIS + AI + Optimization)
pytest -v
```
