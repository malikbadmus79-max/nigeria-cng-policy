"""
Tests for src/monte_carlo.py.

Small n_draws keeps these fast; the properties being checked don't depend on size.

Run from the project root:
    python -m pytest
"""

import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Same import-path tweak as test_cost_model.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from monte_carlo import run_simulation  # noqa: E402

N = 500


@pytest.mark.parametrize("conversion", ["market", "free"])
def test_same_seed_gives_identical_results(conversion):
    first = run_simulation(n_draws=N, seed=7, conversion=conversion)
    second = run_simulation(n_draws=N, seed=7, conversion=conversion)
    pd.testing.assert_frame_equal(first, second)


def test_same_seed_is_identical_across_separate_python_processes():
    # Python randomises the order of sets and dict hashing per process
    # (PYTHONHASHSEED). Running in two fresh processes with different hash seeds
    # catches any hidden dependence on that order, which a single-process test can't.
    script = (
        "import sys; sys.path.insert(0, r'{src}'); from monte_carlo import run_simulation; "
        "print(run_simulation(n_draws=300, seed=5)['net_benefit'].sum().round(6))"
    ).format(src=Path(__file__).resolve().parent.parent / "src")
    outputs = []
    for hash_seed in ("1", "2"):
        env = {**os.environ, "PYTHONHASHSEED": hash_seed}
        done = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, env=env, check=True)
        outputs.append(done.stdout.strip())
    assert outputs[0] == outputs[1]


def test_different_seed_gives_different_results():
    # Guards against the seed being ignored, which would make the test above pass trivially.
    a = run_simulation(n_draws=N, seed=1)
    b = run_simulation(n_draws=N, seed=2)
    assert not a["net_benefit"].equals(b["net_benefit"])


@pytest.mark.parametrize("n_draws", [1, 50, N])
def test_output_has_n_draws_rows(n_draws):
    assert len(run_simulation(n_draws=n_draws)) == n_draws


@pytest.mark.parametrize("conversion", ["market", "free"])
def test_net_benefit_is_saving_minus_queue_minus_loan(conversion):
    r = run_simulation(n_draws=N, conversion=conversion)
    expected = r["fuel_saving"] - r["queue_cost"] - r["loan_cost"]
    np.testing.assert_allclose(r["net_benefit"], expected, rtol=0, atol=1e-6)


def test_free_conversion_has_no_loan_cost():
    r = run_simulation(n_draws=N, conversion="free")
    assert (r["loan_cost"] == 0).all()


def test_market_and_free_share_every_draw_except_the_loan():
    # Same seed -> same prices, drivers and queues, so the difference is only the loan.
    market = run_simulation(n_draws=N, seed=3, conversion="market")
    free = run_simulation(n_draws=N, seed=3, conversion="free")
    for col in ["petrol_price", "cng_price", "respondent_id", "daily_queue_hours", "fuel_saving", "queue_cost"]:
        pd.testing.assert_series_equal(market[col], free[col])
    np.testing.assert_allclose(free["net_benefit"] - market["net_benefit"], market["loan_cost"], atol=1e-6)


def test_fixed_queue_hours_override():
    r = run_simulation(n_draws=N, queue_hours_fixed=2)
    assert (r["daily_queue_hours"] == 2).all()
