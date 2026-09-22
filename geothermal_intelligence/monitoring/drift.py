import pandas as pd
from scipy.stats import ks_2samp

def main():
    df = pd.read_parquet("data/generated/gold_features.parquet").sort_values("timestamp")
    split = df["timestamp"].quantile(.85)

    ref = df[df.timestamp <= split]
    prod = df[df.timestamp > split]

    for feature in ["pressure_mpa", "injection_rate", "seismic_rate"]:
        stat, p = ks_2samp(ref[feature], prod[feature])
        print(feature, {"ks": float(stat), "pvalue": float(p), "drift": p < .01})

if __name__ == "__main__":
    main()
