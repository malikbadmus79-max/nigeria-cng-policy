"""
geocode_stations.py
-------------------
Adds approximate map coordinates to the Lagos CNG station list.

Input : data/raw/lagos_cng_stations.csv            (never modified - see CLAUDE.md)
Output: data/processed/lagos_cng_stations_geocoded.csv

For each station we ask OpenStreetMap's Nominatim geocoder for coordinates:
  1. Full query:  "<name_or_location>, <area_lga>, Lagos, Nigeria"
  2. If nothing is found, an area query:  "<area>, Lagos, Nigeria"
geocode_precision records which one worked ("location" or "area"). An "area"
point is the centre of a neighbourhood, not the station itself, and can be
several kilometres off.

Nominatim is a free public service with a usage policy: identify yourself with
a user agent and send at most one request per second. geopy's RateLimiter
enforces the wait for us.

Run from the project root (needs internet; ~22-44 requests, under a minute):
    python src/geocode_stations.py
"""

import pathlib
import re

import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

from load_data import RAW_DIR, read_csv_safe

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
RAW_PATH = RAW_DIR / "lagos_cng_stations.csv"
OUT_PATH = PROJECT_ROOT / "data" / "processed" / "lagos_cng_stations_geocoded.csv"

USER_AGENT = "nigeria-cng-policy-research"
SUFFIX = ", Lagos, Nigeria"

# Rough Lagos State bounding box, used only as a sanity check on results.
LAT_RANGE = (6.35, 6.75)
LON_RANGE = (2.70, 4.35)


def full_query(name_or_location: str, area_lga: str) -> str:
    """'Mobile Road' + 'Apapa' -> 'Mobile Road, Apapa, Lagos, Nigeria'."""
    return f"{name_or_location}, {area_lga}{SUFFIX}"


def area_name(area_lga: str) -> str:
    """
    The neighbourhood part of area_lga, without the LGA in brackets or after a slash.

        'Ojota (Kosofe)'        -> 'Ojota'
        'Agege / Ifako-Ijaiye'  -> 'Agege'
        'Lagos Island'          -> 'Lagos Island'
    """
    # re.split on "(" or "/" and keep the first piece.
    return re.split(r"[(/]", area_lga)[0].strip()


def area_query(area_lga: str) -> str:
    return f"{area_name(area_lga)}{SUFFIX}"


def in_lagos(lat: float, lon: float) -> bool:
    return LAT_RANGE[0] <= lat <= LAT_RANGE[1] and LON_RANGE[0] <= lon <= LON_RANGE[1]


def geocode_all(stations: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of stations with latitude, longitude, geocode_query, geocode_precision."""
    geolocator = Nominatim(user_agent=USER_AGENT, timeout=10)
    # RateLimiter wraps geocode() so consecutive calls are >= 1 s apart, and
    # retries a couple of times on network errors before giving up.
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.1, max_retries=2, error_wait_seconds=5)

    out = stations.copy()
    results = []
    for _, row in out.iterrows():
        attempts = [
            ("location", full_query(row["name_or_location"], row["area_lga"])),
            ("area", area_query(row["area_lga"])),
        ]
        found = (None, None, None, None)
        for precision, query in attempts:
            # country_codes="ng" stops a vague name matching a place abroad.
            place = geocode(query, country_codes="ng")
            if place is not None:
                found = (place.latitude, place.longitude, query, precision)
                break
        print(f"  {row['station_id']}: {found[3] or 'FAILED':8s} {found[2] or attempts[0][1]}")
        results.append(found)

    out[["latitude", "longitude", "geocode_query", "geocode_precision"]] = pd.DataFrame(
        results, index=out.index
    )
    return out


def main() -> None:
    stations = read_csv_safe(RAW_PATH)

    # The raw file already has latitude/longitude columns, all blank. We fill
    # those (in the output only) rather than adding a second pair. Stop if any
    # are filled in, so a hand-entered coordinate is never overwritten.
    if (stations["latitude"].str.strip() != "").any() or (stations["longitude"].str.strip() != "").any():
        raise ValueError("Raw file already has some coordinates - decide how to merge before geocoding.")

    print(f"Geocoding {len(stations)} stations (about 1 request per second)...")
    geocoded = geocode_all(stations)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    geocoded.to_csv(OUT_PATH, index=False)

    # --- Summary ----------------------------------------------------------
    print("\nGeocode precision:")
    print(geocoded["geocode_precision"].fillna("failed").value_counts().to_string())

    failed = geocoded[geocoded["latitude"].isna()]
    print(f"\nCould not be geocoded: {len(failed)}")
    for _, row in failed.iterrows():
        print(f"  {row['station_id']} {row['name_or_location']} ({row['area_lga']})")

    located = geocoded.dropna(subset=["latitude"])
    outside = located[[not in_lagos(la, lo) for la, lo in zip(located["latitude"], located["longitude"])]]
    print(f"\nOutside the rough Lagos box (lat {LAT_RANGE}, lon {LON_RANGE}): {len(outside)}")
    for _, row in outside.iterrows():
        print(f"  {row['station_id']} {row['name_or_location']}: {row['latitude']:.4f}, {row['longitude']:.4f} "
              f"from '{row['geocode_query']}'")

    print(f"\nSaved {OUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
