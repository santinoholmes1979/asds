import os
import json
import ast
import pandas as pd

# Map feature tokens to human meanings (you can expand this over time)
FEATURE_GLOSSARY = [
    ("num__base_mean_eta", "Base supply lead time (ETA pressure)"),
    ("num__base_stockout_rate", "Base-wide stockout rate"),
    ("stockouts", "Stockouts tied to recent failures"),
    ("eta_days", "ETA delay tied to recent failures"),
    ("num__environment_stress", "Environmental stress (current)"),
    ("environment_stress_mean_7d", "Environmental stress (7-day avg)"),
    ("environment_stress_mean_14d", "Environmental stress (14-day avg)"),
    ("environment_stress_mean_30d", "Environmental stress (30-day avg)"),
    ("num__flight_hours", "Flight hours (current day)"),
    ("flight_hours_sum_7d", "Flight hours (7-day total)"),
    ("flight_hours_sum_14d", "Flight hours (14-day total)"),
    ("flight_hours_sum_30d", "Flight hours (30-day total)"),
    ("num__mission_intensity", "Mission intensity (current day)"),
    ("mission_intensity_mean_7d", "Mission intensity (7-day avg)"),
    ("mission_intensity_mean_14d", "Mission intensity (14-day avg)"),
    ("mission_intensity_mean_30d", "Mission intensity (30-day avg)"),
    ("failures_count_sum_7d", "Recent failures (7-day count)"),
    ("failures_count_sum_14d", "Recent failures (14-day count)"),
    ("down_hours_sum_14d", "Recent downtime (14-day total)"),
    ("wait_parts_hours_sum_14d", "Recent waiting on parts (14-day total)"),
    ("wait_maint_hours_sum_14d", "Recent waiting on maintainers (14-day total)"),
    ("repair_hours_sum_14d", "Recent repair time (14-day total)"),
]

ROLE_TOKENS = {
    "cat__role_ISR": "Role: ISR",
    "cat__role_STRIKE": "Role: Strike",
    "cat__role_TRAIN": "Role: Training",
}

def humanize_feature(feat: str) -> str:
    if feat in ROLE_TOKENS:
        return ROLE_TOKENS[feat]
    for needle, meaning in FEATURE_GLOSSARY:
        if needle in feat:
            return meaning
    # Default fallback: strip sklearn prefixes
    return feat.replace("num__", "").replace("cat__", "").replace("_", " ")

def format_driver(feature: str, impact: float) -> str:
    direction = "↑" if impact > 0 else "↓"
    sign = "+" if impact > 0 else ""
    return f"- {humanize_feature(feature)}: {direction} {sign}{impact:.2f} hrs"

def summarize_drivers(drivers):
    inc = [d for d in drivers if d["impact_hours"] > 0]
    dec = [d for d in drivers if d["impact_hours"] < 0]
    inc_sorted = sorted(inc, key=lambda x: abs(x["impact_hours"]), reverse=True)
    dec_sorted = sorted(dec, key=lambda x: abs(x["impact_hours"]), reverse=True)
    return inc_sorted, dec_sorted

def commander_brief(payload: dict) -> str:
    pred = payload["prediction"]["downtime_next_14d_hours"]
    base = payload["prediction"]["baseline_hours"]
    delta = pred - base

    inc, dec = summarize_drivers(payload["drivers"])

    # Summary language
    if pred < 2:
        risk = "LOW"
    elif pred < 8:
        risk = "MODERATE"
    else:
        risk = "ELEVATED"

    main_up = inc[0]["meaning"] if inc else "None"
    main_down = dec[0]["meaning"] if dec else "None"

    lines = []
    lines.append(f"## Commander Brief — {payload['aircraft_id']} — {payload['date']}")
    lines.append(f"**Predicted downtime (next 14 days): {pred:.2f} hrs** (baseline {base:.2f}, delta {delta:+.2f}) → **Risk: {risk}**")
    lines.append("")
    lines.append("### Key Drivers (Top 5)")
    for d in payload["drivers"][:5]:
        lines.append(format_driver(d["feature"], d["impact_hours"]))
    lines.append("")
    lines.append("### Operational Interpretation")
    lines.append(f"- Primary upward pressure: **{main_up}**.")
    lines.append(f"- Primary downward pressure: **{main_down}**.")
    lines.append("- Recommended focus: prioritize actions that reduce logistics/lead-time delays and monitor operating conditions/tempo drivers.")
    lines.append("")
    lines.append("### Confidence / Limitations")
    lines.append("- Synthetic dataset; directional insights only. Explanations are SHAP-based and tied to model inputs.")
    return "\n".join(lines)

def engineer_brief(payload: dict) -> str:
    pred = payload["prediction"]["downtime_next_14d_hours"]
    base = payload["prediction"]["baseline_hours"]
    delta = pred - base

    inc, dec = summarize_drivers(payload["drivers"])

    lines = []
    lines.append(f"## Engineer Brief — {payload['aircraft_id']} — {payload['date']}")
    lines.append(f"Prediction: **{pred:.2f} hrs** (baseline {base:.2f}, delta {delta:+.2f})")
    lines.append("")
    lines.append("### Attributed Factors (ranked by |impact|)")
    ranked = sorted(payload["drivers"], key=lambda x: abs(x["impact_hours"]), reverse=True)
    for d in ranked[:5]:
        lines.append(f"- {d['feature']} → {d['meaning']} : {d['impact_hours']:+.2f} hrs")
    lines.append("")
    lines.append("### Engineering Notes")
    lines.append("- If logistics features dominate (ETA/stockout), explore: supplier lead time drivers, reorder points, safety stock, expedite policies.")
    lines.append("- If stress/tempo dominates, explore: operating envelope effects, usage patterns, preventive maintenance triggers.")
    lines.append("")
    lines.append("### Data/Model Notes")
    lines.append("- Contributions are local explanations for this sample point; validate across fleet-level SHAP aggregates before taking action.")
    return "\n".join(lines)

def main():
    src = "models/explanations/shap_summary_sample.csv"
    df = pd.read_csv(src)

    os.makedirs("rag/output", exist_ok=True)

    # Make multiple briefs (top N rows)
    N = 10
    briefs = []
    md_parts = ["# Local Readiness Briefs (Deterministic, SHAP-grounded)\n"]

    for i in range(min(N, len(df))):
        row = df.iloc[i]

        drivers_raw = ast.literal_eval(row["top_5_drivers"])
        drivers = []
        for feat, impact in drivers_raw:
            drivers.append({
                "feature": feat,
                "meaning": humanize_feature(feat),
                "impact_hours": float(impact),
            })

        payload = {
            "date": row["date"],
            "aircraft_id": row["aircraft_id"],
            "y_true": float(row["y_true"]),
            "prediction": {
                "downtime_next_14d_hours": float(row["y_pred"]),
                "baseline_hours": float(row["base_value"]),
            },
            "drivers": drivers,
        }

        briefs.append(payload)
        md_parts.append(commander_brief(payload))
        md_parts.append("")
        md_parts.append(engineer_brief(payload))
        md_parts.append("\n---\n")

    with open("rag/output/briefs_local.json", "w", encoding="utf-8") as f:
        json.dump(briefs, f, indent=2)

    with open("rag/output/briefs_local.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_parts))

    print("✅ Wrote:")
    print(" - rag/output/briefs_local.json")
    print(" - rag/output/briefs_local.md")
    print(f"Generated briefs for {min(N, len(df))} samples from {src}")

if __name__ == "__main__":
    main()
