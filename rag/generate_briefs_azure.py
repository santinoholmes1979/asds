import os
import json
import ast
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not ENDPOINT or not API_KEY or not DEPLOYMENT:
    raise RuntimeError("Missing AZURE_OPENAI_* env vars. Fill in .env then rerun.")


def humanize_driver_list(drivers):
    # drivers: list of dicts {feature, meaning, impact_hours}
    # Keep it short and grounded.
    out = []
    for d in drivers:
        sign = "+" if d["impact_hours"] > 0 else ""
        out.append(f"{d['meaning']} ({sign}{d['impact_hours']:.2f} hrs)")
    return out


SYSTEM = "You are a defense readiness analyst. You MUST use only provided facts. Do not introduce new facts."
USER_TEMPLATE = """Generate a commander-ready readiness brief using ONLY the structured facts below.
- Do NOT invent additional causes, units, locations, or events.
- Do NOT speculate beyond the listed drivers.
- Keep it concise.

STRUCTURED FACTS (JSON):
{payload}

Return in this format:
Summary:
Key Drivers:
Operational Interpretation:
Confidence/Limitations:
"""


def make_prompt(payload: dict) -> str:
    return USER_TEMPLATE.format(payload=json.dumps(payload, indent=2))


def main():
    client = AzureOpenAI(
        azure_endpoint=ENDPOINT,
        api_key=API_KEY,
        api_version=API_VERSION,
    )

    df = pd.read_csv("models/explanations/shap_summary_sample.csv")
    os.makedirs("rag/output", exist_ok=True)

    N = 10
    briefs_md = ["# Azure OpenAI Readiness Briefs (SHAP-grounded)\n"]

    for i in range(min(N, len(df))):
        row = df.iloc[i]

        drivers_raw = ast.literal_eval(row["top_5_drivers"])
        drivers = []
        for feat, impact in drivers_raw:
            # Keep the feature name AND the impact; meaning can be added later if you want
            drivers.append({"feature": feat, "impact_hours": float(impact)})

        payload = {
            "date": row["date"],
            "aircraft_id": row["aircraft_id"],
            "prediction": {
                "downtime_next_14d_hours": round(float(row["y_pred"]), 2),
                "baseline_hours": round(float(row["base_value"]), 2),
            },
            "top_drivers": [
                {"feature": d["feature"], "impact_hours": round(d["impact_hours"], 2)}
                for d in drivers
            ],
            "guardrails": [
                "Use only provided JSON facts",
                "No speculation",
                "Synthetic data demo",
            ],
        }

        resp = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": make_prompt(payload)},
            ],
            temperature=0.2,
        )

        text = resp.choices[0].message.content.strip()

        briefs_md.append(f"## Brief {i+1}: {payload['aircraft_id']} — {payload['date']}")
        briefs_md.append(text)
        briefs_md.append("\n---\n")

    out_path = "rag/output/briefs_azure.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(briefs_md))

    print(f"✅ Wrote: {out_path}")


if __name__ == "__main__":
    main()
