# Documentation and Data Index

Research files for *Stuck in the Queue: Nigeria's CNG Transition*. As of 1 October 2026.

## docs/

| File | Contents |
|---|---|
| `sources.md` | Source log: 45 sources (S01–S47) with reliability ratings (H/M/L) |
| `data_conflicts.md` | 14 discrepancies between sources and how each is treated |
| `survey_method.md` | How the driver survey was designed, fielded and cleaned |
| `model_inputs.md` | Model inputs, fuel-saving scenarios and cost model structure |
| `notes/` | Summaries of core readings: NESG report, Pi-CNG official claims, Pakistan case, Delhi case |

## data/raw/

| File | Contents |
|---|---|
| `model_inputs.csv` | 28 model parameters with low/mid/high values, source IDs and confidence |
| `petrol_prices_nbs.csv` | NBS monthly average petrol prices, Jun 2024 – May 2026 |
| `lagos_cng_stations.csv` | 22 named Lagos CNG stations with operator, status and confidence |
| `lagos_conversion_centres.csv` | The six Pi-CNG-approved conversion centres in Lagos |
| `conversion_prices.csv` | 14 published conversion price points by vehicle type |
| `survey_responses.csv` | Driver survey Google Form export, 25 responses (local only, not in the repository) |

Files in `data/raw/` are kept as originally compiled. Cleaned data is written to `data/processed/`.

The raw survey export (`data/raw/survey_responses.csv`) is kept locally and is not published. Only the anonymised clean file, `data/processed/survey_clean.csv` (no submission timestamps), is published.
