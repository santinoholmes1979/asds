import os
import numpy as np
import pandas as pd
import joblib

# Try to import shap; if unavailable, we'll fall back to LightGBM pred_contrib.
try:
    import shap  # type: ignore
    SHAP_AVAILABLE = True
except Exception:
    SHAP_AVAILABLE = False


MODEL_PATHS = [
    "models/artifacts/downtime_14d_model_with_inventory.joblib",
    "models/artifacts/downtime_14d_model.joblib",
    "models/artifacts/downtime_14d_model_base.joblib",
]


def pick_model_path() -> str:
    for p in MODEL_PATHS:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"No model artifact found. Looked for: {MODEL_PATHS}")


def top_drivers(feature_names: np.ndarray, contrib_row: np.ndarray, k: int = 5):
    # Expects contrib_row to be per-feature contribution (no bias term)
    idx = np.argsort(np.abs(contrib_row))[::-1][:k]
    return [(feature_names[i], float(contrib_row[i])) for i in idx]


def main():
    # Prefer inventory table if available
    data_path = "data/training_table_with_inventory.csv" if os.path.exists("data/training_table_with_inventory.csv") else "data/training_table.csv"
    df = pd.read_csv(data_path)

    target = "downtime_next_14d_hours"
    df = df.dropna(subset=[target])

    # Take a slice from the tail to mimic "future" holdout (matches your shuffle=False split style)
    sample = df.tail(200).copy()

    # Load pipeline (prep + model)
    model_path = pick_model_path()
    pipe = joblib.load(model_path)

    # Prepare features in same way as training scripts
    categorical = ["unit_id", "base", "role", "status_start"]
    drop_cols = ["date", "aircraft_id", target, "downtime_next_30d_hours"]
    numeric = [c for c in sample.columns if c not in categorical + drop_cols]

    X = sample[categorical + numeric]
    y = sample[target].to_numpy()

    preds = pipe.predict(X)

    prep = pipe.named_steps["prep"]
    model = pipe.named_steps["model"]

    # Transform into model input space (one-hot + numeric passthrough)
    X_trans = prep.transform(X)
    feature_names = prep.get_feature_names_out()

    out_rows = []
    os.makedirs("models/explanations", exist_ok=True)

    if SHAP_AVAILABLE:
        # SHAP TreeExplainer (best)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_trans)  # (n_samples, n_features)
        base_value = float(explainer.expected_value)

        for i in range(len(sample)):
            contrib = shap_values[i]
            drivers = top_drivers(feature_names, contrib, k=5)

            out_rows.append(
                {
                    "date": sample.iloc[i]["date"],
                    "aircraft_id": sample.iloc[i]["aircraft_id"],
                    "y_true": float(y[i]),
                    "y_pred": float(preds[i]),
                    "base_value": base_value,
                    "top_5_drivers": drivers,
                }
            )

        # Save full SHAP matrix (can be big, but your sample is small)
        shap_df = pd.DataFrame(shap_values, columns=feature_names)
        shap_df.insert(0, "date", sample["date"].values)
        shap_df.insert(1, "aircraft_id", sample["aircraft_id"].values)
        shap_df.insert(2, "y_pred", preds)
        shap_df.to_csv("models/explanations/shap_values_sample.csv", index=False)

        summary = pd.DataFrame(out_rows)
        summary.to_csv("models/explanations/shap_summary_sample.csv", index=False)

        print("✅ SHAP (package) path used.")
        print("Wrote:")
        print(" - models/explanations/shap_values_sample.csv")
        print(" - models/explanations/shap_summary_sample.csv")
        print("\nExample row (top drivers):")
        print(summary.head(1).to_string(index=False))

    else:
        # Fallback: LightGBM pred_contrib (SHAP-style contributions)
        # Returns contributions including last column as bias term.
        contrib = model.predict(X_trans, pred_contrib=True)
        bias = contrib[:, -1]
        contrib = contrib[:, :-1]

        for i in range(len(sample)):
            drivers = top_drivers(feature_names, contrib[i], k=5)
            out_rows.append(
                {
                    "date": sample.iloc[i]["date"],
                    "aircraft_id": sample.iloc[i]["aircraft_id"],
                    "y_true": float(y[i]),
                    "y_pred": float(preds[i]),
                    "base_value": float(bias[i]),
                    "top_5_drivers": drivers,
                }
            )

        contrib_df = pd.DataFrame(contrib, columns=feature_names)
        contrib_df.insert(0, "date", sample["date"].values)
        contrib_df.insert(1, "aircraft_id", sample["aircraft_id"].values)
        contrib_df.insert(2, "y_pred", preds)
        contrib_df.to_csv("models/explanations/shap_like_contrib_sample.csv", index=False)

        summary = pd.DataFrame(out_rows)
        summary.to_csv("models/explanations/shap_like_summary_sample.csv", index=False)

        print("✅ Fallback path used (LightGBM pred_contrib=True).")
        print("Wrote:")
        print(" - models/explanations/shap_like_contrib_sample.csv")
        print(" - models/explanations/shap_like_summary_sample.csv")
        print("\nExample row (top drivers):")
        print(summary.head(1).to_string(index=False))


if __name__ == "__main__":
    main()
