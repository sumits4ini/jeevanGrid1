"""
Pydantic Schemas for Tactical Alerts and Lifecycle Actions
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AlertSeverityEnum(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"


class AlertCategoryEnum(str, Enum):
    HYDROLOGICAL = "HYDROLOGICAL"
    LOGISTICS = "LOGISTICS"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    TACTICAL_DISPATCH = "TACTICAL_DISPATCH"
    GENERAL = "GENERAL"


class AlertCreate(BaseModel):
    alert_code: str = Field(..., description="E.g. INUNDATION_SURGE, RESOURCE_DEFICIT_BOAT")
    severity: AlertSeverityEnum = Field(default=AlertSeverityEnum.WARNING)
    category: AlertCategoryEnum = Field(default=AlertCategoryEnum.GENERAL)
    title: str = Field(..., min_length=3, max_length=200)
    message: str = Field(..., min_length=5)
    entity_type: str = Field(..., description="disaster, resource, location")
    entity_id: str = Field(...)
    latitude: Optional[float] = Field(default=None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(default=None, ge=-180.0, le=180.0)
    recommended_action: Optional[str] = None


class AlertAcknowledgeRequest(BaseModel):
    acknowledged_by: str = Field(default="EOC_OPERATOR", description="Operator identifier")
    notes: Optional[str] = Field(default=None, description="Operational acknowledgment notes")


class AlertResolveRequest(BaseModel):
    resolved_by: str = Field(default="EOC_COMMANDER", description="Commander identifier")
    resolution_notes: str = Field(..., min_length=3, description="Summary of resolution actions taken")


class AlertResponse(BaseModel):
    alert_id: str
    alert_code: str
    severity: AlertSeverityEnum
    status: AlertStatusEnum
    category: AlertCategoryEnum
    title: str
    message: str
    entity_type: str
    entity_id: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    recommended_action: Optional[str] = None
    occurrence_count: int = 1
    created_at: str
    acknowledged_at: Optional[str] = None
    resolved_at: Optional[str] = None
    resolution_notes: Optional[str] = None
