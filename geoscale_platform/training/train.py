from pathlib import Path
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.metrics import (
    roc_auc_score, average_precision_score, brier_score_loss,
    precision_recall_fscore_support
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

FEATURES = [
    "pressure_mpa", "injection_rate", "magnitude",
    "dt", "z_fault_normal"
]

def evaluate(model, X, y):
    p = model.predict_proba(X)[:, 1]
    pred = (p >= .5).astype(int)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y, pred, average="binary", zero_division=0
    )
    return {
        "roc_auc": roc_auc_score(y, p),
        "pr_auc": average_precision_score(y, p),
        "brier": brier_score_loss(y, p),
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }

def main():
    df = pd.read_parquet("data/generated/ae_events.parquet").sort_values("timestamp")

    # Time-based split: never randomly shuffle future information into training.
    n = len(df)
    train = df.iloc[:int(.70*n)]
    valid = df.iloc[int(.70*n):int(.85*n)]
    test = df.iloc[int(.85*n):]

    mlflow.set_experiment("geoscale-risk")

    candidates = {
        "logistic_baseline": Pipeline([
            ("scale", StandardScaler()),
            ("model", LogisticRegression(class_weight="balanced", max_iter=1000)),
        ]),
        "xgboost": XGBClassifier(
            n_estimators=250,
            max_depth=5,
            learning_rate=.05,
            subsample=.8,
            colsample_bytree=.8,
            eval_metric="logloss",
            tree_method="hist",
        ),
    }

    for name, model in candidates.items():
        with mlflow.start_run(run_name=name):
            model.fit(train[FEATURES], train["future_risk_event"])

            metrics = evaluate(model, valid[FEATURES], valid["future_risk_event"])
            mlflow.log_params({"features": ",".join(FEATURES), "split": "time"})
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(model, "model")

            print(name, metrics)

    print("Final holdout:")
    model = candidates["xgboost"]
    model.fit(
        pd.concat([train, valid])[FEATURES],
        pd.concat([train, valid])["future_risk_event"]
    )
    print(evaluate(model, test[FEATURES], test["future_risk_event"]))

    Path("artifacts").mkdir(exist_ok=True)
    joblib.dump(model, "artifacts/risk_model.joblib")

if __name__ == "__main__":
    main()
