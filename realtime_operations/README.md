# 🛰️ JeevanGrid Real-Time Emergency Operations, Alerts & Command Center Core

## 1. Overview
The **JeevanGrid Real-Time Operations Layer** provides centralized command-and-control telemetry, standardized operational event ingestion, multi-tier tactical alerts with sliding-window deduplication, in-app notification center, and bidirectional WebSocket streams for Emergency Operations Centers (EOCs).

---

## 2. Architecture & Design Principles

```text
realtime_operations/
├── models.py                  # SQLAlchemy PostGIS ORM entities (OperationalEvent, Alert, Notification)
├── exceptions.py              # Domain exceptions (AlertNotFound, AlertLifecycle, InvalidEventPayload)
├── schemas/
│   ├── alerts.py              # AlertCreate, AlertResponse, AlertAcknowledge/Resolve schemas
│   ├── events.py              # EventTypeEnum, OperationalEventCreate/Response schemas
│   ├── notifications.py       # NotificationResponse, NotificationListResponse schemas
│   └── operations_status.py   # Unified OperationsStatusResponse schema
├── services/
│   ├── alert_engine.py        # Configurable alert evaluator with 300s sliding-window deduplication
│   ├── event_service.py       # Event ingestion, ring-buffer persistence, and automated alert dispatch
│   ├── notification_service.py # In-app notification delivery and read-state tracker
│   └── operations_status_service.py # Aggregated EOC readiness and live fleet telemetry metrics
└── websocket/
    └── connection_manager.py  # Thread-safe async WebSocket manager with client registry & heartbeat
```

---

## 3. Core Capabilities

### A. Standardized Operational Event Lifecycle
- Event types: `DISASTER_CREATED`, `DISASTER_ESCALATED`, `RISK_LEVEL_CHANGED`, `RESOURCE_ALLOCATED`, `RESOURCE_EXHAUSTED`, `RESPONSE_PLAN_CREATED`, `ALERT_CREATED`, `ALERT_RESOLVED`.
- Capped in-memory ring buffer (up to 1,000 events) for fast query access.
- Automated alert triggers: High/Critical severity events automatically dispatch tactical alerts and in-app notifications.

### B. Tactical Alert Engine & Sliding-Window Deduplication
- Multi-tier severity: `INFO`, `WARNING`, `HIGH`, `CRITICAL`.
- Multi-category classification: `HYDROLOGICAL`, `LOGISTICS`, `INFRASTRUCTURE`, `TACTICAL_DISPATCH`, `GENERAL`.
- Deduplication Key: `f"{alert_code}:{entity_type}:{entity_id}"`. If duplicate alerts burst within `ALERT_DEDUPLICATION_WINDOW_SECONDS` (300s), the engine increments `occurrence_count` and updates telemetry without creating duplicate spam entries.
- State Machine Lifecycle:
  $$\text{ACTIVE} \xrightarrow{\text{Acknowledge}} \text{ACKNOWLEDGED} \xrightarrow{\text{Resolve}} \text{RESOLVED}$$

### C. In-App Notification Center
- Unread badge counter, individual mark-as-read, and bulk `mark-all-read` capabilities.
- Linked alert drill-down references for emergency operators.

### D. WebSocket Telemetry Stream (`/api/v1/ws/operations`)
- Protocol: JSON stream with `OPERATIONAL_EVENT`, `TACTICAL_ALERT`, and `NOTIFICATION` message types.
- Ping/Pong heartbeat every 30 seconds for dead-connection cleanup.

---

## 4. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/operations/status` | Unified EOC readiness status & counters |
| `GET` | `/api/v1/events` | List operational events (filtered by type/severity) |
| `POST` | `/api/v1/events` | Ingest operational event & evaluate alert rules |
| `GET` | `/api/v1/alerts` | List active, acknowledged, or resolved tactical alerts |
| `POST` | `/api/v1/alerts` | Create or deduplicate a tactical alert |
| `GET` | `/api/v1/alerts/{alert_id}` | Retrieve specific tactical alert details |
| `POST` | `/api/v1/alerts/{alert_id}/acknowledge` | Transition alert to `ACKNOWLEDGED` status |
| `POST` | `/api/v1/alerts/{alert_id}/resolve` | Transition alert to `RESOLVED` status with notes |
| `GET` | `/api/v1/notifications` | List in-app notifications with unread counter |
| `POST` | `/api/v1/notifications/{id}/read` | Mark single notification as read |
| `POST` | `/api/v1/notifications/mark-all-read` | Mark all unread notifications as read |
| `WS` | `/api/v1/ws/operations` | Live WebSocket operational telemetry stream |

---

## 5. Configuration & Environment Variables

Configure the following variables in `.env` (refer to `.env.example`):
```env
REALTIME_ENABLED=true
ALERT_DEDUPLICATION_WINDOW_SECONDS=300
REALTIME_HEARTBEAT_SECONDS=30
NEXT_PUBLIC_WS_BASE_URL=ws://localhost:8000/api/v1/ws/operations
```

---

## 6. Running Tests

```bash
# Run Phase 8 Real-Time operations tests
python -m pytest backend/tests/realtime -v

# Run the complete test suite (All 93 tests)
pytest -v
```
