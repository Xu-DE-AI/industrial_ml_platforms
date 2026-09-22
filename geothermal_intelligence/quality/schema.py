import pandera.pandas as pa

SCHEMA = pa.DataFrameSchema({
    "timestamp": pa.Column(pa.DateTime, nullable=False),
    "well_id": pa.Column(str, nullable=False),
    "injection_rate": pa.Column(float, checks=pa.Check.ge(0)),
    "pressure_mpa": pa.Column(float, checks=pa.Check.ge(0)),
    "temperature_c": pa.Column(float, checks=pa.Check.between(-50, 400)),
    "flow_rate": pa.Column(float, checks=pa.Check.ge(0)),
    "seismic_rate": pa.Column(float, checks=pa.Check.ge(0)),
    "seismic_distance_km": pa.Column(float, checks=pa.Check.ge(0)),
    "future_seismic_event_6h": pa.Column(int, checks=pa.Check.isin([0, 1])),
})
