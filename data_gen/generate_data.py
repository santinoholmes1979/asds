import os
import uuid
from datetime import date, timedelta

import numpy as np
import pandas as pd


def main():
    rng = np.random.default_rng(42)
    out_dir = "data"
    os.makedirs(out_dir, exist_ok=True)

    # Sizes
    days = 30
    n_bases = 3
    n_units = 4
    n_aircraft = 40
    n_parts = 200

    # Create bases/units
    bases = [f"BASE_{chr(ord('A') + i)}" for i in range(n_bases)]
    units = [f"UNIT_{i+1:02d}" for i in range(n_units)]
    roles = ["STRIKE", "ISR", "TRAIN"]

    # Aircraft
    aircraft = []
    for i in range(n_aircraft):
        aircraft.append(
            {
                "aircraft_id": f"AC_{i+1:04d}",
                "unit_id": rng.choice(units),
                "base": rng.choice(bases),
                "airframe_age_years": float(np.round(rng.uniform(0.5, 18.0), 1)),
                "role": rng.choice(roles, p=[0.45, 0.25, 0.30]),
                "status_start": rng.choice(["FMC", "PMC"], p=[0.75, 0.25]),
            }
        )
    aircraft_df = pd.DataFrame(aircraft)

    # Parts
    categories = ["AVIONICS", "HYDRAULIC", "ELECTRICAL", "PROPULSION", "STRUCTURAL"]
    parts = []
    for i in range(n_parts):
        cat = rng.choice(categories, p=[0.25, 0.18, 0.22, 0.15, 0.20])
        criticality = int(rng.choice([1, 2, 3, 4, 5], p=[0.10, 0.20, 0.35, 0.25, 0.10]))
        mtbf_hours = float(np.round(rng.uniform(250, 2200), 1))
        mean_repair_hours = float(np.round(rng.uniform(2.0, 18.0), 2))
        vendor_risk = float(np.round(rng.beta(2, 3), 2))
        unit_cost = float(np.round(rng.uniform(500, 60000) * (1 + 0.12 * (criticality - 3)), 2))
        parts.append(
            {
                "part_id": f"P_{i+1:04d}",
                "part_category": cat,
                "criticality": criticality,
                "mtbf_hours": mtbf_hours,
                "mean_repair_hours": mean_repair_hours,
                "vendor_risk": vendor_risk,
                "unit_cost": unit_cost,
            }
        )
    parts_df = pd.DataFrame(parts)

    # Usage (daily time series)
    start = date.today() - timedelta(days=days)
    usage_rows = []
    for d in range(days):
        dt = (start + timedelta(days=d)).isoformat()
        tempo_shift = float(np.clip(rng.normal(0.0, 0.12), -0.25, 0.25))
        stress_shift = float(np.clip(rng.normal(0.0, 0.10), -0.25, 0.25))
        for _, ac in aircraft_df.iterrows():
            base_hours = {"STRIKE": 1.6, "ISR": 1.8, "TRAIN": 1.2}[ac["role"]]
            age_factor = float(np.clip(1.0 - (ac["airframe_age_years"] / 35.0), 0.65, 1.05))
            flight_hours = float(np.clip(rng.normal(base_hours * age_factor, 0.55), 0.0, 4.5))
            mission_intensity = float(np.clip(rng.beta(2, 2) + tempo_shift, 0.0, 1.0))
            environment_stress = float(np.clip(rng.beta(2, 3) + stress_shift, 0.0, 1.0))
            usage_rows.append(
                {
                    "date": dt,
                    "aircraft_id": ac["aircraft_id"],
                    "flight_hours": round(flight_hours, 2),
                    "mission_intensity": round(mission_intensity, 3),
                    "environment_stress": round(environment_stress, 3),
                }
            )
    usage_df = pd.DataFrame(usage_rows)

    # Inventory (daily, sparse)
    inv_rows = []
    for d in range(days):
        dt = (start + timedelta(days=d)).isoformat()
        for base in bases:
            for _, p in parts_df.iterrows():
                criticality = int(p["criticality"])
                on_hand = int(np.clip(rng.poisson(2.0 + 1.1 * criticality), 0, 25))
                on_order = int(rng.choice([0, 0, 0, 1, 2]))
                eta = int(np.clip(rng.normal(20 + 25 * p["vendor_risk"], 9), 3, 90)) if on_order > 0 else 0
                inv_rows.append(
                    {
                        "date": dt,
                        "base": base,
                        "part_id": p["part_id"],
                        "on_hand": on_hand,
                        "on_order": on_order,
                        "expected_days_to_arrival": eta,
                    }
                )
    inventory_df = pd.DataFrame(inv_rows)

    # Failures (influenced by usage + age + stress)
    ac_base = dict(zip(aircraft_df["aircraft_id"], aircraft_df["base"]))
    ac_age = dict(zip(aircraft_df["aircraft_id"], aircraft_df["airframe_age_years"]))

    # part selection weights: lower mtbf => higher chance
    mtbf = parts_df["mtbf_hours"].to_numpy()
    w = (mtbf.max() - mtbf) / (mtbf.max() - mtbf.min() + 1e-9)
    w = np.clip(w, 0.05, None)
    w = w / w.sum()
    part_ids = parts_df["part_id"].to_list()

    base_rate = 0.018
    failures = []
    for (dt, aircraft_id), g in usage_df.groupby(["date", "aircraft_id"], sort=False):
        fh = float(g["flight_hours"].iloc[0])
        intensity = float(g["mission_intensity"].iloc[0])
        stress = float(g["environment_stress"].iloc[0])
        age = float(ac_age[aircraft_id])

        lam = base_rate * float(np.clip(1.0 + age / 18.0, 1.0, 2.2)) * float(np.clip(0.7 + 0.35 * fh + 0.45 * intensity + 0.35 * stress, 0.6, 2.3))
        lam = float(np.clip(lam, 0.001, 0.35))
        n_fail = int(np.clip(rng.poisson(lam), 0, 2))
        if n_fail == 0:
            continue

        chosen = list(rng.choice(part_ids, size=n_fail, replace=False, p=w))
        for part_id in chosen:
            p = parts_df.loc[parts_df["part_id"] == part_id].iloc[0]
            criticality = int(p["criticality"])
            severity = int(rng.choice([1, 2, 3, 4, 5], p=[0.25, 0.25, 0.22, 0.18, 0.10]))
            down_prob = float(np.clip(0.10 + 0.08 * (severity - 1) + 0.06 * (criticality - 1), 0.05, 0.98))
            down_event = int(rng.random() < down_prob)
            repair_hours = float(np.clip(rng.normal(float(p["mean_repair_hours"]) * (1 + 0.18 * (severity - 1)), 1.2), 0.5, 60.0))
            wait_parts_hours = float(np.clip(rng.normal(2.0 + 8.0 * float(p["vendor_risk"]), 6.0), 0.0, 400.0))
            wait_maint_hours = float(np.clip(rng.normal(1.5 + 2.0 * intensity + 1.5 * stress, 1.8), 0.0, 48.0))

            failures.append(
                {
                    "failure_id": f"F_{uuid.uuid4().hex[:10]}",
                    "date": dt,
                    "aircraft_id": aircraft_id,
                    "part_id": part_id,
                    "severity": severity,
                    "down_event": down_event,
                    "repair_hours": round(repair_hours, 2),
                    "wait_parts_hours": round(wait_parts_hours, 2),
                    "wait_maint_hours": round(wait_maint_hours, 2),
                }
            )
    failures_df = pd.DataFrame(failures)

    # Write outputs
    aircraft_df.to_csv(os.path.join(out_dir, "aircraft.csv"), index=False)
    parts_df.to_csv(os.path.join(out_dir, "parts.csv"), index=False)
    usage_df.to_csv(os.path.join(out_dir, "usage_daily.csv"), index=False)
    inventory_df.to_csv(os.path.join(out_dir, "inventory_daily.csv"), index=False)
    failures_df.to_csv(os.path.join(out_dir, "failures.csv"), index=False)

    print("✅ Generated files in ./data")
    print(f"Aircraft:  {len(aircraft_df):,}")
    print(f"Parts:    {len(parts_df):,}")
    print(f"Usage:    {len(usage_df):,} rows")
    print(f"Inventory:{len(inventory_df):,} rows")
    print(f"Failures: {len(failures_df):,} events")
    if len(failures_df) > 0:
        vc = failures_df["part_id"].value_counts().head(5)
        print("\nTop 5 parts by failure count:")
        for pid, cnt in vc.items():
            print(f"  {pid}: {cnt}")


if __name__ == "__main__":
    main()
