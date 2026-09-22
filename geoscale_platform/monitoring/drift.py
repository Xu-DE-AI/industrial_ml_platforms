import numpy as np
from scipy.stats import ks_2samp

def ks_drift(reference, production, alpha=.01):
    statistic, pvalue = ks_2samp(reference, production)
    return {
        "statistic": float(statistic),
        "pvalue": float(pvalue),
        "drift": bool(pvalue < alpha),
    }

def psi(reference, production, bins=10):
    edges = np.quantile(reference, np.linspace(0, 1, bins + 1))
    edges[0] = -np.inf
    edges[-1] = np.inf

    a, _ = np.histogram(reference, bins=edges)
    b, _ = np.histogram(production, bins=edges)

    a = np.maximum(a / a.sum(), 1e-6)
    b = np.maximum(b / b.sum(), 1e-6)

    return float(np.sum((b-a) * np.log(b/a)))
