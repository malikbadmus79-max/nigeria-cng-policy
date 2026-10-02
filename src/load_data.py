"""
load_data.py
------------
Entry point for data validation. Loads all CSVs from data/raw/ and
audits model_inputs.csv for missing source citations.

Run from the project root:
    python src/load_data.py
"""

import csv
import pathlib
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Locate data/raw/ relative to this file's parent (the project root).
#    Using pathlib keeps paths OS-independent and avoids hard-coding the
#    working directory — the script works whether you run it from project
#    root or the src/ folder.
# ---------------------------------------------------------------------------
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Confidence labels for rows that are allowed to have no source_ids:
#   "Gap"        - a survey item with no value yet
#   "Assumption" - a working value we chose ourselves (e.g. 312 working days),
#                  to be checked against survey data
# A set, so adding another placeholder label later is a one-word change.
PLACEHOLDER_CONFIDENCE = {"Gap", "Assumption"}


def read_csv_safe(path: pathlib.Path) -> pd.DataFrame:
    """
    Read a CSV where the last column (notes) may contain unquoted commas.

    Standard pandas read_csv rejects rows with more fields than the header,
    and we cannot edit raw files. Instead we use Python's csv.reader and
    manually merge any overflow columns back into the final 'notes' cell,
    preserving every row intact.
    """
    rows = []
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        n_cols = len(header)
        for raw_row in reader:
            if len(raw_row) > n_cols:
                # Extra commas inside the notes field — rejoin them.
                fixed = raw_row[: n_cols - 1] + [",".join(raw_row[n_cols - 1 :])]
                rows.append(fixed)
            else:
                rows.append(raw_row)
    return pd.DataFrame(rows, columns=header)


def load_all_csvs(raw_dir: pathlib.Path) -> dict[str, pd.DataFrame]:
    """Load every CSV in raw_dir and return a {filename_stem: DataFrame} dict."""
    frames = {}
    for csv_path in sorted(raw_dir.glob("*.csv")):
        # Use read_csv_safe so that note fields with unquoted commas don't crash.
        # keep_default_na=False is handled inside read_csv_safe (empty cells stay
        # as "" rather than NaN, which keeps the source-check logic simple).
        df = read_csv_safe(csv_path)
        frames[csv_path.stem] = df
        print(f"  Loaded {csv_path.name:40s}  {len(df)} rows × {len(df.columns)} cols")
    return frames


def audit_model_inputs(df: pd.DataFrame) -> list[dict]:
    """
    Return a list of rows in model_inputs.csv that are missing a source_id
    but whose confidence is NOT a placeholder label ('Gap' or 'Assumption').

    The project rule (docs/sources.md / CLAUDE.md) is:
      - Every number must trace to a source.
      - Rows marked confidence='Gap' are intentional survey placeholders —
        they have no published source yet, so we skip them.
      - Rows marked confidence='Assumption' are values we chose ourselves and
        say so openly; they are listed in the report, not flagged as errors.
      - Everything else must have a non-empty source_ids value.
    """
    problems = []
    for _, row in df.iterrows():
        is_placeholder = str(row["confidence"]).strip() in PLACEHOLDER_CONFIDENCE
        has_source = str(row["source_ids"]).strip() != ""

        if not is_placeholder and not has_source:
            problems.append({
                "parameter": row["parameter"],
                "vehicle":   row["vehicle"],
                "confidence": row["confidence"],
                "notes":     row.get("notes", ""),
            })
    return problems


def main():
    print("=" * 60)
    print("Loading raw data files")
    print("=" * 60)

    # ---------------------------------------------------------------------------
    # 2. Load all CSVs and report their shape.
    # ---------------------------------------------------------------------------
    frames = load_all_csvs(RAW_DIR)

    print()
    print("=" * 60)
    print("Auditing model_inputs.csv for missing source citations")
    print("=" * 60)

    model_df = frames["model_inputs"]

    # ---------------------------------------------------------------------------
    # 3. Count total input rows, then separate placeholders from sourced rows.
    #    "Gap" rows flag survey items we still need to collect; "Assumption"
    #    rows are working values we chose. Every other row must have a
    #    source_ids entry.
    # ---------------------------------------------------------------------------
    total_rows      = len(model_df)
    confidence      = model_df["confidence"].str.strip()
    gap_rows        = model_df[confidence == "Gap"]
    assumption_rows = model_df[confidence == "Assumption"]
    sourced_rows    = model_df[~confidence.isin(PLACEHOLDER_CONFIDENCE)]
    problems        = audit_model_inputs(model_df)

    print(f"\n  Total input rows   : {total_rows}")
    print(f"  Sourced rows       : {len(sourced_rows)}")
    print(f"  Intentional gaps   : {len(gap_rows)}  (confidence == 'Gap')")
    print(f"  Assumptions        : {len(assumption_rows)}  (confidence == 'Assumption')")

    # ---------------------------------------------------------------------------
    # 4. List the intentional Gap rows so the user knows what still needs
    #    primary research or survey data.
    # ---------------------------------------------------------------------------
    print("\nGap rows (survey items — no published source yet):")
    for _, row in gap_rows.iterrows():
        print(f"    {row['parameter']:<40s}  vehicle={row['vehicle']:<8s}  notes={row['notes']}")

    # ---------------------------------------------------------------------------
    # 5. List the Assumption rows, so unsourced working values stay visible
    #    every time the audit runs instead of being silently accepted.
    # ---------------------------------------------------------------------------
    print("\nAssumption rows (our own working values — check against survey):")
    for _, row in assumption_rows.iterrows():
        print(f"    {row['parameter']:<40s}  vehicle={row['vehicle']:<8s}  notes={row['notes']}")

    # ---------------------------------------------------------------------------
    # 6. Flag any other rows that are ALSO missing a source — these are
    #    genuine data-quality issues that need to be fixed before modelling.
    # ---------------------------------------------------------------------------
    print()
    if problems:
        print(f"WARNING: {len(problems)} row(s) are missing source_ids:")
        for p in problems:
            print(f"    parameter={p['parameter']:<40s}  vehicle={p['vehicle']:<8s}  confidence={p['confidence']}")
    else:
        print("OK: every row except Gap/Assumption placeholders has at least one source_id.")

    print()


if __name__ == "__main__":
    main()
