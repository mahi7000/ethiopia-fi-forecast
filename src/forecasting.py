"""
src/forecasting.py
Module for financial inclusion forecasting and scenario analysis (2025-2028).
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple


def fit_baseline_trend(
    years: np.ndarray,
    values: np.ndarray,
    target_years: np.ndarray,
    model_type: str = "log_linear"
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fits baseline trend model on historical Findex observation points.
    Returns: (point_predictions, lower_ci, upper_ci)
    """
    if model_type == "log_linear":
        log_y = np.log(values)
        slope, intercept = np.polyfit(years, log_y, 1)
        pred_log = intercept + slope * target_years
        preds = np.exp(pred_log)
    else:  # Standard Linear
        slope, intercept = np.polyfit(years, values, 1)
        preds = intercept + slope * target_years

    # Calculate standard residual error for 95% Confidence Intervals
    hist_preds = np.exp(intercept + slope * years) if model_type == "log_linear" else intercept + slope * years
    residuals = values - hist_preds
    std_err = np.std(residuals) if len(residuals) > 2 else 2.5

    # Expanding uncertainty over forecast horizon
    time_delta = target_years - years[-1]
    uncertainty = 1.96 * std_err * np.sqrt(1 + (time_delta / 5.0))

    lower_ci = np.clip(preds - uncertainty, 0.0, 100.0)
    upper_ci = np.clip(preds + uncertainty, 0.0, 100.0)

    return preds, lower_ci, upper_ci


def generate_event_augmented_forecasts(
    baseline_preds: np.ndarray,
    target_years: np.ndarray,
    event_impacts: Dict[int, float],
    scenario_multiplier: float = 1.0,
    saturation_cap: float = 85.0
) -> np.ndarray:
    """
    Applies Task 3 event impacts to baseline trend forecasts with saturation caps.
    """
    final_forecasts = []

    for idx, year in enumerate(target_years):
        base_val = baseline_preds[idx]
        cum_impact = sum(impact for ev_yr, impact in event_impacts.items() if ev_yr <= year)
        
        # Apply scenario multiplier to event effects
        adjusted_val = base_val + (cum_impact * scenario_multiplier)
        
        # Diminishing returns ceiling (Logistic Saturation Cap)
        capped_val = saturation_cap / (1.0 + np.exp(-4.0 * (adjusted_val - 20.0) / saturation_cap)) if adjusted_val > saturation_cap * 0.8 else adjusted_val
        
        final_forecasts.append(round(min(capped_val, saturation_cap), 2))

    return np.array(final_forecasts)


def compile_forecast_table(
    target_years: np.ndarray,
    baseline: np.ndarray,
    lower_ci: np.ndarray,
    upper_ci: np.ndarray,
    base_scenario: np.ndarray,
    optimistic_scenario: np.ndarray,
    pessimistic_scenario: np.ndarray
) -> pd.DataFrame:
    """Compiles forecast data into a structured pandas DataFrame."""
    return pd.DataFrame({
        "year": target_years,
        "baseline_pct": np.round(baseline, 2),
        "ci_lower_95": np.round(lower_ci, 2),
        "ci_upper_95": np.round(upper_ci, 2),
        "base_policy_scenario": base_scenario,
        "optimistic_scenario": optimistic_scenario,
        "pessimistic_scenario": pessimistic_scenario,
    })