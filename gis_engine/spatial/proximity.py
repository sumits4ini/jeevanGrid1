"""
Proximity Search and Spatial Distance Utilities
"""

from typing import Any, Dict, List, Optional
from gis_engine.geometry.transforms import calculate_haversine_distance_m
from gis_engine.schemas.layer import NearbyFeatureItem


def filter_and_rank_nearby_features(
    features: List[Dict[str, Any]],
    center_lng: float,
    center_lat: float,
    radius_meters: float,
    limit: int = 50,
) -> List[NearbyFeatureItem]:
    """
    Ranks features by great-circle distance from (center_lng, center_lat) within radius_meters.
    Features must have 'id', 'name', 'latitude', 'longitude' (or geometry coordinates).
    """
    results: List[NearbyFeatureItem] = []

    for f in features:
        lng = f.get("longitude")
        lat = f.get("latitude")

        # Extract coordinates from geometry if not top-level
        if (lng is None or lat is None) and "geometry" in f:
            geom = f["geometry"]
            if isinstance(geom, dict) and geom.get("type") == "Point":
                coords = geom.get("coordinates", [])
                if len(coords) >= 2:
                    lng, lat = coords[0], coords[1]

        if lng is None or lat is None:
            continue

        dist_m = calculate_haversine_distance_m(center_lng, center_lat, float(lng), float(lat))
        if dist_m <= radius_meters:
            results.append(
                NearbyFeatureItem(
                    id=str(f.get("id", "")),
                    layer_id=str(f.get("layer_id", "default")),
                    name=str(f.get("name", "Unnamed Feature")),
                    distance_meters=round(dist_m, 2),
                    latitude=float(lat),
                    longitude=float(lng),
                    properties=f.get("properties", {}),
                )
            )

    # Sort ascending by distance
    results.sort(key=lambda item: item.distance_meters)
    return results[:limit]
