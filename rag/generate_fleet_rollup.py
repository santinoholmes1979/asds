import os
import json
import ast
import pandas as pd
import numpy as np


def safe_read_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path)


def to_dt(s):
    return pd.to_datetime(s, errors="coerce")


def classify_risk(hours: float) -> str:
    if hours < 2:
        return "LOW"
    if hours < 8:
        return "MODERATE"
    return "ELEVATED"

def fleet_stoplight(fleet_metrics: dict):
    elevated = fleet_metrics["risk_counts"]["ELEVATED"]
    p80 = fleet_metrics["p80_pred_14d_hours"]

    if elevated > 0 and p80 >= 10:
        return "RED", "Immediate readiness risk requiring senior leader attention."
    if elevated > 0 or p80 >= 6:
        return "AMBER", "Localized or emerging readiness risk; monitor and mitigate."
    return "GREEN", "Fleet readiness stable within expected operating limits."


def main():
    # Inputs
    shap_summary_path = "models/explanations/shap_summary_sample.csv"
    shap_values_path = "models/explanations/shap_values_sample.csv"
    train_path = "data/training_table_with_inventory.csv" if os.path.exists("data/training_table_with_inventory.csv") else "data/training_table.csv"

    summ = safe_read_csv(shap_summary_path)
    shapv = safe_read_csv(shap_values_path)
    train = safe_read_csv(train_path)

    # Normalize dates
    summ["date"] = to_dt(summ["date"])
    shapv["date"] = to_dt(shapv["date"])
    train["date"] = to_dt(train["date"])

    # Map aircraft-day -> base/unit/role for context
    meta = train[["date", "aircraft_id", "base", "unit_id", "role", "status_start"]].drop_duplicates()
    summ = summ.merge(meta, on=["date", "aircraft_id"], how="left")

    # Define "reporting window" as last 7 days present in SHAP sample
    max_date = summ["date"].max()
    window_start = max_date - pd.Timedelta(days=6)
    window = summ[(summ["date"] >= window_start) & (summ["date"] <= max_date)].copy()

    # Latest prediction per aircraft within window
    window = window.sort_values(["aircraft_id", "date"])
    latest = window.groupby("aircraft_id", as_index=False).tail(1).copy()

    latest["risk"] = latest["y_pred"].apply(classify_risk)

    # Top risk aircraft (latest)
    top_aircraft = (
        latest.sort_values("y_pred", ascending=False)
        .head(10)[["aircraft_id", "date", "base", "unit_id", "role", "status_start", "y_pred", "risk", "top_5_drivers"]]
        .copy()
    )

    # Base-level rollup (using latest per aircraft)
    base_rollup = (
        latest.groupby("base", as_index=False)
        .agg(
            aircraft_count=("aircraft_id", "nunique"),
            avg_pred_14d_hours=("y_pred", "mean"),
            p80_pred_14d_hours=("y_pred", lambda x: float(np.quantile(x, 0.80))),
            elevated_count=("risk", lambda x: int((x == "ELEVATED").sum())),
            moderate_count=("risk", lambda x: int((x == "MODERATE").sum())),
        )
        .sort_values("avg_pred_14d_hours", ascending=False)
    )

    # Fleet-wide top drivers using full SHAP matrix (mean absolute contribution)
    # shap_values_sample.csv columns: date, aircraft_id, y_pred, then SHAP feature columns
    shap_feature_cols = [c for c in shapv.columns if c not in ["date", "aircraft_id", "y_pred"]]
    shap_window = shapv[(shapv["date"] >= window_start) & (shapv["date"] <= max_date)].copy()

    mean_abs = shap_window[shap_feature_cols].abs().mean().sort_values(ascending=False).head(10)
    top_drivers_fleet = [{"feature": k, "mean_abs_impact_hours": float(v)} for k, v in mean_abs.items()]

    # Also extract most common local drivers from top-risk aircraft (interpretable “reasons”)
    def extract_driver_names(x):
        try:
            drivers = ast.literal_eval(x)
            return [d[0] for d in drivers]
        except Exception:
            return []

    driver_counts = {}
    for s in top_aircraft["top_5_drivers"].tolist():
        for name in extract_driver_names(s):
            driver_counts[name] = driver_counts.get(name, 0) + 1

    common_local = sorted(driver_counts.items(), key=lambda kv: kv[1], reverse=True)[:10]
    common_local = [{"feature": k, "count_in_top10_aircraft": int(v)} for k, v in common_local]

    # Fleet summary metrics
    fleet_metrics = {
        "window_start": str(window_start.date()),
        "window_end": str(max_date.date()),
        "aircraft_in_sample": int(latest["aircraft_id"].nunique()),
        "avg_pred_14d_hours": float(latest["y_pred"].mean()),
        "p80_pred_14d_hours": float(np.quantile(latest["y_pred"], 0.80)),
        "risk_counts": {
            "LOW": int((latest["risk"] == "LOW").sum()),
            "MODERATE": int((latest["risk"] == "MODERATE").sum()),
            "ELEVATED": int((latest["risk"] == "ELEVATED").sum()),
        },
    }

    stoplight, stoplight_text = fleet_stoplight(fleet_metrics)
    fleet_metrics["stoplight"] = stoplight
    fleet_metrics["stoplight_summary"] = stoplight_text

    # Build markdown brief (commander-friendly)
    md = []
    md.append("# Fleet Readiness Rollup (SHAP-grounded, offline)\n")
    md.append("## Executive Summary (Stoplight)")
    md.append(f"**Fleet Status:** {fleet_metrics['stoplight']}")
    md.append(f"- {fleet_metrics['stoplight_summary']}")
    md.append(f"- Reporting window: {fleet_metrics['window_start']} to {fleet_metrics['window_end']}")
    md.append(f"- Aircraft evaluated: {fleet_metrics['aircraft_in_sample']}")
    md.append(
        f"- Predicted downtime (14d): Avg {fleet_metrics['avg_pred_14d_hours']:.2f} hrs | "
        f"P80 {fleet_metrics['p80_pred_14d_hours']:.2f} hrs"
    )
    md.append(
        f"- Risk distribution: LOW={fleet_metrics['risk_counts']['LOW']}  "
        f"MODERATE={fleet_metrics['risk_counts']['MODERATE']}  "
        f"ELEVATED={fleet_metrics['risk_counts']['ELEVATED']}\n"
    )

    md.append(f"**Reporting window:** {fleet_metrics['window_start']} to {fleet_metrics['window_end']}")
    md.append(f"**Aircraft evaluated (sample):** {fleet_metrics['aircraft_in_sample']}")
    md.append(f"**Avg predicted downtime (14d):** {fleet_metrics['avg_pred_14d_hours']:.2f} hrs  |  **P80:** {fleet_metrics['p80_pred_14d_hours']:.2f} hrs")
    md.append(f"**Risk distribution:** LOW={fleet_metrics['risk_counts']['LOW']}  MODERATE={fleet_metrics['risk_counts']['MODERATE']}  ELEVATED={fleet_metrics['risk_counts']['ELEVATED']}\n")

    md.append("## Commander Summary")
    if fleet_metrics["risk_counts"]["ELEVATED"] > 0:
        md.append("- Readiness risk is **concentrated** in a subset of aircraft with elevated predicted downtime.")
    else:
        md.append("- No aircraft in the sample window are classified as **ELEVATED**; risk is primarily **LOW–MODERATE**.")
    md.append("- Primary fleet drivers below are derived from **mean absolute SHAP impact** across the window (model-grounded).")
    md.append("- Use base rollups to prioritize logistics/maintenance attention where downtime risk clusters.\n")

    md.append("## Top 10 Aircraft by Predicted Downtime (latest in window)")
    md.append("| Rank | Aircraft | Date | Base | Unit | Role | Status | Pred 14d downtime (hrs) | Risk |")
    md.append("|---:|---|---|---|---|---|---|---:|---|")
    for i, r in enumerate(top_aircraft.itertuples(index=False), start=1):
        md.append(f"| {i} | {r.aircraft_id} | {str(r.date.date())} | {r.base} | {r.unit_id} | {r.role} | {r.status_start} | {float(r.y_pred):.2f} | {r.risk} |")
    md.append("")

    md.append("## Base-Level Rollup (latest per aircraft)")
    md.append("| Base | Aircraft | Avg Pred 14d (hrs) | P80 (hrs) | Elevated | Moderate |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for r in base_rollup.itertuples(index=False):
        md.append(f"| {r.base} | {int(r.aircraft_count)} | {float(r.avg_pred_14d_hours):.2f} | {float(r.p80_pred_14d_hours):.2f} | {int(r.elevated_count)} | {int(r.moderate_count)} |")
    md.append("")

    md.append("## Fleet-Wide Top Drivers (mean |SHAP| impact in hours)")
    md.append("| Rank | Feature | Mean |SHAP| impact (hrs) |")
    md.append("|---:|---|---:|")
    for i, d in enumerate(top_drivers_fleet, start=1):
        md.append(f"| {i} | {d['feature']} | {d['mean_abs_impact_hours']:.3f} |")
    md.append("")

    md.append("## Common Local Drivers in Top-10 Risk Aircraft (counts)")
    md.append("| Feature | Count in Top-10 Aircraft |")
    md.append("|---|---:|")
    for d in common_local:
        md.append(f"| {d['feature']} | {d['count_in_top10_aircraft']} |")
    md.append("")

        # --- Recommended Actions (rule-based, SHAP-grounded) ---
    md.append("## Recommended Actions (SHAP-grounded)")

    driver_names = [d["feature"] for d in top_drivers_fleet]
    actions = []

    # Logistics / supply-chain driven
    if any(k in name.lower() for name in driver_names for k in ["eta", "stock", "inventory", "on_hand", "on_order"]):
        actions.append(
            "- **Logistics / Supply Chain:** Prioritize review of part lead times and reorder points at bases with elevated predicted downtime. "
            "Consider expediting high-criticality parts contributing to downtime risk."
        )

    # Operations / tempo driven
    if any(k in name.lower() for name in driver_names for k in ["flight_hours", "mission_intensity"]):
        actions.append(
            "- **Operations:** Evaluate near-term flight schedules for high-risk aircraft. "
            "Where feasible, redistribute sortie load to reduce concentrated wear drivers."
        )

    # Environmental stress driven
    if any("environment" in name.lower() for name in driver_names):
        actions.append(
            "- **Basing / Operating Conditions:** Monitor environmental stress exposure for affected aircraft. "
            "Adjust basing, sheltering, or inspection cadence if elevated conditions persist."
        )

    # Maintenance capacity driven
    if any(k in name.lower() for name in driver_names for k in ["wait_maint", "repair_hours", "failures"]):
        actions.append(
            "- **Maintenance:** Review maintenance manning and shift coverage at bases with elevated risk. "
            "Align staffing and spares to reduce wait-for-maintenance and repair delays."
        )

    if not actions:
        actions.append(
            "- **General:** Continue monitoring fleet drivers; no dominant corrective action identified in this window."
        )

    for a in actions:
        md.append(a)

    md.append("")

    # Confidence / limitations
    md.append("## Confidence / Limitations")
    md.append("- This is a **synthetic demonstration dataset**; results are directional and not operationally authoritative.")
    md.append("- Recommendations are **rule-based translations of SHAP drivers**, not automated decisions.")
    md.append("- Human review is required before any operational or sustainment action.\n")


    # Write outputs
    os.makedirs("rag/output", exist_ok=True)
    md_path = "rag/output/fleet_rollup.md"
    json_path = "rag/output/fleet_rollup.json"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    payload = {
        "fleet_metrics": fleet_metrics,
        "top_aircraft": top_aircraft.to_dict(orient="records"),
        "base_rollup": base_rollup.to_dict(orient="records"),
        "fleet_top_drivers_mean_abs_shap": top_drivers_fleet,
        "common_local_driver_counts_top10": common_local,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    print("✅ Wrote:")
    print(f" - {md_path}")
    print(f" - {json_path}")


if __name__ == "__main__":
    main()
