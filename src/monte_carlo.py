"""
monte_carlo.py
--------------
Monte Carlo simulation of the daily CNG cost model.

Instead of one central scenario, we run the model thousands of times. Each run
("draw") picks a plausible value for every uncertain input, then calculates the
net benefit with the functions in cost_model.py. The spread of results shows how
likely CNG is to pay off, and which inputs matter most.

Each draw:
  - petrol price, CNG price           triangular(low, mid, high) from model_inputs.csv
  - one surveyed driver (bootstrap)   their daily petrol spend, net earnings per
                                      hour, working days and vehicle type
  - daily queue hours (bootstrap)     one CNG user's reported daily queue time
  - conversion cost, interest, tenor  triangular from model_inputs.csv
                                      ("market"), or loan cost = 0 ("free")

Triangular distribution: the simplest way to turn a low / most-likely / high
estimate into random draws. Values near "mid" are most likely, and nothing falls
outside low-high. It's an assumption about shape, not something the sources tell us.

Bootstrap: drawing whole survey rows at random, with replacement. It keeps each
driver's spend, earnings and days together, so we never pair one driver's
earnings with another's hours. But it can only ever produce the 20 drivers we have.

Run from the project root for a quick summary:
    python src/monte_carlo.py
"""

import pathlib

import numpy as np
import pandas as pd

import cost_model as cm
from load_data import RAW_DIR, read_csv_safe

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
SURVEY_PATH = PROJECT_ROOT / "data" / "processed" / "survey_clean.csv"

# Vehicle type -> which conversion_cost row in model_inputs.csv to use.
# The CSV only has car and keke rows. Danfo and taxi use the car row: an
# ASSUMPTION (a danfo kit is likely dearer than a car kit; no source yet).
CONVERSION_ROW = {"ride_hailing": "car", "taxi": "car", "danfo": "car", "keke": "keke"}


# ---------------------------------------------------------------------------
# Loading inputs
# ---------------------------------------------------------------------------
def load_inputs() -> pd.DataFrame:
    return read_csv_safe(RAW_DIR / "model_inputs.csv")


def get_row(inputs: pd.DataFrame, parameter: str, vehicle: str) -> dict:
    """Return {'low', 'mid', 'high'} as floats for one model_inputs.csv row (blank -> None)."""
    match = inputs[(inputs["parameter"] == parameter) & (inputs["vehicle"] == vehicle)]
    if len(match) != 1:
        raise ValueError(f"Expected 1 row for {parameter} / {vehicle}, found {len(match)}")
    row = match.iloc[0]
    return {k: float(row[k]) if str(row[k]).strip() else None for k in ("low", "mid", "high")}


def load_drivers() -> pd.DataFrame:
    """
    Unflagged survey drivers with the fields the simulation needs.

    survey_fuel_spend: what the driver spends (or spent) on petrol per day.
        Petrol users: current petrol spend.
        CNG users: recalled petrol spend before converting.
    net_earnings_per_hour: (gross - current fuel spend) / hours, the same
        definition as the net_earnings_per_hour row in model_inputs.csv (S47).
    """
    survey = pd.read_csv(SURVEY_PATH)
    d = survey[survey["quality_flag"].isna()].copy()
    current_fuel = d["cng_spend_per_day"].where(d["uses_cng"], d["petrol_spend_per_day"])
    d["survey_fuel_spend"] = d["petrol_before_per_day"].where(d["uses_cng"], d["petrol_spend_per_day"])
    d["net_earnings_per_hour"] = (d["gross_per_day"] - current_fuel) / d["hours_per_day"]
    d["working_days"] = d["days_per_week"] * 52
    cols = ["respondent_id", "vehicle_type", "uses_cng", "survey_fuel_spend",
            "net_earnings_per_hour", "working_days", "daily_queue_hours"]
    return d[cols].reset_index(drop=True)


def triangular(rng: np.random.Generator, row: dict, size: int) -> np.ndarray:
    return rng.triangular(row["low"], row["mid"], row["high"], size=size)


# ---------------------------------------------------------------------------
# The simulation
# ---------------------------------------------------------------------------
def run_simulation(n_draws=10_000, seed=42, conversion="market", queue_hours_fixed=None):
    """
    Run the Monte Carlo and return one row per draw.

    Args:
        n_draws:           number of draws
        seed:              random seed; the same seed always gives the same result
        conversion:        "market" (repay a loan for the kit) or "free" (loan cost 0)
        queue_hours_fixed: if given, every draw uses this daily queue time instead
                           of sampling one (used for the "what if queues were X hours" runs)

    Returns:
        DataFrame with the sampled inputs, fuel_saving, queue_cost, loan_cost and
        net_benefit (all NGN per working day) for each draw.

    Every random number is drawn in the same order whatever the options, so
    "market" and "free" runs with the same seed use the same prices, drivers and
    queues. The only difference between them is the loan, which makes the
    comparison fair.
    """
    if conversion not in ("market", "free"):
        raise ValueError('conversion must be "market" or "free"')

    rng = np.random.default_rng(seed)
    inputs = load_inputs()
    drivers = load_drivers()
    queue_pool = drivers.loc[drivers["uses_cng"], "daily_queue_hours"].to_numpy()

    # Fixed inputs (same in every draw)
    survey_petrol_price = get_row(inputs, "petrol_price_national", "all")["mid"]  # NGN/L ~Oct 2026 (S11)
    efficiency = get_row(inputs, "efficiency_ratio", "all")["mid"]                 # 1.0 (S20; S05)

    # 1. Prices
    petrol_price = triangular(rng, get_row(inputs, "petrol_price_national", "all"), n_draws)
    cng_price = triangular(rng, get_row(inputs, "cng_price", "car/bus"), n_draws)

    # 2. Bootstrap a driver: rng.integers picks a row number for each draw.
    sample = drivers.iloc[rng.integers(0, len(drivers), size=n_draws)].reset_index(drop=True)

    # 3. Bootstrap a daily queue time from the CNG users
    daily_queue = rng.choice(queue_pool, size=n_draws, replace=True)
    if queue_hours_fixed is not None:
        daily_queue = np.full(n_draws, float(queue_hours_fixed))

    # 4. Loan terms: always drawn (keeps the random sequence identical across
    #    options), then switched off for "free".
    # sorted(), not set(): Python orders a set of strings differently in every
    # new process, which would draw the car and keke kit prices in a different
    # order each run and break reproducibility. Sorting fixes the order.
    conv_rows = {v: get_row(inputs, "conversion_cost", v) for v in sorted(set(CONVERSION_ROW.values()))}
    conv_cost = np.empty(n_draws)
    for vehicle_row, row in conv_rows.items():
        # Draw a full set from this row, then keep it only where the driver's vehicle uses this row.
        draws = triangular(rng, row, n_draws)
        use = sample["vehicle_type"].map(CONVERSION_ROW).to_numpy() == vehicle_row
        conv_cost[use] = draws[use]
    interest = triangular(rng, get_row(inputs, "loan_interest_rate", "all"), n_draws) / 100  # CSV is in percent
    tenor = triangular(rng, get_row(inputs, "loan_tenor", "all"), n_draws)
    tenor = np.round(tenor * 12) / 12   # whole months, as a real loan would be

    # --- Model ---------------------------------------------------------------
    # Same litres per day as when surveyed, so spend scales with the petrol price.
    petrol_spend = sample["survey_fuel_spend"].to_numpy() * petrol_price / survey_petrol_price
    eph = sample["net_earnings_per_hour"].to_numpy()
    working_days = sample["working_days"].to_numpy()

    # These cost_model functions are plain arithmetic, so they accept whole
    # numpy arrays and calculate every draw at once.
    fuel_saving = cm.fuel_saving_per_day(petrol_spend, petrol_price, cng_price, efficiency)
    # daily_queue is hours per DAY, so refuels_per_day=1 gives daily hours x earnings per hour.
    queue_cost = cm.queue_cost_per_day(1, daily_queue, eph)

    if conversion == "free":
        loan_cost = np.zeros(n_draws)
        conv_cost[:] = 0.0
        interest[:] = np.nan
        tenor[:] = np.nan
    else:
        # loan_cost_per_day uses `if` checks, which only work on single numbers,
        # so it's called once per draw.
        loan_cost = np.array([
            cm.loan_cost_per_day(c, r, t, w) for c, r, t, w in zip(conv_cost, interest, tenor, working_days)
        ])

    net_benefit = cm.net_benefit_per_day(fuel_saving, queue_cost, loan_cost)

    return pd.DataFrame({
        "draw": np.arange(n_draws),
        "respondent_id": sample["respondent_id"],
        "vehicle_type": sample["vehicle_type"],
        "uses_cng": sample["uses_cng"],
        "petrol_price": petrol_price,
        "cng_price": cng_price,
        "survey_fuel_spend": sample["survey_fuel_spend"],
        "petrol_spend": petrol_spend,
        "net_earnings_per_hour": eph,
        "working_days": working_days,
        "daily_queue_hours": daily_queue,
        "conversion_cost": conv_cost,
        "interest_rate": interest,
        "tenor_years": tenor,
        "fuel_saving": fuel_saving,
        "queue_cost": queue_cost,
        "loan_cost": loan_cost,
        "net_benefit": net_benefit,
    })


if __name__ == "__main__":
    for option in ("market", "free"):
        result = run_simulation(conversion=option)
        print(f"{option:6s}: P(CNG pays) = {(result['net_benefit'] > 0).mean():.1%}, "
              f"median net benefit NGN {result['net_benefit'].median():,.0f}/day")
