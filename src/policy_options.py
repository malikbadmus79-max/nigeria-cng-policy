"""
policy_options.py
-----------------
Simulated impact of five policy options on whether CNG pays for drivers.

Each option re-runs the Monte Carlo in monte_carlo.py (10,000 draws, seed 42,
market-price conversion) with one input changed. Because every run uses the
same seed and run_simulation applies policy changes AFTER drawing, each option
sees exactly the same prices, drivers and queues as the baseline. The change
in results is due to the policy alone, not to luck of the draw.

Also here: the rule that turns a simulated change into an impact score, and
the two cost calculations that can be made from sourced inputs.

Run from the project root:
    python src/policy_options.py
"""

import pandas as pd

import cost_model as cm
import monte_carlo as mc

N_DRAWS = 10_000
SEED = 42

# Interest rate for option 4. A policy choice to test, not a sourced figure.
CHEAP_LOAN_RATE = 0.05


def option_settings() -> dict:
    """
    Option name -> (short description, run_simulation keyword arguments).

    Built in a function, not at import time, because option 5 needs the CNG
    mid price read from model_inputs.csv.
    """
    cng_mid = mc.get_row(mc.load_inputs(), "cng_price", "car/bus")["mid"]   # NGN/scm (S11)
    return {
        "baseline": ("As surveyed: market-price conversion on current loan terms", {}),
        "option 1": ("More refuelling points: daily queue time halved", {"queue_multiplier": 0.5}),
        "option 2": ("More capacity at existing stations: daily queue capped at 1 hour", {"queue_cap": 1.0}),
        "option 3": ("Free conversion", {"conversion": "free"}),
        "option 4": (f"Cheaper loans: interest fixed at {CHEAP_LOAN_RATE:.0%}", {"fixed_interest": CHEAP_LOAN_RATE}),
        "option 5": (f"Stable CNG price: fixed at the mid value, NGN {cng_mid:,.0f}/scm",
                     {"fixed_cng_price": cng_mid}),
    }


def run_options(n_draws=N_DRAWS, seed=SEED) -> pd.DataFrame:
    """
    Run every option and return one row each: probability CNG pays, median net
    benefit, and the change from baseline.
    """
    rows = []
    for option, (description, kwargs) in option_settings().items():
        # "market" unless the option says otherwise (option 3 sets "free").
        kwargs = {"conversion": "market", **kwargs}
        result = mc.run_simulation(n_draws, seed, **kwargs)
        rows.append({
            "option": option,
            "description": description,
            "p_pays": (result["net_benefit"] > 0).mean(),
            "median_net_benefit": result["net_benefit"].median(),
        })
    out = pd.DataFrame(rows).set_index("option")
    out["change_pts"] = (out["p_pays"] - out.loc["baseline", "p_pays"]) * 100   # percentage points
    out["change_median"] = out["median_net_benefit"] - out.loc["baseline", "median_net_benefit"]
    return out


def impact_score(change_pts: float) -> int:
    """
    Turn a change in probability (percentage points) into a 1-5 impact score.

    The bands are a stated rule, set before seeing results, so the score
    follows the simulation rather than judgement:
        >= 30 pts -> 5 | 15-30 -> 4 | 5-15 -> 3 | 1-5 -> 2 | < 1 -> 1
    """
    for threshold, score in [(30, 5), (15, 4), (5, 3), (1, 2)]:
        if change_pts >= threshold:
            return score
    return 1


def free_conversion_cost(n_conversions=100_000) -> float:
    """Fiscal cost (NGN) of paying for n car conversions at the car mid price (S40)."""
    car_mid = mc.get_row(mc.load_inputs(), "conversion_cost", "car")["mid"]
    return n_conversions * car_mid


def interest_subsidy_per_loan(rate_from=None, rate_to=CHEAP_LOAN_RATE) -> float:
    """
    Interest a lender gives up (NGN) on one car conversion loan if the rate is
    cut from the mid rate (S18) to rate_to, at the car mid price (S40) over
    the mid tenor (S18). Total repaid at the old rate minus total repaid at
    the new rate.

    loan_cost_per_day x working days per year = repayment per year, so x tenor
    years = total repaid. The working days cancel out, so any value works.
    """
    inputs = mc.load_inputs()
    principal = mc.get_row(inputs, "conversion_cost", "car")["mid"]
    tenor = mc.get_row(inputs, "loan_tenor", "all")["mid"]
    if rate_from is None:
        rate_from = mc.get_row(inputs, "loan_interest_rate", "all")["mid"] / 100

    def total_repaid(rate):
        return cm.loan_cost_per_day(principal, rate, tenor, 365) * 365 * tenor

    return total_repaid(rate_from) - total_repaid(rate_to)


if __name__ == "__main__":
    results = run_options()
    results["impact_score"] = results["change_pts"].apply(impact_score)
    pd.options.display.width = 160
    print(results.round(3).to_string())
    print(f"\nOption 3, 100,000 free car conversions: NGN {free_conversion_cost() / 1e9:,.0f} bn")
    print(f"Option 4, interest given up per car loan: NGN {interest_subsidy_per_loan():,.0f}")
