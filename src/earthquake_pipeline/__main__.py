"""Run a preview of the synthetic fixture."""

import json
from pathlib import Path

from earthquake_pipeline.parser import parse_feature_collection


def main() -> None:
    fixture = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "fixtures"
        / "synthetic_earthquakes.geojson"
    )
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    events = parse_feature_collection(payload)

    print("SYNTHETIC TRAINING DATA ONLY — no USGS API request was made")
    print(f"Parsed events: {len(events)}")
    for event in events:
        magnitude = "missing" if event.magnitude is None else f"M {event.magnitude:.1f}"
        print(
            f"{event.event_id}: {magnitude}; {event.place}; "
            f"{event.occurred_at.isoformat()}; "
            f"lon={event.longitude}, lat={event.latitude}, depth={event.depth_km} km"
        )


if __name__ == "__main__":
    main()
