"""
Standardized Operational Event Ingestion, Persistence & Alert Rule Dispatcher
"""

from collections import deque
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from backend.app.core.config import settings
from backend.app.core.logging import logger
from realtime_operations.schemas.alerts import (
    AlertCategoryEnum,
    AlertCreate,
    AlertSeverityEnum,
)
from realtime_operations.schemas.events import (
    EventTypeEnum,
    OperationalEventCreate,
    OperationalEventResponse,
)
from realtime_operations.services.alert_engine import alert_engine
from realtime_operations.websocket.connection_manager import connection_manager


class OperationalEventService:
    """
    Ingests operational lifecycle events, evaluates automated alert rules,
    and broadcasts events over WebSocket to dashboard clients.
    """

    def __init__(self, max_history: Optional[int] = None):
        self._max_history = max_history or settings.MAX_IN_MEMORY_EVENTS
        self._events: deque = deque(maxlen=self._max_history)
        self._seed_default_events()

    def _seed_default_events(self) -> None:
        """Seeds initial operational events for dashboard presentation."""
        default_events = [
            {
                "event_id": "evt-01",
                "event_type": EventTypeEnum.DISASTER_CREATED,
                "entity_type": "disaster",
                "entity_id": "dis-assam-01",
                "severity": "CRITICAL",
                "source": "GIS_ENGINE",
                "latitude": 26.3216,
                "longitude": 91.0063,
                "payload": {"name": "Assam Brahmaputra Basin Inundation", "severity_level": 4},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            {
                "event_id": "evt-02",
                "event_type": EventTypeEnum.RISK_LEVEL_CHANGED,
                "entity_type": "disaster",
                "entity_id": "dis-assam-01",
                "severity": "CRITICAL",
                "source": "AI_SERVICES",
                "latitude": 26.3216,
                "longitude": 91.0063,
                "payload": {"risk_score": 0.88, "risk_level": "CRITICAL", "confidence": 0.94},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            {
                "event_id": "evt-03",
                "event_type": EventTypeEnum.RESOURCE_ALLOCATED,
                "entity_type": "resource",
                "entity_id": "ru-boat-01",
                "severity": "INFO",
                "source": "OPTIMIZATION_ENGINE",
                "latitude": 26.3200,
                "longitude": 91.0080,
                "payload": {"target_incident": "dis-assam-01", "eta_minutes": 4},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            {
                "event_id": "evt-04",
                "event_type": EventTypeEnum.ALERT_CREATED,
                "entity_type": "alert",
                "entity_id": "alert-01",
                "severity": "CRITICAL",
                "source": "ALERT_ENGINE",
                "latitude": 26.3216,
                "longitude": 91.0063,
                "payload": {"alert_code": "CRITICAL_INUNDATION_SURGE"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        ]
        for item in default_events:
            self._events.append(item)

    async def ingest_event(self, event_in: OperationalEventCreate) -> OperationalEventResponse:
        """
        Ingests an event, persists to memory/db, evaluates alert rules,
        and broadcasts to connected WebSocket clients.
        """
        event_id = f"evt-{uuid.uuid4().hex[:8]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "event_id": event_id,
            "event_type": event_in.event_type,
            "entity_type": event_in.entity_type,
            "entity_id": event_in.entity_id,
            "severity": event_in.severity,
            "source": event_in.source,
            "latitude": event_in.latitude,
            "longitude": event_in.longitude,
            "payload": event_in.payload,
            "timestamp": now_iso,
        }

        self._events.append(record)
        response = OperationalEventResponse(**record)

        # 1. Automated alert rules evaluation
        await self._evaluate_event_alert_rules(event_in)

        # 2. Broadcast event to WebSocket clients
        await connection_manager.broadcast_event(response.model_dump())
        logger.info(f"Ingested operational event '{event_id}' [{event_in.event_type.value}] from {event_in.source}")
        return response

    async def _evaluate_event_alert_rules(self, event: OperationalEventCreate) -> None:
        """Evaluates operational triggers to generate tactical alerts automatically."""
        # Rule 1: High/Critical disaster escalations generate alerts
        if event.event_type in [EventTypeEnum.DISASTER_ESCALATED, EventTypeEnum.RISK_LEVEL_CHANGED]:
            if event.severity in ["HIGH", "CRITICAL"]:
                await alert_engine.create_alert(
                    AlertCreate(
                        alert_code="HAZARD_RISK_ESCALATION",
                        severity=AlertSeverityEnum.CRITICAL if event.severity == "CRITICAL" else AlertSeverityEnum.HIGH,
                        category=AlertCategoryEnum.HYDROLOGICAL,
                        title=f"Disaster Risk Escalation Alert ({event.entity_id})",
                        message=f"Risk level escalated to {event.severity}. Immediate multi-agency review required.",
                        entity_type=event.entity_type,
                        entity_id=event.entity_id,
                        latitude=event.latitude,
                        longitude=event.longitude,
                        recommended_action="Review and re-solve emergency dispatch allocations.",
                    )
                )

        # Rule 2: Resource exhaustion triggers logistics alert
        elif event.event_type == EventTypeEnum.RESOURCE_EXHAUSTED:
            await alert_engine.create_alert(
                AlertCreate(
                    alert_code="RESOURCE_DEFICIT_EXHAUSTION",
                    severity=AlertSeverityEnum.HIGH,
                    category=AlertCategoryEnum.LOGISTICS,
                    title="Emergency Resource Unit Exhaustion",
                    message=f"Resource category for {event.entity_id} exhausted within primary response perimeter.",
                    entity_type=event.entity_type,
                    entity_id=event.entity_id,
                    latitude=event.latitude,
                    longitude=event.longitude,
                    recommended_action="Trigger inter-district mutual aid requisition.",
                )
            )

    def list_events(
        self,
        event_type: Optional[EventTypeEnum] = None,
        severity: Optional[str] = None,
        entity_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[OperationalEventResponse]:
        items = list(self._events)

        if event_type:
            items = [i for i in items if i["event_type"] == event_type]
        if severity:
            items = [i for i in items if i["severity"] == severity]
        if entity_type:
            items = [i for i in items if i["entity_type"] == entity_type]

        # Return most recent events first
        items.sort(key=lambda x: x["timestamp"], reverse=True)
        return [OperationalEventResponse(**i) for i in items[:limit]]


# Global singleton instance
event_service = OperationalEventService()
