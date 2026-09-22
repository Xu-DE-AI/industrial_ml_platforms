"""
Feast-style feature definitions.

The important production concept is that the same feature definition must be
used for historical training and online inference.

A real Feast project would include:
- entities.py
- feature_views.py
- feature_store.yaml
- online/offline stores
"""

FEATURES = [
    "pressure_mpa_mean_1d",
    "injection_rate_mean_1d",
    "seismic_rate_mean_1d",
    "pressure_change_6h",
    "injection_change_6h",
]

ENTITY = "well_id"
EVENT_TIMESTAMP = "timestamp"
