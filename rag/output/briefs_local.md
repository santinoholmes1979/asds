# Local Readiness Briefs (Deterministic, SHAP-grounded)

## Commander Brief — AC_0034 — 2026-01-18
**Predicted downtime (next 14 days): 4.91 hrs** (baseline 6.13, delta -1.23) → **Risk: MODERATE**

### Key Drivers (Top 5)
- Environmental stress (current): ↓ -2.26 hrs
- Flight hours (current day): ↑ +1.17 hrs
- Environmental stress (current): ↓ -1.07 hrs
- Role: ISR: ↑ +0.92 hrs
- Mission intensity (current day): ↓ -0.90 hrs

### Operational Interpretation
- Primary upward pressure: **Flight hours (current day)**.
- Primary downward pressure: **Environmental stress (current)**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-18
Prediction: **4.91 hrs** (baseline 6.13, delta -1.23)

### Attributed Factors (ranked by |impact|)
- num__environment_stress → Environmental stress (current) : -2.26 hrs
- num__flight_hours → Flight hours (current day) : +1.17 hrs
- num__environment_stress_mean_7d → Environmental stress (current) : -1.07 hrs
- cat__role_ISR → Role: ISR : +0.92 hrs
- num__mission_intensity_mean_30d → Mission intensity (current day) : -0.90 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---

## Commander Brief — AC_0034 — 2026-01-19
**Predicted downtime (next 14 days): 17.57 hrs** (baseline 6.13, delta +11.44) → **Risk: ELEVATED**

### Key Drivers (Top 5)
- Flight hours (current day): ↑ +2.65 hrs
- Mission intensity (current day): ↑ +2.57 hrs
- Base-wide stockout rate: ↑ +1.91 hrs
- Base supply lead time (ETA pressure): ↓ -1.68 hrs
- Environmental stress (current): ↑ +1.37 hrs

### Operational Interpretation
- Primary upward pressure: **Flight hours (current day)**.
- Primary downward pressure: **Base supply lead time (ETA pressure)**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-19
Prediction: **17.57 hrs** (baseline 6.13, delta +11.44)

### Attributed Factors (ranked by |impact|)
- num__flight_hours → Flight hours (current day) : +2.65 hrs
- num__mission_intensity_mean_7d → Mission intensity (current day) : +2.57 hrs
- num__base_stockout_rate → Base-wide stockout rate : +1.91 hrs
- num__base_mean_eta → Base supply lead time (ETA pressure) : -1.68 hrs
- num__environment_stress_mean_30d → Environmental stress (current) : +1.37 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---

## Commander Brief — AC_0034 — 2026-01-20
**Predicted downtime (next 14 days): 9.85 hrs** (baseline 6.13, delta +3.72) → **Risk: ELEVATED**

### Key Drivers (Top 5)
- Base supply lead time (ETA pressure): ↑ +3.79 hrs
- Flight hours (current day): ↓ -3.09 hrs
- Mission intensity (current day): ↑ +2.17 hrs
- base BASE C: ↑ +1.11 hrs
- Environmental stress (current): ↓ -0.88 hrs

### Operational Interpretation
- Primary upward pressure: **Base supply lead time (ETA pressure)**.
- Primary downward pressure: **Flight hours (current day)**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-20
Prediction: **9.85 hrs** (baseline 6.13, delta +3.72)

### Attributed Factors (ranked by |impact|)
- num__base_mean_eta → Base supply lead time (ETA pressure) : +3.79 hrs
- num__flight_hours → Flight hours (current day) : -3.09 hrs
- num__mission_intensity_mean_7d → Mission intensity (current day) : +2.17 hrs
- cat__base_BASE_C → base BASE C : +1.11 hrs
- num__environment_stress → Environmental stress (current) : -0.88 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---

## Commander Brief — AC_0034 — 2026-01-21
**Predicted downtime (next 14 days): 19.52 hrs** (baseline 6.13, delta +13.39) → **Risk: ELEVATED**

### Key Drivers (Top 5)
- Mission intensity (current day): ↑ +2.69 hrs
- Flight hours (current day): ↑ +2.47 hrs
- Flight hours (current day): ↑ +1.95 hrs
- Environmental stress (current): ↑ +1.73 hrs
- Base supply lead time (ETA pressure): ↑ +1.64 hrs

### Operational Interpretation
- Primary upward pressure: **Mission intensity (current day)**.
- Primary downward pressure: **None**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-21
Prediction: **19.52 hrs** (baseline 6.13, delta +13.39)

### Attributed Factors (ranked by |impact|)
- num__mission_intensity → Mission intensity (current day) : +2.69 hrs
- num__flight_hours_sum_14d → Flight hours (current day) : +2.47 hrs
- num__flight_hours → Flight hours (current day) : +1.95 hrs
- num__environment_stress_mean_30d → Environmental stress (current) : +1.73 hrs
- num__base_mean_eta → Base supply lead time (ETA pressure) : +1.64 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---

## Commander Brief — AC_0034 — 2026-01-22
**Predicted downtime (next 14 days): 8.37 hrs** (baseline 6.13, delta +2.23) → **Risk: ELEVATED**

### Key Drivers (Top 5)
- Mission intensity (current day): ↓ -1.62 hrs
- Environmental stress (current): ↑ +1.61 hrs
- Base supply lead time (ETA pressure): ↓ -1.46 hrs
- Environmental stress (current): ↑ +1.39 hrs
- Base-wide stockout rate: ↑ +1.14 hrs

### Operational Interpretation
- Primary upward pressure: **Environmental stress (current)**.
- Primary downward pressure: **Mission intensity (current day)**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-22
Prediction: **8.37 hrs** (baseline 6.13, delta +2.23)

### Attributed Factors (ranked by |impact|)
- num__mission_intensity_mean_7d → Mission intensity (current day) : -1.62 hrs
- num__environment_stress_mean_7d → Environmental stress (current) : +1.61 hrs
- num__base_mean_eta → Base supply lead time (ETA pressure) : -1.46 hrs
- num__environment_stress_mean_30d → Environmental stress (current) : +1.39 hrs
- num__base_stockout_rate → Base-wide stockout rate : +1.14 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---

## Commander Brief — AC_0034 — 2026-01-23
**Predicted downtime (next 14 days): 3.97 hrs** (baseline 6.13, delta -2.17) → **Risk: MODERATE**

### Key Drivers (Top 5)
- Base-wide stockout rate: ↓ -2.65 hrs
- Environmental stress (current): ↑ +1.56 hrs
- Mission intensity (current day): ↓ -1.10 hrs
- Mission intensity (current day): ↓ -1.04 hrs
- Flight hours (current day): ↑ +0.83 hrs

### Operational Interpretation
- Primary upward pressure: **Environmental stress (current)**.
- Primary downward pressure: **Base-wide stockout rate**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-23
Prediction: **3.97 hrs** (baseline 6.13, delta -2.17)

### Attributed Factors (ranked by |impact|)
- num__base_stockout_rate → Base-wide stockout rate : -2.65 hrs
- num__environment_stress_mean_30d → Environmental stress (current) : +1.56 hrs
- num__mission_intensity → Mission intensity (current day) : -1.10 hrs
- num__mission_intensity_mean_7d → Mission intensity (current day) : -1.04 hrs
- num__flight_hours_sum_14d → Flight hours (current day) : +0.83 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---

## Commander Brief — AC_0034 — 2026-01-24
**Predicted downtime (next 14 days): 0.29 hrs** (baseline 6.13, delta -5.85) → **Risk: LOW**

### Key Drivers (Top 5)
- Flight hours (current day): ↓ -3.62 hrs
- Mission intensity (current day): ↓ -1.18 hrs
- Mission intensity (current day): ↓ -1.08 hrs
- Environmental stress (current): ↓ -0.81 hrs
- Base supply lead time (ETA pressure): ↑ +0.74 hrs

### Operational Interpretation
- Primary upward pressure: **Base supply lead time (ETA pressure)**.
- Primary downward pressure: **Flight hours (current day)**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-24
Prediction: **0.29 hrs** (baseline 6.13, delta -5.85)

### Attributed Factors (ranked by |impact|)
- num__flight_hours → Flight hours (current day) : -3.62 hrs
- num__mission_intensity → Mission intensity (current day) : -1.18 hrs
- num__mission_intensity_mean_7d → Mission intensity (current day) : -1.08 hrs
- num__environment_stress_mean_14d → Environmental stress (current) : -0.81 hrs
- num__base_mean_eta → Base supply lead time (ETA pressure) : +0.74 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---

## Commander Brief — AC_0034 — 2026-01-25
**Predicted downtime (next 14 days): 14.50 hrs** (baseline 6.13, delta +8.36) → **Risk: ELEVATED**

### Key Drivers (Top 5)
- Environmental stress (current): ↑ +4.19 hrs
- Base supply lead time (ETA pressure): ↓ -1.89 hrs
- Environmental stress (current): ↓ -1.80 hrs
- Flight hours (current day): ↑ +1.67 hrs
- Base-wide stockout rate: ↑ +1.56 hrs

### Operational Interpretation
- Primary upward pressure: **Environmental stress (current)**.
- Primary downward pressure: **Base supply lead time (ETA pressure)**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-25
Prediction: **14.50 hrs** (baseline 6.13, delta +8.36)

### Attributed Factors (ranked by |impact|)
- num__environment_stress → Environmental stress (current) : +4.19 hrs
- num__base_mean_eta → Base supply lead time (ETA pressure) : -1.89 hrs
- num__environment_stress_mean_14d → Environmental stress (current) : -1.80 hrs
- num__flight_hours_sum_14d → Flight hours (current day) : +1.67 hrs
- num__base_stockout_rate → Base-wide stockout rate : +1.56 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---

## Commander Brief — AC_0034 — 2026-01-26
**Predicted downtime (next 14 days): 4.10 hrs** (baseline 6.13, delta -2.04) → **Risk: MODERATE**

### Key Drivers (Top 5)
- Base supply lead time (ETA pressure): ↓ -2.23 hrs
- Environmental stress (current): ↓ -2.06 hrs
- Environmental stress (current): ↑ +1.25 hrs
- Flight hours (current day): ↓ -0.88 hrs
- Mission intensity (current day): ↑ +0.86 hrs

### Operational Interpretation
- Primary upward pressure: **Environmental stress (current)**.
- Primary downward pressure: **Base supply lead time (ETA pressure)**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-26
Prediction: **4.10 hrs** (baseline 6.13, delta -2.04)

### Attributed Factors (ranked by |impact|)
- num__base_mean_eta → Base supply lead time (ETA pressure) : -2.23 hrs
- num__environment_stress → Environmental stress (current) : -2.06 hrs
- num__environment_stress_mean_30d → Environmental stress (current) : +1.25 hrs
- num__flight_hours_sum_30d → Flight hours (current day) : -0.88 hrs
- num__mission_intensity_mean_7d → Mission intensity (current day) : +0.86 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---

## Commander Brief — AC_0034 — 2026-01-27
**Predicted downtime (next 14 days): 12.13 hrs** (baseline 6.13, delta +5.99) → **Risk: ELEVATED**

### Key Drivers (Top 5)
- Base supply lead time (ETA pressure): ↑ +5.37 hrs
- Base-wide stockout rate: ↓ -1.19 hrs
- Flight hours (current day): ↑ +1.03 hrs
- Mission intensity (current day): ↓ -0.96 hrs
- Role: ISR: ↑ +0.95 hrs

### Operational Interpretation
- Primary upward pressure: **Base supply lead time (ETA pressure)**.
- Primary downward pressure: **Base-wide stockout rate**.
- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.

### Confidence / Limitations
- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.

## Engineer Brief — AC_0034 — 2026-01-27
Prediction: **12.13 hrs** (baseline 6.13, delta +5.99)

### Attributed Factors (ranked by |impact|)
- num__base_mean_eta → Base supply lead time (ETA pressure) : +5.37 hrs
- num__base_stockout_rate → Base-wide stockout rate : -1.19 hrs
- num__flight_hours → Flight hours (current day) : +1.03 hrs
- num__mission_intensity_mean_30d → Mission intensity (current day) : -0.96 hrs
- cat__role_ISR → Role: ISR : +0.95 hrs

### Engineering Notes
- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.
- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.

### Data/Model Notes
- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.

---
