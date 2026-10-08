"""
clean_survey.py
---------------
Cleans the driver survey (Google Form export) into an analysis-ready table.

Input : data/raw/survey_responses.csv   (never modified - see CLAUDE.md)
Output: data/processed/survey_clean.csv

What it does:
  1. Renames the long question columns to short snake_case names
  2. Adds respondent_id (R01, R02...) in timestamp order and vehicle_type
  3. Converts queue_band to queue_hours (band midpoints) and daily_queue_hours
  4. Adds gross_per_hour and, for CNG users, fuel_saving_pct
  5. Adds quality_flag for implausible money figures (values are NOT changed)
  6. Splits the tick-all-that-apply barriers question into one column per barrier
  7. Adds administration_mode (self / interviewer) from the submission time,
     then drops timestamp from the saved file so it can be published

Run from the project root:
    python src/clean_survey.py
"""

import pathlib

import pandas as pd

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "survey_responses.csv"
OUT_PATH = PROJECT_ROOT / "data" / "processed" / "survey_clean.csv"

# ---------------------------------------------------------------------------
# Short names, in the same order as the form's questions.
# We rename by POSITION rather than by matching the full question text: the
# question strings contain "₦", curly brackets and commas, and one typo-fix in
# the form would break a text match. The length check in load_raw() makes sure
# a reordered or extra column fails loudly instead of being silently mislabelled.
# ---------------------------------------------------------------------------
SHORT_NAMES = [
    "timestamp", "consent", "vehicle", "ownership", "days_per_week",
    "hours_per_day", "gross_per_day", "fuel_type", "petrol_spend_per_day",
    "barriers", "convert_if_station", "convert_if_free", "conversion_cost",
    "payment_method", "cng_spend_per_day", "petrol_before_per_day",
    "refuels_per_day", "queue_band", "cng_shortage", "saved_money",
]

# Form answer -> simple vehicle category.
VEHICLE_TYPES = {
    "Ride-hailing car (Uber, Bolt, inDrive, etc.)": "ride_hailing",
    "Danfo / minibus": "danfo",
    "Keke (tricycle)": "keke",
    "Taxi": "taxi",
}

# Queue band -> midpoint in hours. The open-ended top band ("More than 6
# hours") has no midpoint, so we use 7 as a stated assumption.
QUEUE_MIDPOINTS = {
    "Less than 30 minutes": 0.25,
    "30 minutes to 1 hour": 0.75,
    "1 to 2 hours": 1.5,
    "2 to 4 hours": 3,
    "4 to 6 hours": 5,
    "More than 6 hours": 7,
}

# Barrier answer -> column name. Google Forms joins ticked boxes with ", ".
# None of these option texts contain a comma themselves, so splitting on ", "
# is safe; if a new option with a comma is ever added, it will show up as an
# unknown barrier and raise an error (see split_barriers).
BARRIER_COLUMNS = {
    "Conversion is too expensive": "barrier_too_expensive",
    "There are no CNG stations near where I work": "barrier_no_station",
    "The queues at CNG stations are too long": "barrier_long_queues",
    "I am worried about safety": "barrier_safety",
    "The vehicle is not mine": "barrier_not_my_vehicle",
}

# Money columns we expect to be numbers (blank = question not asked).
NUMERIC_COLUMNS = [
    "days_per_week", "hours_per_day", "gross_per_day", "petrol_spend_per_day",
    "conversion_cost", "cng_spend_per_day", "petrol_before_per_day",
    "refuels_per_day",
]

# The interviewer-administered responses were entered in one session on the
# evening of 7 October 2026; everything else was self-completed. Both ends are
# inclusive and given to the minute (21:54 covers a 21:53:56 submission).
INTERVIEWER_WINDOW = (
    pd.Timestamp("2026-10-07 21:24:00"),
    pd.Timestamp("2026-10-07 21:54:59"),
)

# Dropped before saving: exact submission times could help identify a
# respondent, and administration_mode keeps the only thing we need from them.
COLUMNS_NOT_PUBLISHED = ["timestamp"]

# Below this daily gross (₦) we treat the figure as implausible for a
# full-time commercial driver - likely a missing zero or a typo.
MIN_PLAUSIBLE_GROSS = 20_000


def load_raw(path: pathlib.Path = RAW_PATH) -> pd.DataFrame:
    """Read the raw export and give the columns their short names."""
    df = pd.read_csv(path, encoding="utf-8")
    if len(df.columns) != len(SHORT_NAMES):
        raise ValueError(
            f"Expected {len(SHORT_NAMES)} columns, found {len(df.columns)} - "
            "has the form changed?"
        )
    df.columns = SHORT_NAMES
    return df


def queue_band_to_hours(band) -> float:
    """Return the midpoint (hours) of a queue band; NaN if blank (petrol users)."""
    if pd.isna(band):
        return float("nan")
    # Plain dict lookup: an unexpected label raises KeyError on purpose,
    # so a new or misspelt band can't quietly become NaN.
    return QUEUE_MIDPOINTS[band]


def quality_flag(gross_per_day, petrol_spend, cng_spend) -> str:
    """
    Return a short reason string if the money figures look implausible,
    or "" if the row is fine. Several reasons are joined with "; ".

    Comparisons with NaN are always False in pandas/numpy, so a blank fuel
    figure (question not asked) never triggers a flag by itself.
    """
    reasons = []
    if petrol_spend >= gross_per_day:
        reasons.append("petrol spend >= gross")
    if cng_spend >= gross_per_day:
        reasons.append("CNG spend >= gross")
    if gross_per_day < MIN_PLAUSIBLE_GROSS:
        reasons.append(f"gross < {MIN_PLAUSIBLE_GROSS:,}")
    return "; ".join(reasons)


def split_barriers(barriers: pd.Series, asked: pd.Series) -> pd.DataFrame:
    """
    One True/False column per barrier.

    Only petrol-only drivers were asked this question, so for CNG users the
    columns are left as <NA> ("not asked") rather than False ("didn't tick it").
    The nullable "boolean" dtype lets a column hold True / False / <NA>.
    """
    ticked = barriers.fillna("").str.split(", ")
    unknown = {b for row in ticked for b in row if b and b not in BARRIER_COLUMNS}
    if unknown:
        raise ValueError(f"Unknown barrier option(s): {unknown}")

    out = pd.DataFrame(index=barriers.index)
    for label, col in BARRIER_COLUMNS.items():
        out[col] = ticked.apply(lambda row: label in row).astype("boolean")
        out.loc[~asked, col] = pd.NA
    return out


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning steps and return a new DataFrame (input untouched)."""
    df = df.copy()

    # --- Types -------------------------------------------------------------
    # Google Forms writes timestamps as month/day/year.
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%m/%d/%Y %H:%M:%S")
    for col in NUMERIC_COLUMNS:
        # errors="coerce": anything non-numeric becomes NaN instead of crashing.
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- 2. IDs and vehicle type -------------------------------------------
    # Stable sort so tied timestamps keep their export order.
    df = df.sort_values("timestamp", kind="stable").reset_index(drop=True)
    df.insert(0, "respondent_id", [f"R{i:02d}" for i in range(1, len(df) + 1)])
    # .between() is inclusive at both ends by default.
    df["administration_mode"] = df["timestamp"].between(*INTERVIEWER_WINDOW).map(
        {True: "interviewer", False: "self"}
    )
    df["vehicle_type"] = df["vehicle"].map(VEHICLE_TYPES)
    if df["vehicle_type"].isna().any():
        raise ValueError(f"Unmapped vehicle answers: {df.loc[df['vehicle_type'].isna(), 'vehicle'].unique()}")

    # A driver is a "CNG user" if the vehicle runs on CNG at all (CNG only, or
    # bi-fuel CNG + petrol). Only they answered the CNG questions.
    df["uses_cng"] = df["fuel_type"] != "Petrol only"

    # --- 3. Queue time -----------------------------------------------------
    df["queue_hours"] = df["queue_band"].apply(queue_band_to_hours)
    df["daily_queue_hours"] = df["queue_hours"] * df["refuels_per_day"]

    # --- 4. Earnings and fuel saving ----------------------------------------
    df["gross_per_hour"] = df["gross_per_day"] / df["hours_per_day"]
    # .where() keeps the value where the condition is True and puts NaN
    # elsewhere - so petrol-only drivers get a blank, not a fake number.
    df["fuel_saving_pct"] = (
        1 - df["cng_spend_per_day"] / df["petrol_before_per_day"]
    ).where(df["uses_cng"])

    # --- 5. Quality flag (original values are NOT changed) -----------------
    df["quality_flag"] = [
        quality_flag(g, p, c)
        for g, p, c in zip(df["gross_per_day"], df["petrol_spend_per_day"], df["cng_spend_per_day"])
    ]

    # --- 6. Barriers --------------------------------------------------------
    barrier_cols = split_barriers(df["barriers"], asked=~df["uses_cng"])
    df = pd.concat([df, barrier_cols], axis=1)

    return df


def print_summary(df: pd.DataFrame) -> None:
    """Print the headline counts and medians."""
    print(f"Responses: {len(df)}")

    print("\nFuel type:")
    print(df["uses_cng"].map({True: "CNG (incl. bi-fuel)", False: "Petrol only"})
          .value_counts().to_string())
    print("  of which:")
    print(df["fuel_type"].value_counts().to_string())

    print("\nAdministration mode:")
    print(df["administration_mode"].value_counts().to_string())

    print("\nVehicle type:")
    print(df["vehicle_type"].value_counts().to_string())

    flagged = df[df["quality_flag"] != ""]
    print(f"\nFlagged rows: {len(flagged)}")
    for _, row in flagged.iterrows():
        print(f"  {row['respondent_id']} ({row['vehicle_type']}, gross {row['gross_per_day']:,.0f}): "
              f"{row['quality_flag']}")

    clean_rows = df[df["quality_flag"] == ""]
    print(f"\nMedians, unflagged rows only (n = {len(clean_rows)}):")
    # Median ignores NaN, so fuel_saving_pct and daily_queue_hours are
    # medians over CNG users only.
    print(f"  gross_per_hour     : NGN {clean_rows['gross_per_hour'].median():,.0f}  "
          f"(n = {clean_rows['gross_per_hour'].notna().sum()})")
    print(f"  fuel_saving_pct    : {clean_rows['fuel_saving_pct'].median():.1%}  "
          f"(n = {clean_rows['fuel_saving_pct'].notna().sum()})")
    print(f"  daily_queue_hours  : {clean_rows['daily_queue_hours'].median():.2f} h  "
          f"(n = {clean_rows['daily_queue_hours'].notna().sum()})")


def main() -> None:
    df = clean(load_raw())
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Drop only from the saved copy; respondent_id was already assigned in
    # timestamp order inside clean(), so the order is preserved without it.
    df.drop(columns=COLUMNS_NOT_PUBLISHED).to_csv(OUT_PATH, index=False)
    print_summary(df)
    print(f"\nSaved {OUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
