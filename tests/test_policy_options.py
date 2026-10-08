"""
Tests for src/policy_options.py: the impact-score rule and the cost calculations.

Run from the project root:
    python -m pytest
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from policy_options import free_conversion_cost, impact_score, interest_subsidy_per_loan  # noqa: E402


@pytest.mark.parametrize(
    "change_pts, score",
    [(36.4, 5), (30, 5), (29.9, 4), (15, 4), (14.9, 3), (5, 3), (4.9, 2), (1, 2), (0.9, 1), (0, 1), (-3, 1)],
)
def test_impact_score_bands(change_pts, score):
    # Boundaries belong to the higher band (">= 30 -> 5").
    assert impact_score(change_pts) == score


def test_free_conversion_cost_uses_car_mid():
    # 100,000 x NGN 1,300,000 (conversion_cost car mid, S40) = NGN 130 bn.
    assert free_conversion_cost(100_000) == pytest.approx(130e9)


def test_interest_subsidy_is_positive_and_zero_when_rate_unchanged():
    assert interest_subsidy_per_loan() > 0
    assert interest_subsidy_per_loan(rate_from=0.05, rate_to=0.05) == pytest.approx(0)
