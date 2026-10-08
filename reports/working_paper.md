# Stuck in the Queue: Why Lagos Drivers Are Slow to Switch to CNG, and What Would Help

Malik Badmus · Working paper, first draft · October 2026

---

## 1. Summary

Nigeria's Presidential Initiative on Compressed Natural Gas and Electric Vehicles (Pi-CNG & EV) (S01) aims to move commercial vehicles from petrol to compressed natural gas (CNG). On fuel prices alone, the case for switching is strong. Adoption has nonetheless been slow. This paper asks at what queue time and petrol–CNG price gap conversion stops paying off for Lagos commercial drivers, and which policy levers would restore the incentive.

The analysis combines four sources of evidence. A desk review of 44 published sources provides prices, conversion costs, loan terms and station lists. A survey of 25 Lagos commercial drivers, fielded in October 2026, provides earnings, fuel spend and queue times. A daily cost model is run for fixed scenarios, then repeated 10,000 times in a Monte Carlo simulation that draws prices, drivers, queues and loan terms at random. A map places the 22 named CNG sites in Lagos. Five policy options are then appraised on simulated impact, cost, speed, feasibility and evidence.

Three findings stand out. First, CNG saves 61–86% on fuel across the price scenarios tested (notebook 01). Second, queue time, not fuel price or kit cost, decides whether conversion pays. In the simulation, CNG pays in 62% of draws at market kit prices. That figure rises to 98% if daily queuing is held to one hour and falls to 16% at four hours (notebook 06). Queue time has a rank correlation of −0.68 with net benefit, more than twice that of any other input. Third, refuelling access in Lagos is thin. Only 6 of 22 named sites are confirmed operational, and 10 of 12 surveyed petrol drivers cite the lack of a nearby station as a barrier (notebooks 04 and 05).

The top recommendation is to raise capacity at the busiest existing stations so that daily queuing stays near one hour. Station operators would lead, with support from Pi-CNG and the Midstream and Downstream Gas Infrastructure Fund (MDGIF) (S37). This option ranks first under every weighting tested (notebook 07). The survey is small and non-random, so the results are indicative rather than representative.

## 2. Introduction

Petrol prices in Nigeria have risen steeply since the removal of the petrol subsidy in May 2023 (S03). The national average pump price was ₦750.17 per litre in June 2024 (S30). It reached ₦1,596.25 in May 2026, a 55% rise on a year earlier (S16). The average for the first half of 2026 was ₦1,300.33 per litre (S03). Nigerians are reported to have spent ₦58.6tn on petrol since May 2023 (S03). For commercial drivers, these increases bear directly on daily income and fares.

The federal response has centred on CNG. The Presidential CNG Initiative, now Pi-CNG & EV (S01), promotes conversion of petrol vehicles to CNG. It supports conversion centres, refuelling stations, free or discounted conversion kits, and financing. The stated goal is 1 million vehicles by 2027 (S07). In its 2026 term report, the programme says it has converted more than 120,000 vehicles, deployed 93,845 kits, and supported 90 stations in 28 states (S01). Another source places the same 90 stations in 23 states (S11; conflict C3). Commercial vehicles were offered free kits through transport associations, and ride-hailing and private vehicles a 50% discount (S17). A ₦10bn credit scheme run by the Ministry of Finance Incorporated (MOFI) and the Nigerian Consumer Credit Corporation (CREDICORP) lends for conversions at 15–20% interest over one to three years (S18). In 2026 the programme announced a 100,000 Conversion Kit Programme and "Convert Now, Pay Small Small" financing (S08). The Presidency has said that 1,000 stations have been ordered and that CNG will cut transport fares from 1 October 2026 (S09).

Progress remains small against the target. The programme's own figure of 120,000 vehicles is about 12% of the 2027 goal (S01, S03; conflict C2). The figure is also uncertain, since it differs from the number of kits deployed (conflict C1). An independent review by the Nigerian Economic Summit Group (NESG) found 50,000 or more vehicles converted by mid-2025. It identified thin refuelling infrastructure, high upfront cost and uneven access as the main constraints (S02). The programme's leadership has instead attributed slow adoption mainly to fears about cylinder safety (S05). These fears have some basis. A refuelling explosion occurred in Benin City in October 2024 (S22). The Standards Organisation of Nigeria has reported weak enforcement and few cylinder test facilities (S06).

The gap between a large fuel saving and slow adoption is the starting point for this paper. If CNG is so much cheaper per kilometre, something else must be offsetting the saving for many drivers. Two broad explanations are available. One is demand-side: drivers are unaware, wary or unconvinced. The other is supply-side: refuelling is hard to reach, queues are long, and the time lost costs more than the fuel saved. This paper tests the supply-side explanation directly, using Lagos as the case. It does not test the safety or awareness explanation in detail.

## 3. Research question and hypothesis

The central question is at what queue time and petrol–CNG price gap CNG conversion stops paying off for Nigerian commercial drivers, and which policy levers restore the incentive.

The working hypothesis is that refuelling access, measured as time spent queuing for gas, is the main reason conversion fails to pay for many commercial drivers. Fuel prices and conversion cost play a smaller part. If the hypothesis holds, three things should follow. The cost model should show net benefit falling sharply as queue time rises. Surveyed drivers who have not converted should cite station access and queues more often than cost. Policies that shorten queues should improve the economics of conversion more than policies that make kits or loans cheaper.

The alternative view, that perception and safety fears are the main barrier (S05), is not ruled out by this design. The survey asked petrol drivers whether safety worries were a barrier, which gives a partial test.

## 4. Data and methods

### 4.1 Desk sources

The source log, `docs/sources.md`, holds 44 published sources and the driver survey (S47). Two ID numbers in the S01–S47 range are unused. Each source was rated for reliability: H for official statistics or peer-reviewed work, M for programme claims, think-tank reports or established outlets quoting officials, and L for single news stories or unclear methods. The sources cover programme claims, petrol and CNG prices, conversion costs, loan terms, Lagos station lists, and two comparative cases. Petrol prices come from National Bureau of Statistics (NBS) releases as reported in the press (S14, S15, S16, S30, S31, S32). The NBS series has gaps: 15 of the 24 months from June 2024 to May 2026 are observed (notebook 01).

Model parameters are held in `data/raw/model_inputs.csv` with low, mid and high values and a source ID or an "Assumption" label for each row. Where sources disagreed, the disagreement was logged in `docs/data_conflicts.md` with the treatment chosen. The appendix lists all 14 conflicts.

### 4.2 Driver survey

The driver survey (S47) is described in `docs/survey_method.md`. It was a Google Form, generated by a script so that wording and order are fixed. The first question asked for consent; respondents who declined were routed to the end of the form. The form then branched by fuel type. Petrol-only drivers were asked about daily petrol spend, barriers to conversion, and whether they would convert if a station were within 10 minutes or if conversion were free. Drivers of CNG-only and bi-fuel vehicles were asked about conversion cost and payment, current CNG spend, recalled petrol spend before conversion, refuels per day, queue time per refuel, shortages and perceived savings. No names or phone numbers were collected.

The researcher approached drivers in person at CNG stations and car parks in Lagos between 4 and 7 October 2026. Ten drivers completed the form on their own phones. For 15 drivers who could not, the researcher asked the questions in person, noted the answers, and entered them on the evening of 7 October 2026. The sample is 25 drivers: 12 petrol-only and 13 CNG or bi-fuel. Queue times were collected in bands and converted to hours at band midpoints. Five responses (R09, R15, R17, R22 and R25) were flagged because fuel spend was at least equal to gross daily earnings, or gross earnings were below ₦20,000. All five are petrol drivers. Their original values were kept, but they are excluded from every money figure. This leaves 20 unflagged drivers for money figures: 13 CNG and 7 petrol (notebook 04).

### 4.3 Cost model

The daily cost model (`src/cost_model.py`) compares a driver's position on CNG with their position on petrol, per working day. It has four parts.

```
CNG cost per day   = petrol spend × (CNG price ÷ petrol price) ÷ efficiency ratio
fuel saving        = petrol spend − CNG cost per day
queue cost         = refuels per day × queue hours per refuel × earnings per hour
monthly payment    = conversion cost × r ÷ (1 − (1 + r)^−n),  r = annual rate ÷ 12, n = months
loan cost          = monthly payment × 12 ÷ working days per year
net benefit        = fuel saving − queue cost − loan cost
break-even queue   = (fuel saving − loan cost) ÷ (refuels per day × earnings per hour)
```

The efficiency ratio is the distance covered per standard cubic metre (scm) of CNG divided by the distance per litre of petrol. Two sources imply that the ratio is close to one, although they disagree on the absolute level (S20, S05; conflict C4). The model therefore uses a ratio of 1.0, so the fuel saving share is approximately one minus the ratio of the CNG price to the petrol price (`docs/model_inputs.md`). Queue cost treats each hour in a queue as an hour of lost earnings. The break-even queue time is the queue length at which net benefit falls to zero. It is the main metric of the study.

Notebook 02 runs the model for a ride-hailing car and a keke (tricycle) under three scenarios. In the CNG-favourable scenario, every input is at the end of its range that helps CNG. In the CNG-unfavourable scenario, every input is at the end that hurts it. The central scenario uses mid values. Earnings per hour were unknown when notebook 02 was written, so they are tested over a range of ₦1,000 to ₦5,000 per hour. Daily petrol spend comes from published reports (S19, S21). It is rescaled from about ₦1,000 per litre to each scenario's petrol price, assuming the same litres per day. Notebook 03 then runs the same model on each surveyed CNG driver's own figures.

### 4.4 Monte Carlo simulation

The fixed scenarios put every input at its extreme at once, which is unlikely in practice. The Monte Carlo simulation (`src/monte_carlo.py`, notebook 06) instead draws each input at random and repeats the calculation 10,000 times. Petrol price, CNG price, conversion cost, interest rate and loan tenor are drawn from triangular distributions defined by the low, mid and high values in `model_inputs.csv`. Each draw also picks one of the 20 unflagged surveyed drivers at random, with replacement (a bootstrap), taking that driver's petrol spend, earnings per hour, working days and vehicle type together. A daily queue time is drawn separately from the 13 CNG users' reported values. Petrol spend is rescaled from ₦1,400 per litre, the price around the survey date (S11), to the drawn petrol price.

Two cases are run. In the market case the driver repays a conversion loan; in the free case loan cost is zero. Danfo and taxi drivers use the car conversion price, because `model_inputs.csv` has no separate row for them. All runs use the same random seed and draw values in the same order, so the market and free cases differ only in the loan. Sensitivity is measured by the Spearman rank correlation between each drawn input and net benefit.

### 4.5 Station mapping

The 22 named CNG sites in Lagos (`data/raw/lagos_cng_stations.csv`, from S34–S37 and S39) were geocoded with OpenStreetMap's Nominatim service (`src/geocode_stations.py`). Each site's name and area were searched first. If that failed, only the area was searched, and the site was placed at the area centre. Sites were grouped by status: confirmed operational from two sources, commissioned but not confirmed to be selling gas, and planned or unconfirmed. A 3 km circle was drawn around each confirmed or commissioned site as a rough, illustrative indication of nearby access (notebook 05).

### 4.6 Policy appraisal

Five options were appraised (notebook 07, `docs/policy_options.csv`). Each was simulated by re-running the Monte Carlo with one input changed: daily queue time halved; daily queue time capped at one hour; free conversion; loan interest fixed at 5%; and CNG price fixed at its mid value of ₦318 per scm. The change in the probability that CNG pays was converted to an impact score of 1 to 5 using fixed bands. Cost, speed, feasibility and evidence were each scored 1 to 5, with a written rationale for each score. Most of these scores are the researcher's judgement and are labelled as such. The cost of free conversion and part of the cost of cheaper loans were calculated from sourced inputs. Scores were combined with weights of 35% for impact, 20% for cost and 15% each for speed, feasibility and evidence. The ranking was then tested under equal weights and under a 50% weight on impact.

## 5. Findings

### 5.1 Fuel prices: CNG saves 61–86% on fuel

On fuel price alone, CNG is much cheaper than petrol in every scenario tested. At the May 2026 national average petrol price of ₦1,596.25 per litre (S16), CNG at ₦230, ₦318 or ₦380 per scm (S13, S11, S10) is 86%, 80% or 76% cheaper per unit (notebook 01). Since one scm covers about the same distance as one litre (conflict C4), these shares approximate the saving per kilometre. Across the wider set of price combinations in `docs/model_inputs.md`, the saving ranges from 61% to 86%, as shown below. The chart `outputs/figures/petrol_vs_cng.html` shows the petrol series against the three CNG prices.

| Price combination | CNG (₦/scm) | Petrol (₦/L) | Fuel saving |
|---|---|---|---|
| Lagos petrol, February 2026, official CNG | 380 | 967 | 61% |
| Official CNG, early-2026 petrol | 380 | 1,051 | 64% |
| Official CNG, current petrol | 380 | 1,400 | 73% |
| Current reported prices | 318 | 1,400 | 77% |
| Cheapest CNG, May 2026 petrol | 230 | 1,596 | 86% |

The CNG price has not been stable. In September 2025 the retail price rose from ₦230 to ₦380 per scm overnight (S12), and station prices have ranged up to ₦500 or more (S13; conflict C7). Even so, the gap with petrol is wide enough that price alone does not explain slow adoption.

### 5.2 Driver economics: scenarios and break-even

Notebook 02 applies the cost model to a ride-hailing car and a keke. The table below shows net benefit per working day under each scenario at three earnings levels. In the central scenario, the car saves ₦21,640 a day on fuel and repays ₦2,484 a day on a ₦1.3m conversion loan. The keke saves ₦16,230 and repays ₦717 on a ₦375,000 kit.

| Vehicle | Scenario | ₦2,000/hr | ₦3,000/hr | ₦4,000/hr |
|---|---|---|---|---|
| Ride-hailing car | CNG-favourable | 23,920 | 22,420 | 20,920 |
| Ride-hailing car | Central | 11,156 | 7,156 | 3,156 |
| Ride-hailing car | CNG-unfavourable | −4,637 | −10,637 | −16,637 |
| Keke | CNG-favourable | 17,357 | 15,857 | 14,357 |
| Keke | Central | 7,513 | 3,513 | −487 |
| Keke | CNG-unfavourable | −4,251 | −10,251 | −16,251 |

Net benefit in ₦ per working day. Queue time is 1.5, 4 and 6 hours per refuel in the three scenarios, with one refuel a day (notebook 02).

The three scenarios give three different answers. In the favourable scenario, CNG pays comfortably for both vehicles at every earnings level tested. In the unfavourable scenario, with a six-hour queue and a one-year loan on an expensive kit, it loses money for both at every earnings level shown. The central scenario lies between, and its result depends on earnings. At ₦3,000 per hour, the break-even queue time is 6.4 hours per refuel for the car and 5.2 hours for the keke. At ₦4,000 per hour, it falls to 4.8 and 3.9 hours. The keke then loses about ₦500 a day at the central four-hour queue. The chart `outputs/figures/break_even_queue.html` shows break-even queue time against earnings for the central scenario. A band marks reported queue times of 1.5 hours (S02) to 6 hours (S04). The car's break-even enters that band from ₦3,500 per hour and the keke's from ₦3,000 per hour.

The main lesson of the scenarios is that the fuel saving is large in all three, so the result turns on queue time, earnings and loan terms. Earnings per hour decide the cost of each hour spent queuing, and in notebook 02 they were an assumed range. The survey was designed to fill this gap.

### 5.3 What surveyed drivers report

#### CNG drivers

The 13 CNG drivers in the survey report large fuel savings and moderate queues (notebook 03). For each driver, the fuel saving is recalled petrol spend before conversion minus current CNG spend. The median saving is ₦36,000 a day. The median fuel saving share is 81.7%, slightly above the model's central 77.3%. These drivers refuel twice a day at the median and queue for 0.75 hours each time, or 2.25 hours a day. They earn a median of about ₦11,200 per hour after fuel. That is well above the ₦1,000–5,000 range assumed in notebook 02, though the survey figure does not deduct owner remittance or app commission.

Valuing each driver's queue time at their own earnings gives a median queue cost of about ₦21,000 a day and a median net benefit of about ₦16,700 a day. Nine of the 13 drivers come out ahead. Their median break-even is 2.9 hours of queuing a day, against a median actual queue of 2.25 hours. The margin for the typical driver is therefore under an hour. Four drivers lose money: R01 and R11 (danfo), R07 (ride-hailing) and R14, the one keke CNG user (three keke drivers in total). Three of them queue for three hours a day. The fourth, R07, earns about ₦23,900 an hour, so time in a queue is especially costly. R14, the one keke CNG user (three keke drivers in total), has the smallest fuel saving in the sample, at ₦5,800 a day. The chart `outputs/figures/survey_break_even.html` plots each driver's actual daily queue time against their break-even.

| Measure | Survey median (n = 13) | Model central value |
|---|---|---|
| Earnings per hour (₦) | 11,215 | 1,000–5,000 (range) |
| Refuels per day | 2 | 1 |
| Queue hours per refuel | 0.75 | 4 |
| Daily queue hours | 2.25 | 4 |
| Working days per year | 364 | 312 |
| Fuel saving | 81.7% | 77.3% |

Survey medians for unflagged CNG users against the model's central values (notebook 03).

Twelve of the 13 CNG drivers converted through the free government programme, and the other driver's owner paid. Loan cost is therefore zero for this sample. Notebook 03 asks what would change if each driver had paid ₦1.3m on a 17.5% two-year loan (S40, S18). The repayment would be about ₦2,100–2,500 per working day. The same nine drivers would still come out ahead, and the median net benefit would fall to about ₦14,200. An extra hour in the queue, by contrast, costs the median driver about ₦11,200. For these drivers, queue time matters far more than the price of the kit.

#### Petrol drivers

The 12 petrol drivers were asked what stops them converting, and could tick more than one answer (notebook 04). Ten cited the lack of a CNG station near where they work, nine said queues at CNG stations are too long, and seven said conversion is too expensive. One driver was worried about safety and one did not own the vehicle. The median driver ticked 2.5 barriers. The chart `outputs/figures/barriers.html` shows these counts.

| Barrier | Drivers (of 12) | Share |
|---|---|---|
| No CNG station near where I work | 10 | 83% |
| Queues at CNG stations are too long | 9 | 75% |
| Conversion is too expensive | 7 | 58% |
| Worried about safety | 1 | 8% |
| The vehicle is not mine | 1 | 8% |

Stated interest in converting is high. Ten of the 12 said they would convert either if a station were within 10 minutes or if conversion were free. One more would convert if it were free but was unsure about a nearby station. One would convert under neither condition. Because almost every driver said yes to both, the survey cannot separate the effect of the two levers.

Among unflagged drivers, petrol and CNG drivers earn similar amounts per day: a median of ₦120,000 for both groups. Petrol drivers report longer days, 12 hours against 9, and so earn a little less per hour: ₦10,000 against about ₦11,500. Only seven petrol drivers are unflagged, so these differences may reflect chance.

Notebook 04 also estimates what the seven unflagged petrol drivers would gain from a free conversion. The estimate applies the CNG users' median fuel saving share (81.7%) and median daily queue (2.25 hours) to each petrol driver. This is an assumption, since these drivers have never used CNG. On that basis, four of the seven would come out ahead, with a median net benefit of about ₦3,500 a day. Two of the three who would lose spend relatively little on petrol (R16 and R21). The third (R18) earns enough per hour that queue time is costly.

The safety barrier was cited by only one of 12 petrol drivers. This does not show that safety concerns are unimportant more widely, but it gives little support in this sample to the view that fear is the main barrier (S05).

### 5.4 Refuelling access in Lagos

The station list contains 22 named sites (notebook 05). Only six are confirmed operational by two sources. These six are four fixed stations run by NNPC Retail with NIPCO and two NNPC mobile refuelling units (S34, S35, S36). A further 12 have been commissioned but are not confirmed to be selling gas. Eleven of these are stations in the Lagos State IBILE (IOGC) network, all from a single source, and one is the Portland Gas mother station at Ojota (S37). The remaining four are NNPC mobile units that were due to open by the end of January 2025, with no confirmation found that they did (S35; conflict C12). The IOGC network is described as 15 stations, but only 11 sites are named (S37; conflict C13).

| Status | Sites | Operator |
|---|---|---|
| Confirmed operational (2 sources) | 6 | NNPC Retail / NIPCO (4), NNPC Retail (2) |
| Commissioned, operation not confirmed | 12 | IBILE (11), Portland Gas (1) |
| Planned or unconfirmed | 4 | NNPC Retail (4) |

Lagos CNG sites by status and operator (notebook 05).

The six confirmed points are concentrated in a few places. Five are in the central and northern mainland, in Ikeja, Mushin, Shomolu, Agege and Apapa, and one is at Sangotedo on the Lekki–Epe corridor (notebook 05). Alimosho, Ikorodu, Badagry, Ibeju-Lekki and Lagos Island have no confirmed site on the list (notebook 05). The map `outputs/figures/lagos_station_map.html` shows all 22 sites with illustrative 3 km circles. On those circles, most of the state lies outside reach of a confirmed site. If the commissioned IBILE stations are operating, coverage looks considerably better, especially in Alimosho, Kosofe and the Ajah–Ikota area.

This pattern is consistent with the survey finding that 10 of 12 petrol drivers cite the lack of a nearby station. The survey did not record where drivers work, so individual drivers cannot be matched to the map. Positions are also approximate: 15 of the 22 sites could only be placed at the centre of their neighbourhood.

### 5.5 Uncertainty: Monte Carlo results and sensitivity

The Monte Carlo simulation combines the uncertainty in prices, drivers, queues and loan terms (notebook 06). At market kit prices on a loan, CNG pays in 62% of 10,000 draws, with a median net benefit of about ₦4,400 per working day. The middle 80% of outcomes runs from a loss of about ₦13,700 to a gain of about ₦21,900 a day. With a free conversion, the probability rises only to 66%, with a median of about ₦6,100. The loan repayment has a median of about ₦1,800 per working day, which is small next to fuel savings and queue costs. The chart `outputs/figures/monte_carlo_net_benefit.html` shows the full distribution for the market case.

| Group | Respondents | P(CNG pays), market | Median ₦/day, market | P(CNG pays), free |
|---|---|---|---|---|
| All drivers | 20 | 62% | 4,440 | 66% |
| Ride-hailing | 8 | 71% | 12,299 | 74% |
| Danfo | 8 | 65% | 5,061 | 70% |
| Keke | 3 | 39% | −2,763 | 41% |
| Taxi | 1 | 30% | −8,515 | 35% |

Monte Carlo results, 10,000 draws per case (notebook 06). Keke and taxi results rest on three and one respondents and are not treated as findings.

These probabilities are lower than in notebook 03, where 9 of 13 CNG drivers came out ahead. In the simulation, each driver is given a queue time drawn at random from all CNG users. This removes any real link between a driver and their queue, such as a high earner who refuels where queues are short. The simulation also calculates fuel saving from prices rather than from each driver's reported CNG spend.

Queue time is the input that moves net benefit most. Its Spearman correlation with net benefit is −0.68. The next strongest are the driver's petrol spend (+0.30) and earnings per hour (−0.22), followed by the petrol price (+0.18). CNG price, interest rate, working days and loan tenor each have correlations of 0.05 or less in absolute value. Conversion cost shows a small positive correlation (+0.11). This reflects vehicle type: keke drivers have both cheaper kits and smaller fuel savings. Within ride-hailing or danfo draws alone, the correlation is slightly negative (−0.035 and −0.051). The chart `outputs/figures/monte_carlo_sensitivity.html` ranks all nine inputs.

When daily queue time is held fixed, the probability that CNG pays at market prices is 98% at one hour, 62% at two hours, 29% at three hours and 16% at four hours. Moving from a three-hour to a one-hour daily queue raises the probability by about 70 percentage points. Making the conversion free raises it by about 4 points. These results answer the first half of the research question. For drivers like those surveyed, conversion pays in most cases at up to about two hours of queuing a day and in a minority of cases beyond three hours. Within the ranges observed, the petrol–CNG price gap matters much less than queue time.

| Daily queue time | P(CNG pays), market | P(CNG pays), free |
|---|---|---|
| 1 hour | 98% | 99% |
| 2 hours | 62% | 66% |
| 3 hours | 29% | 32% |
| 4 hours | 16% | 18% |
| As surveyed (drawn) | 62% | 66% |

Probability that CNG pays with daily queue time held fixed (notebook 06).

## 6. Lessons from Pakistan and Delhi

Pakistan shows how CNG adoption can outrun gas supply. By 2011 it had 2.5 million CNG vehicles, 3,329 stations, and about 21% of its vehicles running on CNG (S23). From February 2008 the government stopped issuing new station licences (S24). Shortages followed declining local gas production, and in shortages gas was diverted to households (S25, S26). All CNG stations in Sindh and Balochistan were shut from 1 December 2021 to 15 February 2022 (S25), and winter closures affected Punjab and Islamabad (S26). CNG use fell 83%, from 325 to 55 million cubic feet per day between FY2011–12 and FY2024–25 (S24). The lesson for Nigeria is that cheap gas can attract vehicles faster than supply can serve them. In Pakistan, transport lost its gas when supply ran short (S25, S26). In this study's interpretation, policy reversals such as the 2008 licence ban (S24) and the later supply cuts weakened the confidence of station owners and drivers. Nigeria's overnight CNG price rise in September 2025 (S12) carries a similar risk to trust.

Delhi faced the same problem and responded by expanding supply. In July 1998, India's Supreme Court ordered Delhi's buses, taxis and auto-rickshaws to switch to CNG (S27). The early rollout ran into the problem now seen in Lagos. By the time of the CRRI account, 42,756 vehicles had been converted but the 87 stations could not meet demand. Supply fell 32% short and queues formed on the roads (S27). By 2003, stations had risen from 30 to 112 and the gas allocation from 0.48 to 2 million standard cubic metres per day (MMSCMD), and about 80,000 vehicles ran on CNG (S28). Bus conversions measurably reduced PM10, carbon monoxide and sulphur dioxide, though auto-rickshaw conversions did less (S29).

In this study's interpretation, the two cases point the same way as the Lagos findings: queues signal that supply has not kept pace with conversions, not that the fuel is unsuitable. Delhi expanded stations and gas allocation together (S28). Pakistan stopped licensing new stations and later cut gas to transport (S24, S25). Delhi's mandate applied to defined commercial fleets of buses, taxis and auto-rickshaws (S27), which is relevant to Nigeria's focus on commercial vehicles such as danfo and keke.

## 7. Policy options and recommendations

### 7.1 Simulated impact

Each option was simulated against the same 10,000 draws as the baseline (notebook 07). The two queue options have by far the largest effect. Halving daily queue time raises the probability that CNG pays from 62% to 92%, and capping daily queuing at one hour raises it to 98%. Both cut the average daily queue to about an hour, from 1.98 hours to 0.99 and 0.92 hours. The cap scores higher because it also removes the longest queues, which are the ones that turn a gain into a loss. Free conversion adds about 4 percentage points, a 5% loan rate under 1 point, and a fixed CNG price nothing. The chart `outputs/figures/policy_options_impact.html` compares the options.

| Option | P(CNG pays) | Change from baseline | Median net benefit (₦/day) |
|---|---|---|---|
| Baseline | 61.8% | – | 4,440 |
| 1. More refuelling points (queues halved) | 91.5% | +29.7 pts | 14,426 |
| 2. More capacity at existing stations (queue capped at 1 hour) | 98.2% | +36.4 pts | 15,125 |
| 3. Free conversion | 65.5% | +3.8 pts | 6,141 |
| 4. Cheaper loans (5% interest) | 62.3% | +0.5 pts | 4,640 |
| 5. Stable CNG price (fixed at ₦318/scm) | 61.5% | −0.2 pts | 4,238 |

Simulated impact of each option, 10,000 draws, market conversion except option 3 (notebook 07).

### 7.2 Appraisal and ranking

Free conversion of 100,000 cars at the car mid price of ₦1.3m (S40) would cost about ₦130bn. Cutting the loan rate from 17.5% to 5% on a ₦1.3m two-year car loan gives up about ₦181,000 of interest per loan (S40, S18). That is about ₦18bn per 100,000 loans, against a scheme size of ₦10bn (S18). No sourced figure was found for the cost of new stations or capacity upgrades. Those costs are therefore rated Low, Medium or High with reasons rather than given in naira. Speed, feasibility and evidence scores are judgements, each with a rationale citing sources where available (`docs/policy_options.csv`).

| Option | Impact | Cost | Speed | Feasibility | Evidence | Weighted score | Rank |
|---|---|---|---|---|---|---|---|
| 2. More capacity at existing stations | 5 | 3 | 4 | 3 | 3 | 3.85 | 1 |
| 1. More refuelling points | 4 | 2 | 2 | 3 | 4 | 3.15 | 2 |
| 3. Free conversion | 2 | 1 | 4 | 4 | 3 | 2.55 | 3 |
| 4. Cheaper loans | 1 | 3 | 4 | 4 | 2 | 2.45 | 4 |
| 5. Stable CNG price | 1 | 3 | 3 | 2 | 2 | 2.00 | 5 |

Scores 1–5, 5 = best. Weights: impact 35%, cost 20%, speed 15%, feasibility 15%, evidence 15% (notebook 07).

The top two options keep their positions with equal weights (3.60 and 3.00) and with impact weighted at 50% (4.12 and 3.35). Only the order of options 3 and 4 changes: they tie for third under equal weights. Option 1 falls just below the threshold for the top impact band (+29.7 points against 30). Scoring it 5 would raise its weighted score to 3.50, which would still place it second.

### 7.3 Recommendations

The first recommendation is to raise capacity at the busiest existing stations. The proposed measures are additional compressors and dispensers, longer opening hours, and mobile units deployed to sites with the longest queues. The aim is that drivers queue for no more than about an hour a day. The lead would be the station operators, NNPC Retail with NIPCO and IBILE, supported by Pi-CNG and MDGIF, which has funded CNG infrastructure in Lagos (S37). Of the two queue options, this is the faster, because it builds on sites that already have land and a gas connection. Its feasibility depends on gas supply as well as equipment, as Delhi's early supply deficit showed (S27).

The second recommendation is to add refuelling points in areas with no confirmed site, such as Alimosho, Ikorodu, Badagry, Ibeju-Lekki and Lagos Island (notebook 05). A cheap first step is to confirm whether the 11 commissioned IBILE stations are selling gas. The lead would be Pi-CNG, working with Lagos State through IBILE, with the Nigerian Midstream and Downstream Petroleum Regulatory Authority (NMDPRA), the regulator that granted NIPCO its regulatory approvals (S38). This is a medium-term programme. The four mobile units planned for January 2025 remain unconfirmed (S35), which illustrates the delays involved.

The third recommendation is to link any expansion of free conversion to station capacity. Free kits add little to the probability that CNG pays on their own, and 100,000 car conversions would cost about ₦130bn (S40). Free conversion without added refuelling capacity would be expected to lengthen queues, which this analysis identifies as the main constraint. This interaction was not modelled. The lead would be Pi-CNG, which runs the free-kit programme and the approved conversion centres (S17, S39).

The fourth recommendation is not to prioritise cheaper loans or fixed CNG prices on the present evidence. In the simulation, neither changes the probability that CNG pays by more than 1 percentage point. A 5% rate would give up about ₦181,000 of interest per car loan. Fixing prices below market risks reducing supply. A published price band could still help drivers plan, since the September 2025 price rise was abrupt (S12), but that benefit lies outside what the model measures. If pursued, the leads would be MOFI and CREDICORP for loans (S18) and NMDPRA with the National Automotive Design and Development Council (NADDC), which announced the official CNG rate, for pricing (S10).

## 8. Limitations

The survey limits every result that draws on it. It covers 25 drivers found at CNG stations and car parks in Lagos. It is not a random sample, and it does not represent Lagos commercial drivers as a whole. Only 20 responses are usable for money figures, and some groups are very small. There is one keke CNG user (three keke drivers in total), and one unflagged taxi driver. Fifteen responses were recorded by the researcher and entered later, so transcription errors are possible, and interviewer-recorded answers may differ from self-completed ones. CNG drivers' pre-conversion petrol spend is recalled, possibly from months earlier, and some recalled figures are a large share of gross earnings. Nine of the 13 CNG drivers run bi-fuel vehicles, and their current petrol spend was not asked, so their fuel saving is probably overstated. Earnings are reported before owner remittance or app commission, so take-home pay per hour is lower and queue costs are an upper bound. Twelve of the 13 CNG drivers converted free, so the survey says nothing direct about drivers who paid market prices.

The cost model and simulation rest on further assumptions. The efficiency ratio of 1.0 comes from two sources that disagree on absolute efficiency (conflict C4), and it is applied to keke and danfo as well as cars. Petrol spend is rescaled assuming the same litres per day at any price. The triangular distributions are an assumption about shape: the low, mid and high values are sourced, but the shape is not. Inputs are drawn independently, although in practice they may move together. For example, higher petrol prices could push more drivers to CNG and lengthen queues. The simulation re-uses 20 real drivers and cannot create new information about drivers who were not surveyed. Queue times drawn from CNG users are applied to petrol drivers, who may refuel at different places and times. Danfo and taxi drivers use the car conversion price. The market case applies only while the loan is being repaid.

The station map uses approximate positions. Fifteen of 22 sites are placed at the centre of their neighbourhood, and the others matched a road or place name rather than a verified site. The list covers only sites named in published sources and may be incomplete or out of date. The 3 km circles show straight-line distance, not travel time.

The policy appraisal is partly judgement. Only the impact scores come from the simulation, and only the free-conversion cost and part of the loan cost are calculated. Each option is modelled on its own, so interactions are not captured. For example, free conversion would bring more vehicles to the same stations. The policy settings tested, such as "queues halved" or "capped at one hour", are test values rather than costed programmes. There is no evidence here on what investment would deliver them. Costs are indicative. The safety and awareness explanation for slow adoption was tested only through a single survey item.

## 9. Conclusion

CNG is much cheaper than petrol per kilometre in Nigeria, by 61–86% across the price scenarios tested. Whether conversion pays a commercial driver depends mainly on how long that driver queues for gas. For the Lagos drivers surveyed, conversion pays in most cases when daily queuing stays at about two hours or less. It pays in a minority of cases at three hours or more. Within observed ranges, the price gap between petrol and CNG and the cost of the kit matter much less than queue time. The evidence on access points the same way. Lagos has six confirmed refuelling points among 22 named sites, and most petrol drivers surveyed cite the lack of a nearby station. Experience in Delhi and Pakistan suggests that queues reflect supply lagging behind conversions. Delhi responded by expanding stations and gas allocation together (S28). The appraisal therefore favours raising capacity at existing stations, then extending the network, over further subsidies for kits or loans. These conclusions rest on a small, non-random survey and on modelling assumptions set out above. A larger, representative survey and verified station data would be needed to confirm them.

---

## References

- S01. Pi-CNG & EV. Jan 2026. Impact & Results (2026 Term Report). https://pci.gov.ng/impact.html
- S02. NESG (Omakoji, Aliyu, Wikina). Dec 2025. From Plans to Progress: The State of the Presidential CNG Initiative. https://app.nesgroup.org/download_resource_documents/Final_%20From%20Plans%20to%20Progress%20The%20State%20of%20the%20Presidential%20CNG%20Initiative%20in%20Nigeria_1764945608.pdf
- S03. The Guardian (Nigeria). 2026. Nigerians spend N58tr on fuel in 3yrs as CNG adoption stalls at 12%. https://guardian.ng/?p=2908818
- S04. Nairametrics. 20 Sep 2026. CNG conversion drive faces hurdles over financing, safety and operational bottlenecks. https://nairametrics.com/2026/09/20/nigerias-cng-conversion-drive-faces-hurdles-over-financing-safety-and-operational-bottlenecks/
- S05. Nairametrics. 9 Sep 2026. CNG cylinder explosion fears slowing adoption – Pi-CNG/EV CEO. https://nairametrics.com/2026/09/09/cng-cylinder-explosion-fears-slowing-adoption-in-nigeria-pi-cng-ev-ceo/
- S06. The Guardian (Nigeria). 30 Jul 2026. Gaps in standards, enforcement threaten Nigeria's CNG transition, SON warns. https://guardian.ng/?p=2888204
- S07. BusinessMonitor. 24 Dec 2025. Evaluating Nigeria's Presidential CNG Initiative Two Years On. https://businessmonitor.ng/2025/12/24/evaluating-nigerias-presidential-compressed-natural-gas-cng-initiative-two-years-on/
- S08. ThisDay. 30 Jun 2026. Pi-CNG Chair lists achievements, set to expand refuelling, charging networks. https://www.thisdaylive.com/2026/06/30/pi-cng-chair-lists-achievements-set-to-expand-refuelling-charging-networks/
- S09. TechEconomy. 28 Aug 2026. Tinubu, governors move to cut transport fares with CNG buses. https://techeconomy.ng/tinubu-governors-move-to-cut-transport-fares-with-220000-cng-buses
- S10. Legit.ng. Aug 2026. CNG costs N380 per SCM as Nigeria licenses 81 new retailers. https://www.legit.ng/business-economy/money/1727590-nigeria-licenses-81-firms-retail-cng-n380-scm-cars/
- S11. BusinessDay. 1 Oct 2026. Transport cost pain bites despite Tinubu's Oct 1 promise. https://businessday.ng/news/article/transport-cost-pain-bites-despite-tinubus-oct-1-promise
- S12. TheCable. 3 Sep 2025. CNG retail price increases by N150 per SCM in Lagos, Abuja. https://www.thecable.ng/cng-retail-price-increases-by-n150-per-scm-in-lagos-abuja/
- S13. Legit.ng. 2 Sep 2025. Filling stations announce new CNG pump prices closer to petrol cost. https://www.legit.ng/business-economy/energy/1672203-filling-stations-increase-cng-fuel-prices-nigerians-switch/
- S14. Gazette NGR (citing NBS). Mar 2026. Petrol pump price N1,051.47 per litre in February – NBS. https://gazettengr.com/?p=457722
- S15. Channels TV (citing NBS). 30 May 2026. Average petrol price hits ₦1,532 per litre. https://www.channelstv.com/2026/05/30/average-petrol-price-hits-%E2%82%A61532-per-litre/
- S16. Tribune. 24 Jun 2026. Petrol prices rise by 55% to N1,596/litre in May – NBS. https://tribuneonlineng.com/petrol-prices-rise-by-55-to-n1596-litre-in-may-nbs/
- S17. ICIR. 2 Oct 2024. What is the state of Tinubu's CNG conversion initiative?. https://www.icirnigeria.org/explainer-what-is-the-state-of-tinubus-cng-conversion-initiative/
- S18. BusinessDay. 16 Oct 2024. Nigeria launches N10 billion credit scheme for CNG vehicle conversions. https://businessday.ng/business-economy/article/nigeria-launches-n10-billion-credit-scheme-for-cng-vehicle-conversions/
- S19. TechEconomy. 16 Oct 2024. Lagos NURTW launches ₦10.2bn CNG tricycles. https://techeconomy.ng/lagos-nurtw-launches-10-2b-cng-tricycles-to-curb-rising-transport-expenses
- S20. Dataphyte. Oct 2024. Exploring the CNG option in post-subsidy Nigeria. https://dataphyte.com/topic/energy/exploring-the-cng-option-in-post-subsidy-nigeria
- S21. TechCabal. 2024–25. Lagos drivers reveal the most profitable ride-hailing apps. https://techcabal.com/?p=152847
- S22. Prime Business Africa. Oct 2024. The safety of using CNG: a growing concern after Benin explosion. https://www.primebusiness.africa/?p=184951
- S23. Dawn. 2 Jun 2011. Pakistan largest CNG user. https://www.dawn.com/news/633775
- S24. The Nation. 10 Jun 2026. Pakistan sees 83pc decline in CNG use since 2012, OGRA report shows. https://www.nation.com.pk/10-Jun-2026/pakistan-sees-83pc-decline-cng-use-since-2012-ogra-report-shows
- S25. Arab News. 1 Dec 2021. 'Longest' supply cut to CNG stations in Pakistan may jeopardize 20,000 jobs. https://www.arabnews.pk/node/1978991/pakistan
- S26. Arab News. Dec 2018. Shortfall forces closure of CNG stations in Punjab, Islamabad. https://www.arabnews.com/business/shortfall-forces-closure-of-cng-stations-in-punjab-islamabad-1427811
- S27. Singh, Sharma, Sharma & Bhan, CRRI. c. 2001. CNG in Delhi: implementation problems (Transport Asia workshop paper). https://groups.seas.harvard.edu/TransportAsia/workshop_papers/Singhetal.pdf
- S28. Press Information Bureau, Govt of India. 13 Jul 2003. Gas requirements of Delhi will be met. https://archive.pib.gov.in/release02/lyr2003/rjul2003/13072003/r130720031.html
- S29. Narain & Krupnick, Resources for the Future. 2007. The Impact of Delhi's CNG Program on Air Quality. https://www.rff.org/publications/working-papers/the-impact-of-delhi039s-cng-program-on-air-quality/
- S30. Gazette NGR (citing NBS). 31 Jul 2025. Jigawa, Ondo, Lagos paid highest retail price of petrol in June – NBS. https://gazettengr.com/jigawa-ondo-lagos-paid-highest-retail-price-of-petrol-in-june-nbs/
- S31. Channels TV (citing NBS). 23 Dec 2025. Consumers paid ₦1,061 average petrol price in November – NBS. https://www.channelstv.com/2025/12/23/consumers-paid-%E2%82%A61061-average-petrol-price-in-november-nbs/
- S32. Shipping Position (citing NBS). Feb 2026. Petrol price drops slightly to N1,048 per litre in December 2025 – NBS. https://shippingposition.com.ng/petrol-price-drops-slightly-to-n1048-per-litre-in-december-2025-nbs/
- S33. Legit.ng. 2 Mar 2026. NNPC announces new petrol price, NIPCO rolls out 20 new CNG stations. https://www.legit.ng/business-economy/energy/1699267-nnpc-reduces-petrol-price-lagos-nigerian-company-opens-filling-station-n380-fuel/
- S34. BusinessDay. 4 Jul 2024. Presidential CNG Initiative, NNPC, NIPCO commission 12 CNG stations in FCT, Lagos. https://businessday.ng/news/article/presidential-cng-initiative-nnpc-nipco-commission-12-cng-stations-to-drive-autogas-scheme-in-fct-lagos/
- S35. Advisors Reports. 17 Jan 2025. NNPC increases CNG stations in Lagos to 10 with 6 new mobile refuelling units. https://advisorsreports.com/nnpc-increases-cng-stations-in-lagos-to-10-with-addition-of-6-new-mobile-refueling-units/
- S36. Legit.ng. 15 Jan 2025. NNPC launches 6 new CNG filling stations, gives location. https://www.legit.ng/business-economy/energy/1635733-cng-nnpc-launches-6-filling-stations-nigerians-buy-fuel-priced-n200-location/
- S37. State House. 30 May 2026. President Tinubu commissions four MDGIF-supported CNG projects. https://statehouse.gov.ng/?p=64205
- S38. Gazette NGR. 14 Apr 2024. NIPCO completes four CNG stations in Lagos. https://gazettengr.com/nipco-completes-four-cng-stations-in-lagos/
- S39. BusinessDay. Sep 2024. Here are six locations for free CNG conversion in Lagos. https://businessday.ng/news/article/here-are-six-locations-for-free-cng-conversion-in-lagos/
- S40. Nairametrics. 3 Oct 2024. Inside the CNG conversion journey in Lagos. https://nairametrics.com/2024/10/03/inside-the-cng-conversion-journey-in-lagos/
- S41. TechCabal. 27 Sep 2024. "₦5000 gas can take me from Lagos to Ibadan": drivers move to CNG. https://techcabal.com/2024/09/27/rising-fuel-costs-push-early-cng-adoption/
- S42. Daily Trust. 14 Nov 2023. Conversion of petrol vehicles to CNG to cost N600,000 – FG. https://dailytrust.com/conversion-of-petrol-vehicles-to-cng-to-cost-n600000-fg/
- S43. Prime Business Africa. 2024–25. Between fuel price burden and CNG conversion cost: the dilemma of Nigerians. https://www.primebusiness.africa/?p=190735
- S47. The researcher. Oct 2026. Lagos commercial driver survey. None (primary data).

---

## Appendix A: Data conflicts

The table summarises the 14 conflicts logged in `docs/data_conflicts.md` and how each is treated.

| ID | Issue | Treatment |
|---|---|---|
| C1 | 120,000+ vehicles converted vs 93,845 kits deployed (S01) | Both reported; 93,845 used as the conservative figure |
| C2 | "12% adoption" matches progress to the 1m target, not market share (S03, S01) | Described as 12% of the 2027 target |
| C3 | 90 stations in 28 states (S01) vs 23 states (S11) | Cited as 23–28 states |
| C4 | 10.67 km/scm (S20) vs about 6.8 km/scm implied by the official benchmark (S05) | Ratio of about 1:1 used; savings modelled as a ratio |
| C5 | "₦70,330 daily saving" (S11) vs ride-hailing fuel spend of about ₦20,000/day (S21) | Excluded as a likely error |
| C6 | Conversion cost from ₦300k to ₦1.5m; free for commercial vehicles in 2024 (S02, S17, S20, S05) | Low/mid/high scenarios using published Lagos quotes |
| C7 | CNG price ₦230, ₦318, ₦380, up to ₦500+/scm (S13, S11, S10) | Modelled as scenarios |
| C8 | Technicians trained: 7,700 vs 8,000 vs 500+ (S01, S02) | Noted only |
| C9 | Pakistan station counts in Arab News inconsistent with 3,329 national stations (S26, S23) | Arab News cited for mechanism only |
| C10 | Official ₦300k–600k (S42) vs Lagos quotes ₦1m–1.7m, up to ₦2.5m (S40, S41) | Lagos quotes used in the model |
| C11 | NNPC Lagos pump ₦837 (S33) vs NBS Lagos average ₦966.61 (S14) | NBS used; NNPC as the low case |
| C12 | Four NNPC mobile units due by end January 2025, opening unconfirmed (S35, S36) | Marked planned; excluded from the confirmed count |
| C13 | IOGC 15-station network, 11 sites named (S37) | Named sites only counted |
| C14 | Keke conversion paid (₦100k–650k) vs free for association members (S43, S04, S17, S40) | Paid range used for the loan case; free case kept for the appraisal |

## Appendix B: Files for reproducing the results

Data:
- `data/raw/model_inputs.csv` (model parameters with source IDs)
- `data/raw/petrol_prices_nbs.csv` (NBS petrol price series)
- `data/raw/lagos_cng_stations.csv` (22 named Lagos CNG sites)
- `data/raw/lagos_conversion_centres.csv` and `data/raw/conversion_prices.csv`
- `data/processed/survey_clean.csv` (anonymised survey; the raw export is kept locally and not published)
- `data/processed/lagos_cng_stations_geocoded.csv`

Code:
- `src/load_data.py`, `src/cost_model.py`, `src/clean_survey.py`, `src/geocode_stations.py`, `src/monte_carlo.py`, `src/policy_options.py`
- `tests/` (run with `python -m pytest`)
- `requirements.txt`

Notebooks:
- `notebooks/01_petrol_prices.ipynb` (fuel price gap)
- `notebooks/02_cost_model.ipynb` (scenarios and break-even)
- `notebooks/03_survey_calibrated.ipynb` (survey CNG drivers)
- `notebooks/04_barriers.ipynb` (survey petrol drivers)
- `notebooks/05_station_map.ipynb` (station map)
- `notebooks/06_monte_carlo.ipynb` (simulation and sensitivity)
- `notebooks/07_policy_options.ipynb` (policy appraisal)

Documentation:
- `docs/sources.md`, `docs/data_conflicts.md`, `docs/model_inputs.md`, `docs/survey_method.md`, `docs/policy_options.csv`, `docs/notes/`

Figures (`outputs/figures/`):
- `petrol_vs_cng.html`, `break_even_queue.html`, `survey_break_even.html`, `barriers.html`
- `lagos_station_map.html`, `monte_carlo_net_benefit.html`, `monte_carlo_sensitivity.html`, `policy_options_impact.html`
