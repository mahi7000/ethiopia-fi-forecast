"""
src/impact_modeling.py
Module for modeling event impacts on financial inclusion indicators.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple


def load_and_merge_impact_data(csv_path: str) -> pd.DataFrame:
    """Loads enriched dataset and merges impact links with parent events."""
    df = pd.read_csv(csv_path)

    events_df = df[df["record_type"] == "event"].copy()
    links_df = df[df["record_type"] == "impact_link"].copy()

    if links_df.empty:
        raise ValueError("No impact_link records found in dataset.")

    # Select existing metadata columns from events
    id_col = "record_id" if "record_id" in events_df.columns else "id"
    event_cols = [id_col]
    for col in ["observation_date", "indicator_name", "notes", "source_name", "description"]:
        if col in events_df.columns:
            event_cols.append(col)

    # Merge links with parent event details
    merged_df = pd.merge(
        links_df,
        events_df[event_cols],
        left_on="parent_id",
        right_on=id_col,
        suffixes=("_link", "_event"),
        how="left",
    )

    return merged_df


def build_association_matrix(impact_merged_df: pd.DataFrame) -> pd.DataFrame:
    """Constructs Event-Indicator Association Matrix (Rows: Parent Event ID, Cols: Related Indicator)."""
    # Map directly to the verified dataset schema
    index_col = "parent_id"
    col_name = "related_indicator" if "related_indicator" in impact_merged_df.columns else "indicator_code"
    val_col = "impact_magnitude" if "impact_magnitude" in impact_merged_df.columns else "impact_magnitude_pp"

    # Convert numeric values cleanly
    impact_merged_df[val_col] = pd.to_numeric(impact_merged_df[val_col], errors="coerce").fillna(0.0)

    pivot_df = impact_merged_df.pivot_table(
        index=index_col,
        columns=col_name,
        values=val_col,
        aggfunc="sum",
    ).fillna(0.0)

    return pivot_df


def calculate_temporal_impact(
    t_current: float,
    t_event: float,
    magnitude: float,
    lag_months: float = 6.0,
    ramp_months: float = 18.0,
) -> float:
    """
    Calculates non-linear impact at time t using a Sigmoid/Logistic Ramp-up Function.
    
    Formula:
      S(t) = Magnitude / (1 + exp(-k * (t - t_event - lag - ramp/2)))
    """
    elapsed_months = (t_current - t_event) * 12.0

    if elapsed_months < lag_months:
        return 0.0

    # Logistic growth parameter
    k = 6.0 / max(ramp_months, 1.0)
    midpoint = lag_months + (ramp_months / 2.0)
    
    growth_factor = 1.0 / (1.0 + np.exp(-k * (elapsed_months - midpoint)))
    return magnitude * growth_factor


def validate_telebirr_impact(
    baseline_2021: float = 4.7,
    observed_2024: float = 19.4,
    modeled_telebirr_impact: float = 8.2,
    modeled_ethswitch_impact: float = 2.5,
) -> Dict[str, float]:
    """Validates predicted mobile money account growth against observed Findex figures."""
    predicted_2024 = baseline_2021 + modeled_telebirr_impact + modeled_ethswitch_impact
    absolute_error = abs(predicted_2024 - observed_2024)
    percentage_error = (absolute_error / observed_2024) * 100.0

    return {
        "baseline_2021": baseline_2021,
        "observed_2024": observed_2024,
        "predicted_2024": round(predicted_2024, 2),
        "absolute_error_pp": round(absolute_error, 2),
        "mape_pct": round(percentage_error, 2),
    }