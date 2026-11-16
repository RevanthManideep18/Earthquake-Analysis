import json
from datetime import UTC
from pathlib import Path

from earthquake_pipeline.parser import parse_feature_collection


FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "fixtures"
    / "synthetic_earthquakes.geojson"
)


def test_parse_synthetic_fixture_fields_and_utc_timestamps():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    events = parse_feature_collection(payload)

    assert len(events) == 2
    first = events[0]
    assert first.event_id == "synthetic-quake-001"
    assert first.occurred_at.isoformat() == "2023-11-14T22:13:20+00:00"
    assert first.occurred_at.tzinfo is UTC
    assert first.updated_at.isoformat() == "2023-11-14T22:13:30+00:00"
    assert first.magnitude == 4.2
    assert first.longitude == -118.25
    assert first.latitude == 34.05
    assert first.depth_km == 8.1


def test_missing_magnitude_is_kept_as_none():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    events = parse_feature_collection(payload)

    assert events[1].event_id == "synthetic-quake-002"
    assert events[1].magnitude is None
