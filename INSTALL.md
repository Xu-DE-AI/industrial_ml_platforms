# Installation notes

Start lightweight.

## GeoScale

```bash
cd geoscale_platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m data.generate
python -m data.validate
python -m training.train
```

Optional:

```bash
pip install pyspark
pip install confluent-kafka
pip install scipy
```

## Geothermal

```bash
cd geothermal_intelligence
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m data.generate
python -m quality.validate
python -m features.build
python -m training.train
python -m monitoring.drift
```

Feast, Iceberg, Flink, Terraform and Kubernetes are intentionally optional.
Learn the local Python pipeline first, then add infrastructure one layer at a time.

On Apple Silicon, prefer Docker services and Python versions with available wheels.
Do not install every distributed framework simultaneously.
