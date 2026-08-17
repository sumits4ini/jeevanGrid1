"""
Unit Tests for Incident Prioritization Algorithm
"""

import pytest
from response_optimization.algorithms.priority import (
    compute_incident_priority,
    rank_and_prioritize_incidents,
)
from response_optimization.schemas.incident_priority import (
    IncidentItem,
    PriorityLevelEnum,
)


def test_compute_incident_priority_critical_flood():
    """Verifies prioritization of severe flood event."""
    incident = IncidentItem(
        id="inc-01",
        name="Barpeta Flash Flood Severe",
        disaster_type="FLOOD",
        severity_level=5,
        latitude=26.3216,
        longitude=91.0063,
        affected_population=85000,
        inundation_depth_m=1.8,
    )
    result = compute_incident_priority(incident)
    assert result.priority_score >= 0.75
    assert result.priority_level == PriorityLevelEnum.CRITICAL
    assert result.contributing_factors.severity_score == 1.0
    assert "Critical" in result.explanation


def test_compute_incident_priority_low_incident():
    """Verifies low severity incident produces low/medium tier."""
    incident = IncidentItem(
        id="inc-02",
        name="Localized Minor Waterlogging",
        disaster_type="FLOOD",
        severity_level=1,
        latitude=26.3500,
        longitude=91.0500,
        affected_population=50,
        inundation_depth_m=0.1,
    )
    result = compute_incident_priority(incident)
    assert result.priority_score < 0.40
    assert result.priority_level in [PriorityLevelEnum.LOW, PriorityLevelEnum.MEDIUM]


def test_rank_multiple_incidents():
    """Verifies ranking orders incidents strictly descending by priority score."""
    incidents = [
        IncidentItem(
            id="inc-low",
            name="Low Warning",
            disaster_type="FLOOD",
            severity_level=2,
            latitude=26.3000,
            longitude=91.0000,
            affected_population=500,
        ),
        IncidentItem(
            id="inc-high",
            name="Catastrophic Flood Wave",
            disaster_type="FLOOD",
            severity_level=5,
            latitude=26.3216,
            longitude=91.0063,
            affected_population=120000,
            inundation_depth_m=2.1,
        ),
        IncidentItem(
            id="inc-mid",
            name="Moderate River Surge",
            disaster_type="FLOOD",
            severity_level=3,
            latitude=26.3300,
            longitude=91.0200,
            affected_population=15000,
        ),
    ]

    ranked = rank_and_prioritize_incidents(incidents)
    assert len(ranked) == 3
    assert ranked[0].incident_id == "inc-high"
    assert ranked[0].priority_rank == 1
    assert ranked[1].incident_id == "inc-mid"
    assert ranked[1].priority_rank == 2
    assert ranked[2].incident_id == "inc-low"
    assert ranked[2].priority_rank == 3
