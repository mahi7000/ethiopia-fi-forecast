"""
tests/test_task3.py
Unit tests for Task 3 event impact modeling module.
"""

import pytest
import pandas as pd
from src.impact_modeling import (
    calculate_temporal_impact,
    validate_telebirr_impact,
    build_association_matrix,
)


def test_temporal_impact_zero_before_lag():
    """Verify that impact is 0 prior to lag completion."""
    # Event in 2021.0, 6-month lag -> No impact after 2 months (0.166 years)
    impact = calculate_temporal_impact(
        t_current=2021.16, t_event=2021.0, magnitude=5.0, lag_months=6.0, ramp_months=12.0
    )
    assert impact == 0.0


def test_temporal_impact_builds_over_time():
    """Verify non-linear growth after lag period."""
    impact_early = calculate_temporal_impact(
        t_current=2021.75, t_event=2021.0, magnitude=5.0, lag_months=3.0, ramp_months=12.0
    )
    impact_late = calculate_temporal_impact(
        t_current=2023.0, t_event=2021.0, magnitude=5.0, lag_months=3.0, ramp_months=12.0
    )
    assert impact_early > 0.0
    assert impact_late > impact_early
    assert pytest.approx(impact_late, rel=1e-1) == 5.0


def test_historical_validation_accuracy():
    """Check that Telebirr model error remains within acceptable threshold (<25%)."""
    res = validate_telebirr_impact()
    assert res["mape_pct"] < 25.0
    assert res["predicted_2024"] > res["baseline_2021"]


def test_association_matrix_structure():
    """Ensure association matrix builds correct pivoting dimensions."""
    sample_data = pd.DataFrame([
        {"parent_id": "EVT_1", "indicator_code": "ACC_OWN", "impact_magnitude_pp": 2.5},
        {"parent_id": "EVT_1", "indicator_code": "USG_PAY", "impact_magnitude_pp": 5.0},
        {"parent_id": "EVT_2", "indicator_code": "ACC_OWN", "impact_magnitude_pp": 1.0},
    ])
    matrix = build_association_matrix(sample_data)
    assert matrix.shape == (2, 2)
    assert matrix.loc["EVT_1", "ACC_OWN"] == 2.5
    assert matrix.loc["EVT_2", "USG_PAY"] == 0.0