# Project: Stuck in the Queue — Nigeria's CNG Transition
Policy analysis portfolio project by Malik.

## Central question
At what queue time and petrol-CNG price gap does CNG conversion stop paying off
for Nigerian commercial drivers, and which policy levers restore the incentive?

## Components
1. Driver total-cost-of-ownership model (keke, danfo/bus, ride-hailing car)
2. Station access mapping (vehicles per station, Lagos & Abuja)
3. Pakistan CNG boom-bust comparative lesson
4. Policy options appraisal + costed recommendations

## Rules
- Never modify source exports in data/raw/ (survey_responses.csv, petrol_prices_nbs.csv, lagos_cng_stations.csv, lagos_conversion_centres.csv, conversion_prices.csv). model_inputs.csv is a curated parameter table: it may be edited, but every change must keep a source ID or an Assumption label in its row and be described in the commit message.
- Every figure/number must trace to docs/sources.md
- Explain code choices — I'm learning, not just shipping
- Python, pandas, plotly; keep code readable and commented
