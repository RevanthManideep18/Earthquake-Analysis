"""Parse the USGS GeoJSON fields used by the pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class Earthquake:
    """A small, typed view of one GeoJSON earthquake feature."""

    event_id: str
    occurred_at: datetime
    updated_at: datetime
    magnitude: float | None
    place: str | None
    longitude: float
    latitude: float
    depth_km: float


def _milliseconds_to_utc(value: int | float) -> datetime:
    """Convert a USGS Unix timestamp in milliseconds to aware UTC."""
    return datetime.fromtimestamp(value / 1000, tz=UTC)


def parse_feature_collection(payload: dict[str, Any]) -> list[Earthquake]:
    """Turn GeoJSON features into simple Python records.

    Validation and malformed-record quarantine are introduced in a later
    milestone; this first parser is intentionally for well-formed fixture rows.
    """
    events: list[Earthquake] = []
    for feature in payload["features"]:
        properties = feature["properties"]
        longitude, latitude, depth_km = feature["geometry"]["coordinates"]
        magnitude = properties.get("mag")
        events.append(
            Earthquake(
                event_id=feature["id"],
                occurred_at=_milliseconds_to_utc(properties["time"]),
                updated_at=_milliseconds_to_utc(properties["updated"]),
                magnitude=float(magnitude) if magnitude is not None else None,
                place=properties.get("place"),
                longitude=float(longitude),
                latitude=float(latitude),
                depth_km=float(depth_km),
            )
        )
    return events
