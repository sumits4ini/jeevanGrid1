"""
Tests for GIS Operational Layers and LayerRegistry
"""

from gis_engine.layers.disaster import DisasterLayer
from gis_engine.layers.hazard_zone import HazardZoneLayer
from gis_engine.layers.location import LocationLayer
from gis_engine.layers.registry import LayerRegistry
from gis_engine.layers.resource import ResourceLayer
from gis_engine.schemas.geometry import BoundingBox


def test_layer_registry_initialization():
    """Verifies default layer registration and counts."""
    registry = LayerRegistry()
    summary = registry.list_layers()
    assert summary.total_layers == 4

    expected_layer_ids = {"disasters", "hazard_zones", "infrastructure", "response_units"}
    registered_ids = {layer.layer_id for layer in summary.layers}
    assert expected_layer_ids == registered_ids


def test_disaster_layer_features():
    """Verifies DisasterLayer returns GeoJSON FeatureCollection."""
    layer = DisasterLayer()
    fc = layer.get_feature_collection()
    assert fc.type == "FeatureCollection"
    assert len(fc.features) >= 2

    first_feat = fc.features[0]
    assert first_feat.type == "Feature"
    assert "disaster_type" in first_feat.properties
    assert first_feat.geometry.type == "Point"


def test_hazard_zone_layer_features():
    """Verifies HazardZoneLayer returns MultiPolygon GeoJSON."""
    layer = HazardZoneLayer()
    fc = layer.get_feature_collection()
    assert fc.type == "FeatureCollection"
    assert len(fc.features) >= 1
    assert fc.features[0].geometry.type == "MultiPolygon"


def test_registry_bounding_box_query():
    """Verifies spatial bounding box filtering across layers."""
    registry = LayerRegistry()
    # Query bbox covering Barpeta, Assam
    bbox = BoundingBox(min_lng=90.90, min_lat=26.20, max_lng=91.10, max_lat=26.40)

    fc = registry.query_features(layer_ids=["infrastructure"], bbox=bbox)
    assert fc.type == "FeatureCollection"
    assert len(fc.features) > 0


def test_registry_find_nearby():
    """Verifies proximity search across layers."""
    registry = LayerRegistry()
    # Search around Barpeta center with 10 km radius
    resp = registry.find_nearby(
        center_lat=26.3216,
        center_lng=91.0063,
        radius_meters=10000.0,
    )
    assert resp.total_found > 0
    assert len(resp.features) > 0
    # First item must be closest (ascending order)
    if len(resp.features) > 1:
        assert resp.features[0].distance_meters <= resp.features[1].distance_meters
