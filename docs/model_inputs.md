# Model Inputs

Data file: `data/raw/model_inputs.csv` · Petrol series: `data/raw/petrol_prices_nbs.csv` · As of 1 Oct 2026

## The headline inputs

| Input | Low | Mid | High | Confidence |
|---|---|---|---|---|
| Petrol price (₦/L, national) | 1,051 | 1,400 | 1,596 | High |
| CNG price (₦/scm, cars) | 230 | 318 | 380 | Medium |
| Conversion cost (₦, car) | 300,000 | 1,300,000 | 1,700,000 | Medium |
| Conversion cost (₦, keke) | 100,000 | — | 650,000 | Low |
| Lagos CNG stations (count) | 7 confirmed | 18 | 22 named | Low |
| Loan interest (% / yr) | 15 | 17.5 | 20 | Medium |
| Queue time per refuel (hrs) | 1.5 | 4 | 6 | Medium |
| Distance driven per day (km) | — | — | — | **Gap: survey** |
| Keke / danfo daily earnings (₦) | — | — | — | **Gap: survey** |

## A key calibration finding

Two independent sources imply that **1 scm of CNG takes a car roughly as far as 1 litre of petrol**:

- Dataphyte (S20): about 10.67 km/scm vs 9–11 km/L.
- The official cost benchmark (S05) implies about 6.8 km/scm (₦5,600 ÷ ₦380 per 100km) vs about 6.5 km/L (₦21,450 ÷ ₦1,400). The absolute level is lower, but the ratio is the same.

So the fuel saving share is roughly **1 − (CNG price ÷ petrol price)**:

| Scenario | CNG ₦/scm | Petrol ₦/L | Fuel saving |
|---|---|---|---|
| Worst (Lagos Feb 2026 petrol, official CNG) | 380 | 967 | 61% |
| Official CNG, early-2026 petrol | 380 | 1,051 | 64% |
| Official CNG, current petrol | 380 | 1,400 | 73% |
| Current reported prices | 318 | 1,400 | 77% |
| Best (cheapest CNG, May 2026 peak petrol) | 230 | 1,596 | 86% |

The fuel saving is large in every scenario, which sharpens the research question: if CNG cuts fuel costs by 60–86%, **why is uptake slow?** Queue time and upfront conversion cost are the explanations the model tests.

## Cost model structure

Daily net benefit of CNG for a driver:

```
fuel saving per day  = km/day × (petrol price ÷ km/L − CNG price ÷ km/scm)
queue cost per day   = refuels/day × queue hours × net earnings per hour
loan cost per day    = conversion cost repayment (incl. interest) ÷ working days
net benefit per day  = fuel saving − queue cost − loan cost
```

**Break-even queue time** = the queue hours at which net benefit hits zero. This is the study's headline metric.

## Data gaps addressed by the driver survey

1. Distance driven per day (keke, danfo, ride-hailing)
2. Net earnings per hour (after owner remittance, commission)
3. Refuels per day for CNG vehicles, and actual queue times at Lagos stations
4. Danfo fuel use (km/L)
5. Whether the free (commercial) and 50% (ride-hailing) conversion subsidies still apply in 2026

Lagos conversion prices are drawn from published centre quotes (`conversion_prices.csv`).
