# 03. AI/ML, Risk Analysis, and Resource Optimization Engine

## 1. Multi-Criteria Risk & Vulnerability Index (MCDA)

JeevanGrid implements the internationally recognized **UNDRR (United Nations Office for Disaster Risk Reduction)** disaster risk formulation:

$$\text{Risk} = \frac{\text{Hazard (H)} \times \text{Exposure (E)} \times \text{Vulnerability (V)}}{\text{Coping Capacity (C)}}$$

### Component Calculations (Normalized 0.0 to 1.0)
1. **Hazard Intensity ($H$)**:
   - Inundation Depth / Flood Height ($w_1 = 0.4$)
   - Rainfall Intensity / Rate (mm/hr) ($w_2 = 0.3$)
   - Rate of Water Level Rise (cm/hr) ($w_3 = 0.3$)
2. **Exposure ($E$)**:
   - Absolute Population Density within H3 Cell ($w_1 = 0.5$)
   - Critical Infrastructure Asset Count (Hospitals, Power, Water) ($w_2 = 0.5$)
3. **Vulnerability ($V$)**:
   - Demographic Vulnerability (% Elderly $>65$, Children $<5$, Differently Abled) ($w_1 = 0.4$)
   - Structural Vulnerability (% Kutcha / non-reinforced housing) ($w_2 = 0.3$)
   - Elevation Slope Factor (Low-lying depression index) ($w_3 = 0.3$)
4. **Coping Capacity ($C$)**:
   - Distance to Nearest Operating Hospital / Trauma Center ($w_1 = 0.3$)
   - Road Connectivity & Evacuation Corridor Density ($w_2 = 0.4$)
   - Pre-positioned NDRF / SDRF Asset Proximity ($w_3 = 0.3$)

**Output**: Composite Risk Score categorized into 4 operational tiers:
- **0.00 - 0.25**: Low (Monitor)
- **0.25 - 0.50**: Moderate (Advisory / Standby)
- **0.50 - 0.75**: High (Pre-evacuate / Resource Pre-position)
- **0.75 - 1.00**: Critical (Immediate Emergency Rescue Dispatch)

---

## 2. Machine Learning Model Suite

```text
Model Name          Type                     Input Features                                   Target Output              Baseline Metric
-----------------------------------------------------------------------------------------------------------------------------------------
1. SeverityPred     LightGBM Classifier      Rainfall(24h/48h), River Stage, Soil Moisture,  Severity Class (1 to 5)    F1-Score > 0.88
                                             Elevation, Upstream Discharge
2. DemandForecast   Multi-Output Ridge/XGB   Affected Pop, Risk Tier, Displacement %,        Required: [Boats,          RMSE < 12% 
                                             Hospital Outages, Shelter Capacity              Ambulances, Food, Water]   of demand
3. DistressTriage   NLP Classifier           Distress Message Text, GPS Accuracy, Urgency    Triage Priority            Accuracy > 91%
                    (DistilBERT / TF-IDF)    Keywords (Trapped, Medical, Children, Food)     (P1-Life Threat to P4-Info)
```

### Model Governance & Integrity Rule
- **No Hallucinated Predictions**: All ML models output prediction intervals / confidence bands.
- If model confidence is $< 0.70$, the system automatically relies on deterministic PostGIS MCDA rule baselines and marks the recommendation with `Confidence: Low - Rule-Based Fallback Engaged`.

---

## 3. Resource Allocation & Dispatch Optimizer (MILP)

When multiple disaster zones demand limited rescue assets, manual allocation causes severe delays and misallocation. JeevanGrid formulates resource dispatch as a **Mixed-Integer Linear Program (MILP)** solved using `PuLP` / `SciPy`:

### Objective Function: Maximize Total Life-Saving Utility
$$\max \sum_{i \in \text{Demands}} \sum_{j \in \text{Depots}} \sum_{k \in \text{Vehicles}} \left( \text{PriorityScore}_i \times \text{MatchedSupply}_{ijk} - \lambda \times \text{TravelTime}_{ij} \times X_{ijk} \right)$$

### Subject to Constraints:
1. **Supply Capacity**: Dispatched assets from depot $j$ cannot exceed available stock.
2. **Demand Cap**: Allocated resources to zone $i$ cannot exceed the ceiling required to stabilize zone $i$.
3. **Vehicle Reachability**: Binary decision variable $X_{ijk} = 0$ if path from depot $j$ to zone $i$ is impassable.
4. **Time Horizon**: Total round-trip travel time cannot exceed the maximum operational shift duration.
