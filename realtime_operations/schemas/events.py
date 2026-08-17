"""
Pydantic Schemas for Operational Events
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import uuid
from pydantic import BaseModel, Field


class EventTypeEnum(str, Enum):
    # Disaster events
    DISASTER_CREATED = "DISASTER_CREATED"
    DISASTER_UPDATED = "DISASTER_UPDATED"
    DISASTER_ESCALATED = "DISASTER_ESCALATED"
    DISASTER_RESOLVED = "DISASTER_RESOLVED"

    # Risk events
    RISK_LEVEL_CHANGED = "RISK_LEVEL_CHANGED"

    # Resource events
    RESOURCE_ADDED = "RESOURCE_ADDED"
    RESOURCE_UPDATED = "RESOURCE_UPDATED"
    RESOURCE_ALLOCATED = "RESOURCE_ALLOCATED"
    RESOURCE_RELEASED = "RESOURCE_RELEASED"
    RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"

    # Response plan events
    RESPONSE_PLAN_CREATED = "RESPONSE_PLAN_CREATED"
    RESPONSE_PLAN_UPDATED = "RESPONSE_PLAN_UPDATED"
    RESPONSE_PLAN_COMPLETED = "RESPONSE_PLAN_COMPLETED"

    # Alert events
    ALERT_CREATED = "ALERT_CREATED"
    ALERT_ACKNOWLEDGED = "ALERT_ACKNOWLEDGED"
    ALERT_RESOLVED = "ALERT_RESOLVED"


class OperationalEventCreate(BaseModel):
    event_type: EventTypeEnum
    entity_type: str = Field(..., description="disaster, resource, risk_zone, response_plan, alert")
    entity_id: str = Field(..., description="ID of the related entity")
    severity: str = Field(default="INFO", description="INFO, WARNING, HIGH, CRITICAL")
    source: str = Field(default="SYSTEM", description="GIS_ENGINE, AI_SERVICES, OPTIMIZATION_ENGINE, EOC_COMMAND")
    latitude: Optional[float] = Field(default=None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(default=None, ge=-180.0, le=180.0)
    payload: Dict[str, Any] = Field(default_factory=dict)


class OperationalEventResponse(BaseModel):
    event_id: str
    event_type: EventTypeEnum
    entity_type: str
    entity_id: str
    severity: str
    source: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str
