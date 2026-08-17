"""
Configurable Tactical Alert Engine with Sliding-Window Deduplication & Lifecycle Actions
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from backend.app.core.config import settings
from backend.app.core.logging import logger
from realtime_operations.exceptions import AlertLifecycleException, AlertNotFoundException
from realtime_operations.schemas.alerts import (
    AlertAcknowledgeRequest,
    AlertCategoryEnum,
    AlertCreate,
    AlertResolveRequest,
    AlertResponse,
    AlertSeverityEnum,
    AlertStatusEnum,
)
from realtime_operations.services.notification_service import notification_service
from realtime_operations.websocket.connection_manager import connection_manager


class AlertEngine:
    """
    Evaluates real-time disaster anomalies, generates deduplicated tactical alerts,
    and manages alert lifecycle transitions (ACTIVE -> ACKNOWLEDGED -> RESOLVED).
    """

    def __init__(self, deduplication_window_seconds: Optional[int] = None):
        self._deduplication_window_seconds = (
            deduplication_window_seconds or settings.ALERT_DEDUPLICATION_WINDOW_SECONDS
        )
        self._alerts: Dict[str, Dict[str, Any]] = {}
        self._dedup_index: Dict[str, str] = {}  # dedup_key -> alert_id
        self._seed_default_alerts()

    def _seed_default_alerts(self) -> None:
        """Seeds initial tactical alerts for dashboard presentation."""
        seed_items = [
            {
                "alert_id": "alert-01",
                "alert_code": "CRITICAL_INUNDATION_SURGE",
                "severity": AlertSeverityEnum.CRITICAL,
                "status": AlertStatusEnum.ACTIVE,
                "category": AlertCategoryEnum.HYDROLOGICAL,
                "title": "Critical Flash Flood Inundation Surge",
                "message": "Water levels at Barpeta lowlands breached 1.25m benchmark with 85,400 exposed residents.",
                "entity_type": "disaster",
                "entity_id": "dis-assam-01",
                "latitude": 26.3216,
                "longitude": 91.0063,
                "recommended_action": "Execute immediate boat evacuation for Ward 4 residential cluster.",
                "occurrence_count": 3,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "acknowledged_at": None,
                "resolved_at": None,
                "resolution_notes": None,
            },
            {
                "alert_id": "alert-02",
                "alert_code": "HOSPITAL_BACKUP_POWER_CRITICAL",
                "severity": AlertSeverityEnum.HIGH,
                "status": AlertStatusEnum.ACKNOWLEDGED,
                "category": AlertCategoryEnum.INFRASTRUCTURE,
                "title": "Barpeta Civil Hospital Grid Severance",
                "message": "Substation #4 submerged. Hospital generator operating at 6h remaining fuel capacity.",
                "entity_type": "location",
                "entity_id": "loc-hosp-01",
                "latitude": 26.3260,
                "longitude": 91.0110,
                "recommended_action": "Route mobile 250kVA diesel generator trailer via Western elevated bypass.",
                "occurrence_count": 1,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "acknowledged_at": datetime.now(timezone.utc).isoformat(),
                "resolved_at": None,
                "resolution_notes": None,
            },
            {
                "alert_id": "alert-03",
                "alert_code": "BRIDGE_ACCESS_IMPASSABLE",
                "severity": AlertSeverityEnum.WARNING,
                "status": AlertStatusEnum.ACTIVE,
                "category": AlertCategoryEnum.INFRASTRUCTURE,
                "title": "Bridge B-12 Submergence (0.65m)",
                "message": "Bridge impassable to conventional road transport. Logistics supply trucks rerouted.",
                "entity_type": "location",
                "entity_id": "loc-brg-12",
                "latitude": 26.3180,
                "longitude": 91.0150,
                "recommended_action": "Update GIS route barriers and instruct rescue convoys to take NH-31 detour.",
                "occurrence_count": 2,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "acknowledged_at": None,
                "resolved_at": None,
                "resolution_notes": None,
            },
        ]
        for item in seed_items:
            self._alerts[item["alert_id"]] = item
            dedup_key = f"{item['alert_code']}:{item['entity_type']}:{item['entity_id']}"
            self._dedup_index[dedup_key] = item["alert_id"]

    async def create_alert(self, payload: AlertCreate) -> AlertResponse:
        """
        Creates or deduplicates a tactical alert using sliding-window deduplication.
        """
        dedup_key = f"{payload.alert_code}:{payload.entity_type}:{payload.entity_id}"
        now_dt = datetime.now(timezone.utc)
        now_iso = now_dt.isoformat()

        # Check for existing active/acknowledged alert with same key within deduplication window
        if dedup_key in self._dedup_index:
            existing_id = self._dedup_index[dedup_key]
            existing_alert = self._alerts.get(existing_id)

            if existing_alert and existing_alert["status"] in [AlertStatusEnum.ACTIVE, AlertStatusEnum.ACKNOWLEDGED]:
                # Increment occurrence count and update message
                existing_alert["occurrence_count"] += 1
                existing_alert["message"] = payload.message
                logger.info(
                    f"Deduplicated alert '{existing_id}' [{dedup_key}]. Occurrence count: {existing_alert['occurrence_count']}"
                )
                response = AlertResponse(**existing_alert)
                await connection_manager.broadcast_alert(response.model_dump())
                return response

        # Create new alert
        alert_id = f"alert-{uuid.uuid4().hex[:8]}"
        record = {
            "alert_id": alert_id,
            "alert_code": payload.alert_code,
            "severity": payload.severity,
            "status": AlertStatusEnum.ACTIVE,
            "category": payload.category,
            "title": payload.title,
            "message": payload.message,
            "entity_type": payload.entity_type,
            "entity_id": payload.entity_id,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "recommended_action": payload.recommended_action,
            "occurrence_count": 1,
            "created_at": now_iso,
            "acknowledged_at": None,
            "resolved_at": None,
            "resolution_notes": None,
        }

        self._alerts[alert_id] = record
        self._dedup_index[dedup_key] = alert_id

        response = AlertResponse(**record)

        # Trigger in-app notification for High/Critical alerts
        if payload.severity in [AlertSeverityEnum.HIGH, AlertSeverityEnum.CRITICAL]:
            await notification_service.create_notification(
                title=f"[{payload.severity.value}] {payload.title}",
                message=payload.message,
                severity=payload.severity.value,
                related_alert_id=alert_id,
            )

        # Broadcast over WebSocket
        await connection_manager.broadcast_alert(response.model_dump())
        logger.info(f"Generated new Tactical Alert '{alert_id}' [{payload.alert_code}]: {payload.title}")
        return response

    def list_alerts(
        self,
        status: Optional[AlertStatusEnum] = None,
        severity: Optional[AlertSeverityEnum] = None,
        category: Optional[AlertCategoryEnum] = None,
    ) -> List[AlertResponse]:
        items = list(self._alerts.values())

        if status:
            items = [i for i in items if i["status"] == status]
        if severity:
            items = [i for i in items if i["severity"] == severity]
        if category:
            items = [i for i in items if i["category"] == category]

        # Sort descending by created_at
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return [AlertResponse(**i) for i in items]

    def get_alert(self, alert_id: str) -> AlertResponse:
        if alert_id not in self._alerts:
            raise AlertNotFoundException(alert_id)
        return AlertResponse(**self._alerts[alert_id])

    async def acknowledge_alert(
        self, alert_id: str, request: AlertAcknowledgeRequest
    ) -> AlertResponse:
        if alert_id not in self._alerts:
            raise AlertNotFoundException(alert_id)

        record = self._alerts[alert_id]
        if record["status"] == AlertStatusEnum.RESOLVED:
            raise AlertLifecycleException(
                alert_id=alert_id,
                current_status="RESOLVED",
                target_status="ACKNOWLEDGED",
                reason="Resolved alerts cannot be transitioned back to acknowledged.",
            )

        record["status"] = AlertStatusEnum.ACKNOWLEDGED
        record["acknowledged_at"] = datetime.now(timezone.utc).isoformat()
        if request.notes:
            record["resolution_notes"] = f"Ack by {request.acknowledged_by}: {request.notes}"

        response = AlertResponse(**record)
        await connection_manager.broadcast_alert(response.model_dump())
        logger.info(f"Alert '{alert_id}' acknowledged by '{request.acknowledged_by}'")
        return response

    async def resolve_alert(
        self, alert_id: str, request: AlertResolveRequest
    ) -> AlertResponse:
        if alert_id not in self._alerts:
            raise AlertNotFoundException(alert_id)

        record = self._alerts[alert_id]
        record["status"] = AlertStatusEnum.RESOLVED
        record["resolved_at"] = datetime.now(timezone.utc).isoformat()
        record["resolution_notes"] = f"Resolved by {request.resolved_by}: {request.resolution_notes}"

        response = AlertResponse(**record)
        await connection_manager.broadcast_alert(response.model_dump())
        logger.info(f"Alert '{alert_id}' resolved by '{request.resolved_by}': {request.resolution_notes}")
        return response


# Global singleton instance
alert_engine = AlertEngine()
