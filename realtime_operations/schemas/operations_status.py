"""
Pydantic Schemas for Operations Command Status Overview
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class OperationsStatusResponse(BaseModel):
    active_incidents: int = Field(..., ge=0)
    critical_incidents: int = Field(..., ge=0)
    active_alerts: int = Field(..., ge=0)
    critical_alerts: int = Field(..., ge=0)
    total_response_units: int = Field(..., ge=0)
    available_response_units: int = Field(..., ge=0)
    allocated_response_units: int = Field(..., ge=0)
    resource_shortages: int = Field(..., ge=0)
    active_response_plans: int = Field(..., ge=0)
    system_readiness_status: str = Field(
        default="OPERATIONAL_ACTIVE",
        description="OPERATIONAL_ACTIVE, ELEVATED_ALERT, CRITICAL_DEFCON_1",
    )
    connected_clients_count: int = Field(default=0, ge=0)
    last_sync_timestamp: str
