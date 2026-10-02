"""
Tests for src/cost_model.py.

Each test uses round numbers you can check by hand, so if a test fails it is
easy to see whether the code or the expectation is wrong.

Run from the project root:
    python -m pytest

Why pytest.approx: computers store decimals like 0.1 in binary, so a result
such as 3846.153846... can be off in the last few digits. pytest.approx
compares numbers with a tiny tolerance instead of demanding exact equality.
"""

import sys
from pathlib import Path

import pytest

# src/ isn't an installed package, so add it to the import path (same approach
# as the notebooks). Path(__file__) is this test file, so this works no matter
# which folder pytest is started from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cost_model import (  # noqa: E402  (import after the sys.path tweak, on purpose)
    break_even_queue_hours,
    fuel_saving_per_day,
    loan_cost_per_day,
    net_benefit_per_day,
    payback_days,
    queue_cost_per_day,
)


# ---------------------------------------------------------------------------
# 1. fuel_saving_per_day
# ---------------------------------------------------------------------------
def test_fuel_saving_half_price_cng_saves_half():
    # CNG at half the petrol price, same distance per unit -> half the spend is saved.
    # CNG cost = 10,000 x (500 / 1,000) / 1.0 = 5,000; saving = 10,000 - 5,000.
    assert fuel_saving_per_day(10_000, 1_000, 500, efficiency_ratio=1.0) == pytest.approx(5_000)


# ---------------------------------------------------------------------------
# 2. queue_cost_per_day
# ---------------------------------------------------------------------------
def test_queue_cost():
    # 2 refuels x 1.5 hours x NGN 2,000/hour = NGN 6,000
    assert queue_cost_per_day(2, 1.5, 2_000) == pytest.approx(6_000)


# ---------------------------------------------------------------------------
# 3. loan_cost_per_day
# ---------------------------------------------------------------------------
def test_loan_cost_zero_interest():
    # No interest: 1,200,000 / 12 months = 100,000 a month,
    # x 12 months / 312 working days = about NGN 3,846 per day.
    expected = 100_000 * 12 / 312
    assert loan_cost_per_day(1_200_000, 0, 1, working_days_per_year=312) == pytest.approx(expected)


def test_loan_cost_zero_conversion_cost():
    # A free (fully subsidised) conversion costs nothing to repay.
    assert loan_cost_per_day(0, 0.175, 2) == 0


# ---------------------------------------------------------------------------
# 4. net_benefit_per_day
# ---------------------------------------------------------------------------
def test_net_benefit():
    # 10,000 fuel saving - 4,000 queue cost - 1,000 loan cost = 5,000
    assert net_benefit_per_day(10_000, 4_000, 1_000) == pytest.approx(5_000)


# ---------------------------------------------------------------------------
# 5. break_even_queue_hours
# ---------------------------------------------------------------------------
def test_break_even_gives_zero_net_benefit():
    # The definition of break-even: queuing for exactly that long leaves the
    # driver no better or worse off. So feed the answer back through the model
    # and check net benefit comes out at zero.
    fuel_saving, loan_cost = 15_000, 2_500
    refuels, earnings = 1, 3_000

    hours = break_even_queue_hours(fuel_saving, loan_cost, refuels, earnings)
    queue_cost = queue_cost_per_day(refuels, hours, earnings)

    # abs=1e-6 because the expected value is 0, and a purely relative
    # tolerance around 0 would allow almost no rounding error.
    assert net_benefit_per_day(fuel_saving, queue_cost, loan_cost) == pytest.approx(0, abs=1e-6)


def test_break_even_is_zero_when_loan_exceeds_saving():
    # Loan cost (6,000) > fuel saving (5,000): CNG loses money even with no
    # queue, so the formula would give negative hours. Should return 0 instead.
    assert break_even_queue_hours(5_000, 6_000, 1, 3_000) == 0


# ---------------------------------------------------------------------------
# 6. payback_days
# ---------------------------------------------------------------------------
def test_payback_days():
    # 1,000,000 / (15,000 - 5,000) = 100 working days
    assert payback_days(1_000_000, 15_000, 5_000) == pytest.approx(100)


def test_payback_never_when_queue_exceeds_saving():
    # Queue cost (8,000) > fuel saving (5,000): the driver loses money every
    # day, so the conversion never pays back.
    assert payback_days(1_000_000, 5_000, 8_000) is None
