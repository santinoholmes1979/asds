import pandas as pd
import numpy as np


def to_dt(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")


def main():
    # Load base training table + inventory + failures + aircraft (for base mapping)
    train = pd.read_csv("data/training_table.csv")
    inv = pd.read_csv("data/inventory_daily.csv")
    failures = pd.read_csv("data/failures.csv")
    aircraft = pd.read_csv("data/aircraft.csv")

    train["date"] = to_dt(train["date"])
    inv["date"] = to_dt(inv["date"])
    failures["date"] = to_dt(failures["date"])

    # Map aircraft -> base (static)
    ac_base = dict(zip(aircraft["aircraft_id"], aircraft["base"]))
    failures["base"] = failures["aircraft_id"].map(ac_base)

    # Join inventory to failures by (date, base, part_id) to get on_hand/eta at time of failure
    inv_keyed = inv[["date", "base", "part_id", "on_hand", "on_order", "expected_days_to_arrival"]].copy()
    fail_inv = failures.merge(inv_keyed, on=["date", "base", "part_id"], how="left")

    # If any inventory rows missing, fill conservatively
    fail_inv["on_hand"] = fail_inv["on_hand"].fillna(0)
    fail_inv["on_order"] = fail_inv["on_order"].fillna(0)
    fail_inv["expected_days_to_arrival"] = fail_inv["expected_days_to_arrival"].fillna(60)

    # Stockout indicator at failure time
    fail_inv["stockout_at_failure"] = (fail_inv["on_hand"] <= 0).astype(int)
    fail_inv["eta_days_at_failure"] = fail_inv["expected_days_to_arrival"].astype(float)

    # Aggregate per aircraft-day: supply friction signals tied to actual failures
    daily_supply = (
        fail_inv.groupby(["date", "aircraft_id"], as_index=False)
        .agg(
            stockouts_today=("stockout_at_failure", "sum"),
            eta_days_sum_today=("eta_days_at_failure", "sum"),
            eta_days_mean_today=("eta_days_at_failure", "mean"),
        )
    )

    # Merge onto training table (days with no failures => zeros)
    out = train.merge(daily_supply, on=["date", "aircraft_id"], how="left")
    out["stockouts_today"] = out["stockouts_today"].fillna(0.0)
    out["eta_days_sum_today"] = out["eta_days_sum_today"].fillna(0.0)
    out["eta_days_mean_today"] = out["eta_days_mean_today"].fillna(0.0)

    # Rolling windows for these new supply signals
    out = out.sort_values(["aircraft_id", "date"])
    windows = [7, 14, 30]
    for w in windows:
        out[f"stockouts_sum_{w}d"] = (
            out.groupby("aircraft_id", sort=False)["stockouts_today"]
            .rolling(w, min_periods=1)
            .sum()
            .reset_index(level=0, drop=True)
        )
        out[f"eta_days_sum_{w}d"] = (
            out.groupby("aircraft_id", sort=False)["eta_days_sum_today"]
            .rolling(w, min_periods=1)
            .sum()
            .reset_index(level=0, drop=True)
        )
        out[f"eta_days_mean_{w}d"] = (
            out.groupby("aircraft_id", sort=False)["eta_days_mean_today"]
            .rolling(w, min_periods=1)
            .mean()
            .reset_index(level=0, drop=True)
        )

    # Extra: base-level stockout rate per day (supply stress at the base)
    # stockout = on_hand==0; compute per base-day across all parts
    inv["stockout"] = (inv["on_hand"] <= 0).astype(int)
    base_daily = (
        inv.groupby(["date", "base"], as_index=False)
        .agg(
            base_stockout_rate=("stockout", "mean"),
            base_mean_eta=("expected_days_to_arrival", "mean"),
        )
    )

    out = out.merge(base_daily, on=["date", "base"], how="left")
    out["base_stockout_rate"] = out["base_stockout_rate"].fillna(0.0)
    out["base_mean_eta"] = out["base_mean_eta"].fillna(0.0)

    # Save updated training table
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    out.to_csv("data/training_table_with_inventory.csv", index=False)

    print("✅ Wrote: data/training_table_with_inventory.csv")
    print("Shape:", out.shape)
    print("\nNew columns (sample):")
    new_cols = [c for c in out.columns if "stockout" in c or "eta_days" in c or c.startswith("base_")]
    print(new_cols[:30])


if __name__ == "__main__":
    main()
