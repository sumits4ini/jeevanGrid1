# 🤖 JeevanGrid AI Intelligence & Decision Support Core

## 1. Overview
The **JeevanGrid AI Services Layer** provides structured multi-source spatial reasoning, automated risk intelligence, and decision support for Emergency Operations Centers (EOCs). It consumes spatial telemetry directly from `gis_engine`, integrates with live database models, and generates grounded, actionable operational directives without fabricating unverified claims.

---

## 2. Architecture & Design Principles

```text
ai_services/
├── providers/
│   ├── base.py            # BaseAIProvider abstract interface
│   ├── factory.py         # AI provider factory with safe fallback logic
│   └── mock_provider.py   # Deterministic, rule-informed AI provider (UNDRR & NDMA protocols)
├── services/
│   ├── ai_manager.py      # Unified AIServiceManager coordinator
│   ├── recommendation_service.py # Categorized Incident Command recommendations
│   ├── resource_service.py # Fleet proximity & suitability prioritization
│   └── risk_service.py    # Spatial hazard & vulnerability risk intelligence
└── schemas/
    └── __init__.py        # Re-exported Pydantic request/response schemas
```

### Core Architecture Highlights:
- **Provider Abstraction**: Decoupled interface `BaseAIProvider` allowing zero-downtime swapping between `MockAIProvider`, `GeminiProvider`, `OpenAIProvider`, or local SLMs (e.g. Llama-3/Mistral).
- **Graceful Failure Handling**: If an external provider experiences network latency, rate limits, or invalid outputs, the factory fails over to the high-fidelity deterministic engine.
- **Strict Schema Enforcement**: All AI outputs are parsed and validated through Pydantic schemas before returning to API consumers.

---

## 3. Core AI Modules

### A. Disaster Risk Intelligence (`DisasterRiskService`)
- Computes composite risk score:
  $$\text{Risk Score} = 0.40 \cdot \text{Hazard Intensity} + 0.35 \cdot \text{Depth Factor} + 0.25 \cdot \text{Population Exposure Factor}$$
- Classifies operational alert level: `LOW`, `MODERATE`, `HIGH`, `CRITICAL` (DEFCON 1 to 4).
- Enriches spatial context with nearby critical infrastructure queried from `gis_engine`.

### B. Resource Prioritization (`ResourcePrioritizationService`)
- Evaluates available emergency fleet units (Boats, Ambulances, NDRF teams).
- Computes transit ETAs using Haversine great-circle distances.
- Weighs vehicle suitability against disaster type (e.g. shallow-draft boats for flood rescue, ALS ambulances for trauma).
- Assigns actionable mission tasks and urgency ratings (`IMMEDIATE`, `URGENT`, `STANDARD`, `STANDBY`).

### C. AI Recommendation Engine (`RecommendationService`)
- Generates structured, categorized guidelines across:
  - `IMMEDIATE_ACTION` (0 - 30 mins)
  - `RESOURCE_DEPLOYMENT` (30 - 60 mins)
  - `INFRASTRUCTURE_SAFEGUARD` (1 - 2 hours)
  - `EVACUATION_CONSIDERATION` (2 - 4 hours)
  - `MONITORING_FOLLOWUP` (Ongoing)

---

## 4. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/ai/status` | AI provider telemetry and readiness health check |
| `POST` | `/api/v1/ai/risk-analysis` | AI-assisted multi-factor disaster risk assessment |
| `POST` | `/api/v1/ai/resource-priority` | Prioritized rescue fleet allocation by proximity & urgency |
| `POST` | `/api/v1/ai/recommendations` | Actionable Incident Command operational directives |

---

## 5. Configuration & Environment Variables

Configure the following variables in `.env` (refer to `.env.example`):
```env
AI_PROVIDER=mock                      # Options: "mock", "gemini", "openai", "anthropic"
AI_API_KEY=                           # Leave blank for local mock mode
AI_MODEL_NAME=gemini-1.5-flash        # Target LLM model identifier
AI_TEMPERATURE=0.2                    # Sampling temperature for deterministic outputs
AI_REQUEST_TIMEOUT_SECONDS=10.0       # Timeout in seconds
ENABLE_AI_RECOMMENDATION_ENGINE=true  # Enable/disable decision engine
```

---

## 6. Running Tests
Run the comprehensive AI test suite:
```bash
python -m pytest backend/tests/ai -v
```
Or run the full project backend & GIS test suite:
```bash
pytest -v
```
