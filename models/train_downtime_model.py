import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from lightgbm import LGBMRegressor
import joblib
import os


def main():
    # Load training table
    df = pd.read_csv("data/training_table.csv")

    target = "downtime_next_14d_hours"

    # Drop rows where target is missing (should be none, but safe)
    df = df.dropna(subset=[target])

    # Define features
    categorical = ["unit_id", "base", "role", "status_start"]
    numeric = [c for c in df.columns if c not in categorical + ["date", "aircraft_id", target, "downtime_next_30d_hours"]]

    X = df[categorical + numeric]
    y = df[target]

    # Train / test split (time-aware-ish)
    # We shuffle=False to reduce leakage
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, shuffle=False
    )

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric),
        ]
    )

    # Model
    model = LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=-1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )

    pipeline = Pipeline(
        steps=[
            ("prep", preprocessor),
            ("model", model),
        ]
    )

    # Train
    pipeline.fit(X_train, y_train)

    # Predict
    preds = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))


    print("✅ Model trained")
    print(f"MAE : {mae:.3f} hours")
    print(f"RMSE: {rmse:.3f} hours")

    # Save model
    os.makedirs("models/artifacts", exist_ok=True)
    joblib.dump(pipeline, "models/artifacts/downtime_14d_model.joblib")

    print("✅ Saved model to models/artifacts/downtime_14d_model.joblib")

    # Feature importance (top 15)
    booster = pipeline.named_steps["model"]
    feature_names = pipeline.named_steps["prep"].get_feature_names_out()
    importances = booster.feature_importances_

    fi = (
        pd.DataFrame({"feature": feature_names, "importance": importances})
        .sort_values("importance", ascending=False)
        .head(15)
    )

    print("\nTop 15 features:")
    print(fi.to_string(index=False))


if __name__ == "__main__":
    main()
