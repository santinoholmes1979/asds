import pandas as pd


def _to_dt(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")


def _rolling_sum(df: pd.DataFrame, value_col: str, windows: list[int], group_col: str, date_col: str) -> pd.DataFrame:
    """
    Returns df with new columns: f"{value_col}_sum_{w}d" for each w in windows.
    Assumes df is sorted by group_col, date_col and has one row per day per group.
    """
    out = df.copy()
    out = out.sort_values([group_col, date_col])
    for w in windows:
        out[f"{value_col}_sum_{w}d"] = (
            out.groupby(group_col, sort=False)[value_col]
            .rolling(window=w, min_periods=1)
            .sum()
            .reset_index(level=0, drop=True)
        )
    return out


def main():
    # Load
    aircraft = pd.read_csv("data/aircraft.csv")
    usage = pd.read_csv("data/usage_daily.csv")
    failures = pd.read_csv("data/failures.csv")

    # Parse dates
    usage["date"] = _to_dt(usage["date"])
    failures["date"] = _to_dt(failures["date"])

    # One row per aircraft per day (spine)
    spine = usage[["date", "aircraft_id"]].drop_duplicates().copy()

    # --- Build daily failure aggregates (per aircraft/day) ---
    # Total downtime hours from events that cause downtime (down_event=1)
    failures["event_total_hours"] = failures["repair_hours"] + failures["wait_parts_hours"] + failures["wait_maint_hours"]
    failures["down_hours"] = failures["event_total_hours"] * failures["down_event"]

    daily_fail = (
        failures.groupby(["date", "aircraft_id"], as_index=False)
        .agg(
            failures_count=("failure_id", "count"),
            down_events=("down_event", "sum"),
            repair_hours=("repair_hours", "sum"),
            wait_parts_hours=("wait_parts_hours", "sum"),
            wait_maint_hours=("wait_maint_hours", "sum"),
            down_hours=("down_hours", "sum"),
        )
    )

    # Merge onto spine (fill missing days with zeros)
    df = spine.merge(daily_fail, on=["date", "aircraft_id"], how="left")
    for c in ["failures_count","down_events","repair_hours","wait_parts_hours","wait_maint_hours","down_hours"]:
        df[c] = df[c].fillna(0.0)

    # --- Create labels: future downtime sums ---
    # For each aircraft-day, label is sum of down_hours over next N days (excluding today).
    df = df.sort_values(["aircraft_id", "date"])
    for horizon in [14, 30]:
        df[f"downtime_next_{horizon}d_hours"] = (
            df.groupby("aircraft_id", sort=False)["down_hours"]
            .shift(-1)  # start tomorrow
            .rolling(window=horizon, min_periods=1)
            .sum()
            .reset_index(level=0, drop=True)
        ).fillna(0.0)

    labels = df[["date","aircraft_id","downtime_next_14d_hours","downtime_next_30d_hours"]].copy()

    # --- Feature engineering (rolling history sums over past windows including today) ---
    windows = [7, 14, 30]
    feat = df[["date","aircraft_id","failures_count","down_events","repair_hours","wait_parts_hours","wait_maint_hours","down_hours"]].copy()

    feat = _rolling_sum(feat, "failures_count", windows, "aircraft_id", "date")
    feat = _rolling_sum(feat, "down_events", windows, "aircraft_id", "date")
    feat = _rolling_sum(feat, "repair_hours", windows, "aircraft_id", "date")
    feat = _rolling_sum(feat, "wait_parts_hours", windows, "aircraft_id", "date")
    feat = _rolling_sum(feat, "wait_maint_hours", windows, "aircraft_id", "date")
    feat = _rolling_sum(feat, "down_hours", windows, "aircraft_id", "date")

    # Usage-based rolling features
    usage_feat = usage[["date","aircraft_id","flight_hours","mission_intensity","environment_stress"]].copy()
    usage_feat = usage_feat.sort_values(["aircraft_id","date"])
    for w in windows:
        usage_feat[f"flight_hours_sum_{w}d"] = (
            usage_feat.groupby("aircraft_id", sort=False)["flight_hours"].rolling(w, min_periods=1).sum().reset_index(level=0, drop=True)
        )
        usage_feat[f"mission_intensity_mean_{w}d"] = (
            usage_feat.groupby("aircraft_id", sort=False)["mission_intensity"].rolling(w, min_periods=1).mean().reset_index(level=0, drop=True)
        )
        usage_feat[f"environment_stress_mean_{w}d"] = (
            usage_feat.groupby("aircraft_id", sort=False)["environment_stress"].rolling(w, min_periods=1).mean().reset_index(level=0, drop=True)
        )

    # Static aircraft attributes
    aircraft_static = aircraft[["aircraft_id","unit_id","base","airframe_age_years","role","status_start"]].copy()

    # Assemble training table
    training = (
        spine.merge(aircraft_static, on="aircraft_id", how="left")
        .merge(usage_feat, on=["date","aircraft_id"], how="left")
        .merge(feat.drop(columns=["failures_count","down_events","repair_hours","wait_parts_hours","wait_maint_hours","down_hours"]), on=["date","aircraft_id"], how="left")
        .merge(labels, on=["date","aircraft_id"], how="left")
    )

    # Save
    labels_out = labels.copy()
    labels_out["date"] = labels_out["date"].dt.strftime("%Y-%m-%d")
    training_out = training.copy()
    training_out["date"] = training_out["date"].dt.strftime("%Y-%m-%d")

    labels_out.to_csv("data/downtime_labels.csv", index=False)
    training_out.to_csv("data/training_table.csv", index=False)

    print("✅ Wrote: data/downtime_labels.csv")
    print("✅ Wrote: data/training_table.csv")
    print("Training shape:", training_out.shape)

    # Quick checks
    print("\nLabel sanity:")
    print(training_out[["downtime_next_14d_hours","downtime_next_30d_hours"]].describe().round(2))

    # How many non-zero labels?
    nz14 = (training_out["downtime_next_14d_hours"] > 0).sum()
    nz30 = (training_out["downtime_next_30d_hours"] > 0).sum()
    print(f"\nNon-zero labels: 14d={nz14}, 30d={nz30} (out of {len(training_out)})")


if __name__ == "__main__":
    main()
