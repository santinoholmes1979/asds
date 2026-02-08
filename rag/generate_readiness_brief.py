import json
import pandas as pd

TEMPLATE_COMMANDER = """
You are a defense readiness analyst.

Using ONLY the structured inputs below, generate a concise commander-ready readiness brief.
Do NOT introduce new facts.
Do NOT speculate beyond the provided drivers.

STRUCTURED INPUT:
{payload}

OUTPUT FORMAT:
- Summary (2–3 sentences)
- Key Drivers (bullet list with +/- hours)
- Operational Interpretation (1–2 sentences)
- Confidence / Limitations (1 sentence)
"""

def main():
    # Load one SHAP summary row
    df = pd.read_csv("models/explanations/shap_summary_sample.csv")
    row = df.iloc[0]

    payload = {
        "aircraft_id": row["aircraft_id"],
        "date": row["date"],
        "prediction": {
            "downtime_next_14d_hours": round(float(row["y_pred"]), 2),
            "baseline_hours": round(float(row["base_value"]), 2),
        },
        "top_drivers": eval(row["top_5_drivers"]),  # safe here (synthetic + local)
        "confidence_notes": [
            "Synthetic data",
            "14-day prediction horizon",
            "Explainable via SHAP"
        ]
    }

    print("=== STRUCTURED PAYLOAD ===")
    print(json.dumps(payload, indent=2))

    print("\n=== PROMPT (to GenAI) ===")
    print(TEMPLATE_COMMANDER.format(payload=json.dumps(payload, indent=2)))

if __name__ == "__main__":
    main()
