from pathlib import Path
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from sklearn.calibration import CalibratedClassifierCV
from xgboost import XGBClassifier

FEATURES = [
    "injection_rate", "pressure_mpa", "temperature_c", "flow_rate",
    "seismic_rate", "seismic_distance_km",
    "pressure_mpa_mean_1d", "injection_rate_mean_1d",
    "seismic_rate_mean_1d", "pressure_change_6h",
    "injection_change_6h",
]

def metrics(model, df):
    p = model.predict_proba(df[FEATURES])[:, 1]
    y = df["future_seismic_event_6h"]
    return {
        "roc_auc": roc_auc_score(y, p),
        "pr_auc": average_precision_score(y, p),
        "brier": brier_score_loss(y, p),
    }

def main():
    df = pd.read_parquet("data/generated/gold_features.parquet").sort_values("timestamp")
    cut1 = df["timestamp"].quantile(.70)
    cut2 = df["timestamp"].quantile(.85)

    train = df[df.timestamp <= cut1]
    valid = df[(df.timestamp > cut1) & (df.timestamp <= cut2)]
    test = df[df.timestamp > cut2]

    mlflow.set_experiment("geothermal-seismic-risk")

    base = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=.04,
        subsample=.8,
        colsample_bytree=.8,
        eval_metric="logloss",
        tree_method="hist",
    )

    with mlflow.start_run(run_name="xgboost_calibrated"):
        base.fit(train[FEATURES], train["future_seismic_event_6h"])

        calibrated = CalibratedClassifierCV(base, method="isotonic", cv="prefit")
        calibrated.fit(valid[FEATURES], valid["future_seismic_event_6h"])

        m = metrics(calibrated, test)
        mlflow.log_params({"validation": "chronological", "calibration": "isotonic"})
        mlflow.log_metrics(m)
        mlflow.sklearn.log_model(calibrated, "model")

        print("Holdout:", m)

        Path("artifacts").mkdir(exist_ok=True)
        joblib.dump(calibrated, "artifacts/geothermal_risk_model.joblib")

if __name__ == "__main__":
    main()
