"""
tests/test_task4.py
Unit tests for Task 4 forecasting module.
"""

import pytest
import numpy as np
from src.forecasting import (
    fit_baseline_trend,
    generate_event_augmented_forecasts,
    compile_forecast_table,
)


def test_baseline_trend_shape_and_bounds():
    """Verify forecast arrays match output dimensions and stay within percentage limits."""
    hist_yrs = np.array([2011, 2014, 2017, 2021, 2024])
    hist_vals = np.array([14.0, 21.8, 34.8, 46.1, 49.0])
    target_yrs = np.array([2025, 2026, 2027, 2028])

    preds, low_ci, high_ci = fit_baseline_trend(hist_yrs, hist_vals, target_yrs)

    assert len(preds) == len(target_yrs)
    assert np.all(preds >= 0.0) and np.all(preds <= 100.0)
    assert np.all(low_ci <= preds)
    assert np.all(high_ci >= preds)


def test_event_augmented_multipliers():
    """Verify scenario scaling orders (Optimistic > Base > Pessimistic)."""
    base_preds = np.array([50.0, 52.0, 54.0])
    target_yrs = np.array([2025, 2026, 2027])
    events = {2025: 2.0, 2026: 4.0, 2027: 6.0}

    base_scen = generate_event_augmented_forecasts(base_preds, target_yrs, events, 1.0)
    opt_scen = generate_event_augmented_forecasts(base_preds, target_yrs, events, 1.35)
    pess_scen = generate_event_augmented_forecasts(base_preds, target_yrs, events, 0.45)

    assert np.all(opt_scen > base_scen)
    assert np.all(base_scen > pess_scen)


def test_compile_forecast_table_columns():
    """Ensure compiled table contains expected header keys."""
    target_yrs = np.array([2025, 2026])
    df = compile_forecast_table(
        target_yrs,
        np.array([50.0, 52.0]),
        np.array([48.0, 49.0]),
        np.array([52.0, 55.0]),
        np.array([53.0, 56.0]),
        np.array([55.0, 58.0]),
        np.array([51.0, 53.0]),
    )

    assert "baseline_pct" in df.columns
    assert "base_policy_scenario" in df.columns
    assert len(df) == 2