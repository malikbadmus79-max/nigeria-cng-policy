# Data Conflicts Log

Discrepancies found during desk research, and how each is treated in the analysis.

| ID | Issue | Values | Sources | Treatment |
|---|---|---|---|---|
| C1 | Vehicles converted vs kits deployed | 120,000+ vehicles vs 93,845 kits (same report) | S01 | Report both; use 93,845 as the conservative figure; Pi-CNG has not published its definition of "converted" |
| C2 | "12% adoption" is mislabelled | 12% matches 120,000 ÷ 1,000,000 target, i.e. progress to target, not market penetration | S03, S01 | Described in this study as "12% of the 2027 target" |
| C3 | States with active CNG stations | 28 vs 23 states (both with 90 stations) | S01, S11 | Cited as "23–28 states" pending an official station list |
| C4 | Fuel efficiency level | 10.67 km/scm (Dataphyte) vs ~6.8 km/scm implied by official benchmark | S20, S05 | The CNG:petrol ratio is consistent (~1:1), so savings modelled as a ratio; absolute km/day to be tested with survey data |
| C5 | Implausible daily saving | "₦70,330 daily saving for a CNG sedan" vs ride-hailing fuel spend of ~₦20,000/day | S11, S21 | Excluded as a likely error |
| C6 | Conversion cost | ₦300k – ₦1.5m across sources; free for commercial vehicles (2024) | S02, S17, S20, S05 | Low/mid/high scenarios; published Lagos quotes used (see C10) |
| C7 | CNG price | ₦230, ₦318, ₦380, up to ₦500+/scm | S13, S11, S10 | Modelled as scenarios; survey records prices paid |
| C8 | Technicians trained | 7,700 (Pi-CNG) vs 8,000 vs 500+ (NESG cites both) | S01, S02 | Not central to the model; noted only |
| C9 | Pakistan station counts | Arab News figures (e.g. "22,000" Punjab stations) inconsistent with 3,329 national stations in 2011 | S26, S23 | Arab News cited for mechanism only; Dawn/OGRA used for counts |
| C10 | Official vs market conversion cost | Official ₦300k–600k (2023) vs Lagos centre quotes ₦1m–1.7m (2024), up to ₦2.5m | S42, S40, S41 | Published Lagos quotes used in the model; official figure cited as the policy assumption |
| C11 | Lagos petrol price | NNPC Lagos pump ₦837 (Mar 2026) vs NBS Lagos average ₦966.61 (Feb 2026) | S33, S14 | Pump price at one retailer ≠ survey average; NBS used, NNPC shown as the low case |
| C12 | Station status | 4 of 6 NNPC mobile units were "due by end Jan 2025"; no confirmation found that they opened | S35, S36 | Marked "Planned"; excluded from the confirmed count |
| C13 | Lagos station total | IOGC claims a 15-station network but only 11 sites are named | S37 | Named sites only counted |
| C14 | Keke conversion: paid vs free | ₦100k–200k official estimate and ₦650k reported (paid) vs free for association members under the Pi-CNG drive (free kits for commercial vehicles via associations; free for NURTW/RTEAN members) | S43, S04, S17, S40 | Model uses the paid range (₦100k–650k, mid ₦375k) as the loan-financed case; free conversion (`conversion_cost_after_subsidy` = 0) kept for the policy appraisal; 2026 status unverified (survey item) |
