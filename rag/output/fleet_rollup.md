# Fleet Readiness Rollup (SHAP-grounded, offline)

## Executive Summary (Stoplight)
**Fleet Status:** AMBER
- Localized or emerging readiness risk; monitor and mitigate.
- Reporting window: 2026-01-31 to 2026-02-06
- Aircraft evaluated: 7
- Predicted downtime (14d): Avg 5.78 hrs | P80 7.50 hrs
- Risk distribution: LOW=1  MODERATE=5  ELEVATED=1

**Reporting window:** 2026-01-31 to 2026-02-06
**Aircraft evaluated (sample):** 7
**Avg predicted downtime (14d):** 5.78 hrs  |  **P80:** 7.50 hrs
**Risk distribution:** LOW=1  MODERATE=5  ELEVATED=1

## Commander Summary
- Readiness risk is **concentrated** in a subset of aircraft with elevated predicted downtime.
- Primary fleet drivers below are derived from **mean absolute SHAP impact** across the window (model-grounded).
- Use base rollups to prioritize logistics/maintenance attention where downtime risk clusters.

## Top 10 Aircraft by Predicted Downtime (latest in window)
| Rank | Aircraft | Date | Base | Unit | Role | Status | Pred 14d downtime (hrs) | Risk |
|---:|---|---|---|---|---|---|---:|---|
| 1 | AC_0036 | 2026-02-06 | BASE_B | UNIT_02 | TRAIN | FMC | 10.87 | ELEVATED |
| 2 | AC_0034 | 2026-02-06 | BASE_B | UNIT_04 | ISR | FMC | 7.58 | MODERATE |
| 3 | AC_0038 | 2026-02-06 | BASE_B | UNIT_04 | TRAIN | PMC | 7.21 | MODERATE |
| 4 | AC_0037 | 2026-02-06 | BASE_B | UNIT_03 | STRIKE | FMC | 6.60 | MODERATE |
| 5 | AC_0035 | 2026-02-06 | BASE_C | UNIT_01 | TRAIN | FMC | 4.44 | MODERATE |
| 6 | AC_0039 | 2026-02-06 | BASE_A | UNIT_03 | STRIKE | FMC | 2.53 | MODERATE |
| 7 | AC_0040 | 2026-02-06 | BASE_A | UNIT_01 | TRAIN | PMC | 1.21 | LOW |

## Base-Level Rollup (latest per aircraft)
| Base | Aircraft | Avg Pred 14d (hrs) | P80 (hrs) | Elevated | Moderate |
|---|---:|---:|---:|---:|---:|
| BASE_B | 4 | 8.06 | 8.89 | 1 | 3 |
| BASE_C | 1 | 4.44 | 4.44 | 0 | 1 |
| BASE_A | 2 | 1.87 | 2.27 | 0 | 1 |

## Fleet-Wide Top Drivers (mean |SHAP| impact in hours)
| Rank | Feature | Mean |SHAP| impact (hrs) |
|---:|---|---:|
| 1 | num__base_mean_eta | 1.734 |
| 2 | num__flight_hours_sum_30d | 1.220 |
| 3 | num__environment_stress | 1.134 |
| 4 | num__base_stockout_rate | 1.041 |
| 5 | num__flight_hours | 0.890 |
| 6 | num__mission_intensity | 0.783 |
| 7 | num__mission_intensity_mean_7d | 0.710 |
| 8 | num__mission_intensity_mean_30d | 0.635 |
| 9 | num__environment_stress_mean_7d | 0.565 |
| 10 | num__environment_stress_mean_14d | 0.561 |

## Common Local Drivers in Top-10 Risk Aircraft (counts)
| Feature | Count in Top-10 Aircraft |
|---|---:|
| num__base_mean_eta | 6 |
| num__flight_hours_sum_30d | 4 |
| num__flight_hours | 4 |
| num__environment_stress | 3 |
| num__environment_stress_mean_7d | 3 |
| num__mission_intensity_mean_7d | 2 |
| num__mission_intensity_mean_30d | 2 |
| num__flight_hours_sum_14d | 2 |
| num__mission_intensity | 2 |
| cat__base_BASE_A | 1 |

## Recommended Actions (SHAP-grounded)
- **Logistics / Supply Chain:** Prioritize review of part lead times and reorder points at bases with elevated predicted downtime. Consider expediting high-criticality parts contributing to downtime risk.
- **Operations:** Evaluate near-term flight schedules for high-risk aircraft. Where feasible, redistribute sortie load to reduce concentrated wear drivers.
- **Basing / Operating Conditions:** Monitor environmental stress exposure for affected aircraft. Adjust basing, sheltering, or inspection cadence if elevated conditions persist.

## Confidence / Limitations
- This is a **synthetic demonstration dataset**; results are directional and not operationally authoritative.
- Recommendations are **rule-based translations of SHAP drivers**, not automated decisions.
- Human review is required before any operational or sustainment action.
