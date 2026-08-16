"""
Spatial Intersection Evaluation Utilities
"""

from typing import Any, Dict, List, Optional, Union
import shapely
from gis_engine.geometry.transforms import buffer_geometry_meters
from gis_engine.geometry.validation import safe_to_geojson, safe_to_shapely
from gis_engine.schemas.geometry import GeoJSONFeature, GeoJSONFeatureCollection
from gis_engine.schemas.layer import IntersectedLayerResult


def evaluate_polygon_intersections(
    target_polygon: Union[Dict[str, Any], shapely.Geometry],
    candidate_features: List[Dict[str, Any]],
    layer_id: str,
    buffer_meters: float = 0.0,
) -> IntersectedLayerResult:
    """
    Evaluates which candidate features intersect with the target polygon (with optional buffer).
    Candidate features can be Points, LineStrings, or Polygons.
    """
    target_shapely = safe_to_shapely(target_polygon)
    if buffer_meters > 0:
        target_shapely = buffer_geometry_meters(target_shapely, buffer_meters)

    intersected_features: List[GeoJSONFeature] = []

    for item in candidate_features:
        geom_data = item.get("geometry")
        if not geom_data and "latitude" in item and "longitude" in item:
            geom_data = {
                "type": "Point",
                "coordinates": [float(item["longitude"]), float(item["latitude"])],
            }

        if not geom_data:
            continue

        try:
            cand_shapely = safe_to_shapely(geom_data)
            if target_shapely.intersects(cand_shapely):
                properties = item.get("properties", {})
                if not properties:
                    properties = {k: v for k, v in item.items() if k not in ["geometry"]}

                # If candidate is a polygon, also compute intersection geometry
                if cand_shapely.geom_type in ["Polygon", "MultiPolygon"]:
                    intersection_geom = target_shapely.intersection(cand_shapely)
                    feature_geom = safe_to_geojson(intersection_geom)
                else:
                    feature_geom = safe_to_geojson(cand_shapely)

                intersected_features.append(
                    GeoJSONFeature(
                        type="Feature",
                        id=str(item.get("id", "")),
                        geometry=feature_geom,
                        properties=properties,
                    )
                )
        except Exception:
            continue

    fc = GeoJSONFeatureCollection(
        type="FeatureCollection",
        features=intersected_features,
        metadata={
            "layer_id": layer_id,
            "total_intersected": len(intersected_features),
            "buffer_applied_meters": buffer_meters,
        },
    )

    return IntersectedLayerResult(
        layer_id=layer_id,
        intersected_count=len(intersected_features),
        feature_collection=fc,
    )
