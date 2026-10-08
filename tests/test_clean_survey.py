"""
Tests for src/clean_survey.py: the queue-band midpoint mapping and the
quality-flag rule.

Run from the project root:
    python -m pytest
"""

import math
import sys
from pathlib import Path

import pytest

# Same import-path tweak as test_cost_model.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from clean_survey import quality_flag, queue_band_to_hours  # noqa: E402

NAN = float("nan")


# ---------------------------------------------------------------------------
# 1. Queue band midpoints
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "band, hours",
    [
        ("Less than 30 minutes", 0.25),
        ("30 minutes to 1 hour", 0.75),
        ("1 to 2 hours", 1.5),
        ("2 to 4 hours", 3),
        ("4 to 6 hours", 5),
        ("More than 6 hours", 7),
    ],
)
def test_queue_band_midpoints(band, hours):
    assert queue_band_to_hours(band) == hours


def test_blank_queue_band_is_nan():
    # Petrol-only drivers skip the queue question.
    assert math.isnan(queue_band_to_hours(NAN))


def test_unknown_queue_band_raises():
    # A new/misspelt band must fail loudly, not become NaN silently.
    with pytest.raises(KeyError):
        queue_band_to_hours("About 3 hours")


# ---------------------------------------------------------------------------
# 2. Quality flag rule
# ---------------------------------------------------------------------------
def test_plausible_row_not_flagged():
    assert quality_flag(gross_per_day=80_000, petrol_spend=25_000, cng_spend=NAN) == ""


def test_petrol_spend_equal_to_gross_is_flagged():
    # ">=" - spending the whole day's takings on fuel is implausible.
    assert quality_flag(25_000, 25_000, NAN) == "petrol spend >= gross"


def test_cng_spend_above_gross_is_flagged():
    assert quality_flag(30_000, NAN, 35_000) == "CNG spend >= gross"


def test_gross_below_threshold_is_flagged():
    assert quality_flag(19_999, 5_000, NAN) == "gross < 20,000"


def test_gross_exactly_at_threshold_not_flagged():
    # The rule is "below 20,000", so 20,000 itself passes.
    assert quality_flag(20_000, 5_000, NAN) == ""


def test_multiple_reasons_are_joined():
    assert quality_flag(11_000, 30_000, NAN) == "petrol spend >= gross; gross < 20,000"


def test_blank_fuel_figures_do_not_flag():
    # NaN comparisons are False, so "question not asked" never triggers a flag.
    assert quality_flag(80_000, NAN, NAN) == ""
