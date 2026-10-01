# Start Here: Project Files Package (as of 1 Oct 2026)

This package contains **all files so far** (week 2 desk research + the desk tasks). It replaces the earlier `week2_desk_research.zip`.

## How to add it to your repo

Copy the **contents** of this folder (`docs/`, `data/`, this file) into your `nigeria-cng-policy` repo folder, replacing any older copies. Don't copy the outer folder itself, or you'll end up with a folder inside a folder.

## What's inside

```
docs/
├── sources.md              46 sources, each with an ID (S01–S46) and reliability rating
├── data_conflicts.md       13 places where sources disagree, and how we handle each
├── model_inputs.md         The model's inputs explained + the formula for week 3
├── project_plan.md         Updated 8-week plan (desk + online survey + Monte Carlo + FOI)
├── foi_request_picng.md    Freedom of Information letter to Pi-CNG, ready to fill in and send
└── notes/                  Summaries: NESG report, Pi-CNG claims, Pakistan, Delhi

data/raw/
├── model_inputs.csv            28 model inputs with low/mid/high values and source IDs
├── petrol_prices_nbs.csv       NBS monthly petrol prices, Jun 2024 – May 2026 (15 months)
├── lagos_cng_stations.csv      22 named Lagos CNG stations with confidence ratings (coordinates added in week 4)
├── lagos_conversion_centres.csv  The 6 Pi-CNG-approved conversion centres in Lagos, with addresses
└── conversion_prices.csv       14 published conversion price points by vehicle type
```

## Rule

Files in `data/raw/` are the original record: never edit them by hand. Code reads them and writes cleaned versions to `data/processed/`.
