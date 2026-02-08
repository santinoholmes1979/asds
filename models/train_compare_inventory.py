import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from lightgbm import LGBMRegressor


def train_eval(df: pd.DataFrame, target: str):
    categorical = ["unit_id", "base", "role", "status_start"]
    drop_cols = ["date", "aircraft_id", target, "downtime_next_30d_hours"]
    numeric = [c for c in df.columns if c not in categorical + drop_cols]

    X = df[categorical + numeric]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric),
        ]
    )

    model = LGBMRegressor(
        n_estimators=350,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )

    pipe = Pipeline([("prep", preprocessor), ("model", model)])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))

    # feature importance
    feature_names = pipe.named_steps["prep"].get_feature_names_out()
    importances = pipe.named_steps["model"].feature_importances_
    top = (
        pd.DataFrame({"feature": feature_names, "importance": importances})
        .sort_values("importance", ascending=False)
        .head(10)
    )
    return pipe, mae, rmse, top


def main():
    target = "downtime_next_14d_hours"

    base_df = pd.read_csv("data/training_table.csv").dropna(subset=[target])
    inv_df = pd.read_csv("data/training_table_with_inventory.csv").dropna(subset=[target])

    print("== BASE FEATURES ==")
    base_model, base_mae, base_rmse, base_top = train_eval(base_df, target)
    print(f"MAE : {base_mae:.3f} hours")
    print(f"RMSE: {base_rmse:.3f} hours")
    print("\nTop 10 features (base):")
    print(base_top.to_string(index=False))

    print("\n== + INVENTORY FEATURES ==")
    inv_model, inv_mae, inv_rmse, inv_top = train_eval(inv_df, target)
    print(f"MAE : {inv_mae:.3f} hours")
    print(f"RMSE: {inv_rmse:.3f} hours")
    print("\nTop 10 features (+inventory):")
    print(inv_top.to_string(index=False))

    print("\n== DELTA ==")
    print(f"MAE  improvement: {base_mae - inv_mae:+.3f} hours (positive is better)")
    print(f"RMSE improvement: {base_rmse - inv_rmse:+.3f} hours (positive is better)")

    # Save the better model artifact
    os.makedirs("models/artifacts", exist_ok=True)
    if inv_mae <= base_mae:
        joblib.dump(inv_model, "models/artifacts/downtime_14d_model_with_inventory.joblib")
        print("\n✅ Saved better model: models/artifacts/downtime_14d_model_with_inventory.joblib")
    else:
        joblib.dump(base_model, "models/artifacts/downtime_14d_model_base.joblib")
        print("\n✅ Saved better model: models/artifacts/downtime_14d_model_base.joblib")


if __name__ == "__main__":
    main()
