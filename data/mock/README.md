# Mock and Simulation Datasets (Data Integrity & Provenance)

## 1. Data Integrity Principle
In accordance with strict scientific and engineering standards:
- **Never fabricate real disaster data and present it as genuine live telemetry.**
- All datasets located in this directory (`data/mock/`) are **explicitly synthetic or historical scenario simulations** designed for offline testing, developer onboarding, and fail-safe demonstrations.
- Real-world production integrations (e.g. IMD, CWC, GDACS, USGS, OpenStreetMap Overpass) are maintained separately in `backend/app/services/ingestion/adapters/`.

---

## 2. Standard Metadata Schema
Every mock/simulation dataset committed to this repository must include a companion `.meta.json` file with the following attributes:

```json
{
  "dataset_id": "mock_assam_barpeta_flood_2026",
  "title": "Assam Barpeta District Flash Flood Scenario 2026",
  "data_type": "SIMULATED_SCENARIO",
  "geographical_scope": {
    "district": "Barpeta",
    "state": "Assam",
    "country": "India",
    "bounding_box": [90.85, 26.15, 91.25, 26.50]
  },
  "created_at": "2026-08-16T20:00:00Z",
  "source_and_provenance": "Synthetic dataset calibrated against historical Brahmaputra flood levels (CWC/ISRO Bhuvan historical flood atlas 2020-2024)",
  "licensing": "CC-BY-4.0 / Open Data Commons",
  "features_included": [
    "inundation_polygons",
    "critical_infrastructure_points",
    "h3_vulnerability_hexgrid",
    "response_unit_telemetry",
    "road_network_severance_points"
  ]
}
```

---

## 3. Included Demo Scenarios
1. `assam_brahmaputra_flood_2026`: Multi-ward riverine flood scenario with hospital cutoff and bridge inundation.
2. `chennai_cyclone_inundation_2026`: Urban storm surge and power substation failure scenario.
3. `wayanad_landslide_blockage_2026`: Hilly terrain road severance and rescue boat/drone dispatch scenario.
