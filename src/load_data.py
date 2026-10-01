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
    but whose confidence is NOT 'Gap'.

    The project rule (docs/sources.md / CLAUDE.md) is:
      - Every number must trace to a source.
      - Rows marked confidence='Gap' are intentional survey placeholders —
        they have no published source yet, so we skip them.
      - Everything else must have a non-empty source_ids value.
    """
    problems = []
    for _, row in df.iterrows():
        is_gap = str(row["confidence"]).strip() == "Gap"
        has_source = str(row["source_ids"]).strip() != ""

        if not is_gap and not has_source:
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
    # 3. Count total input rows, then separate intentional gaps from sourced rows.
    #    "Gap" rows are expected — they flag survey items we still need to collect.
    #    Every non-Gap row must have a source_ids entry.
    # ---------------------------------------------------------------------------
    total_rows     = len(model_df)
    gap_rows       = model_df[model_df["confidence"] == "Gap"]
    sourced_rows   = model_df[model_df["confidence"] != "Gap"]
    problems       = audit_model_inputs(model_df)

    print(f"\n  Total input rows   : {total_rows}")
    print(f"  Sourced rows       : {len(sourced_rows)}")
    print(f"  Intentional gaps   : {len(gap_rows)}  (confidence == 'Gap')")

    # ---------------------------------------------------------------------------
    # 4. List the intentional Gap rows so the user knows what still needs
    #    primary research or survey data.
    # ---------------------------------------------------------------------------
    print("\nGap rows (survey items — no published source yet):")
    for _, row in gap_rows.iterrows():
        print(f"    {row['parameter']:<40s}  vehicle={row['vehicle']:<8s}  notes={row['notes']}")

    # ---------------------------------------------------------------------------
    # 5. Flag any non-Gap rows that are ALSO missing a source — these are
    #    genuine data-quality issues that need to be fixed before modelling.
    # ---------------------------------------------------------------------------
    print()
    if problems:
        print(f"WARNING: {len(problems)} non-Gap row(s) are missing source_ids:")
        for p in problems:
            print(f"    parameter={p['parameter']:<40s}  vehicle={p['vehicle']:<8s}  confidence={p['confidence']}")
    else:
        print("OK: all non-Gap rows have at least one source_id.")

    print()


if __name__ == "__main__":
    main()
