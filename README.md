# Earthquake Data Pipeline

A small, local Python + DuckDB project for learning data engineering with public USGS earthquake data. It is designed to run on a personal computer without Docker, cloud accounts, API keys, or a background service.

## Milestone 1: offline foundation

The first milestone uses only the explicitly synthetic file `data/fixtures/synthetic_earthquakes.geojson`. It parses GeoJSON event fields and prints a preview; it does not contact USGS or write to DuckDB yet.

### Set up the isolated environment

Python 3.11 or newer is required. From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

The project pins DuckDB to `2.0.0` and pytest to `9.2.0` in `pyproject.toml`. DuckDB is in-process, so it does not require a running database service.

### Run the offline demo and tests

```bash
python -m earthquake_pipeline
pytest
```

## Learning journal

- **Decision:** begin with a local, synthetic GeoJSON response so parsing work and tests never depend on network availability.
- **Decision:** keep timestamps timezone-aware in UTC; treat USGS coordinate order as longitude, latitude, depth in kilometers.
- **Milestone 1 result:** the offline demo parsed 2 synthetic events; pytest ran 2 tests and both passed on Python 3.14.6 / macOS arm64.
- **Next:** add bounded extraction from the USGS FDSN Event Web Service and preserve each raw response with request metadata.
