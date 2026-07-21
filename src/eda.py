import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def calculate_growth_rates(df: pd.DataFrame, indicator_code: str = "ACC_OWNERSHIP") -> pd.DataFrame:
    """Calculates year-over-year and period growth rates for a given indicator."""
    filtered = df[df["indicator_code"] == indicator_code].copy()
    if filtered.empty:
        logging.warning(f"No records found for indicator_code: {indicator_code}")
        return pd.DataFrame()

    filtered["observation_date"] = pd.to_datetime(filtered["observation_date"])
    filtered = filtered.sort_values("observation_date").reset_index(drop=True)
    filtered["year"] = filtered["observation_date"].dt.year

    # Calculate absolute change (percentage points) and relative growth (%)
    filtered["prev_value"] = filtered["value_numeric"].shift(1)
    filtered["prev_year"] = filtered["year"].shift(1)
    filtered["change_pp"] = filtered["value_numeric"] - filtered["prev_value"]
    filtered["years_elapsed"] = filtered["year"] - filtered["prev_year"]
    filtered["annualized_change_pp"] = filtered["change_pp"] / filtered["years_elapsed"]
    filtered["pct_growth"] = ((filtered["value_numeric"] - filtered["prev_value"]) / filtered["prev_value"]) * 100

    return filtered[["year", "value_numeric", "change_pp", "years_elapsed", "annualized_change_pp", "pct_growth"]]


def analyze_gender_gap(df: pd.DataFrame) -> pd.DataFrame:
    """Computes the historical financial inclusion gender gap between males and females."""
    male_df = df[df["indicator_code"] == "ACC_OWN_MALE"][["observation_date", "value_numeric"]].rename(
        columns={"value_numeric": "male_ownership"}
    )
    female_df = df[df["indicator_code"] == "ACC_OWN_FEMALE"][["observation_date", "value_numeric"]].rename(
        columns={"value_numeric": "female_ownership"}
    )

    if male_df.empty or female_df.empty:
        logging.warning("Gender disaggregated data missing or incomplete.")
        return pd.DataFrame()

    merged = pd.merge(male_df, female_df, on="observation_date", how="inner")
    merged["observation_date"] = pd.to_datetime(merged["observation_date"])
    merged["year"] = merged["observation_date"].dt.year
    merged["gender_gap_pp"] = merged["male_ownership"] - merged["female_ownership"]
    merged["female_to_male_ratio"] = merged["female_ownership"] / merged["male_ownership"]

    return merged.sort_values("year").reset_index(drop=True)


def analyze_registered_vs_active_gap(df: pd.DataFrame) -> dict:
    """Evaluates supply-side registered accounts vs demand-side Findex active usage."""
    telebirr_users = df[df["indicator_code"] == "USG_TELEBIRR_USERS"]["value_numeric"].max()
    mm_findex_rate = df[df["indicator_code"] == "ACC_MM_ACCOUNT"]["value_numeric"].max()

    # Assuming adult population ~65 Million for calculation
    adult_pop_millions = 65.0
    estimated_survey_active_millions = (mm_findex_rate / 100.0) * adult_pop_millions if mm_findex_rate else 0.0

    return {
        "telebirr_registered_millions": telebirr_users,
        "findex_mm_ownership_pct": mm_findex_rate,
        "estimated_survey_active_millions": round(estimated_survey_active_millions, 2),
        "registration_to_active_gap_millions": round(telebirr_users - estimated_survey_active_millions, 2)
        if telebirr_users
        else None,
    }


def get_data_quality_summary(df: pd.DataFrame) -> dict:
    """Summarizes record counts by record_type, pillar, and confidence level."""
    return {
        "record_types": df["record_type"].value_counts().to_dict(),
        "pillars": df["pillar"].value_counts(dropna=False).to_dict(),
        "confidence_levels": df["confidence"].value_counts(dropna=False).to_dict(),
        "total_records": len(df),
    }


if __name__ == "__main__":
    data_path = Path("data/processed/ethiopia_fi_enriched.csv")
    if data_path.exists():
        df_data = pd.read_csv(data_path)
        print("=== Growth Rates ===")
        print(calculate_growth_rates(df_data))
        print("\n=== Gender Gap ===")
        print(analyze_gender_gap(df_data))