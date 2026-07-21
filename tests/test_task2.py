import sys
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import pytest
import pandas as pd
from eda import calculate_growth_rates, analyze_gender_gap, analyze_registered_vs_active_gap, get_data_quality_summary


@pytest.fixture
def sample_eda_df():
    return pd.DataFrame([
        {
            "record_id": "OBS_1",
            "record_type": "observation",
            "pillar": "Access",
            "indicator_code": "ACC_OWNERSHIP",
            "value_numeric": 46.0,
            "observation_date": "2021-01-01",
            "confidence": "High"
        },
        {
            "record_id": "OBS_2",
            "record_type": "observation",
            "pillar": "Access",
            "indicator_code": "ACC_OWNERSHIP",
            "value_numeric": 49.0,
            "observation_date": "2024-01-01",
            "confidence": "High"
        },
        {
            "record_id": "OBS_3",
            "record_type": "observation",
            "pillar": "Access",
            "indicator_code": "ACC_OWN_MALE",
            "value_numeric": 56.0,
            "observation_date": "2024-01-01",
            "confidence": "High"
        },
        {
            "record_id": "OBS_4",
            "record_type": "observation",
            "pillar": "Access",
            "indicator_code": "ACC_OWN_FEMALE",
            "value_numeric": 42.0,
            "observation_date": "2024-01-01",
            "confidence": "High"
        },
        {
            "record_id": "OBS_5",
            "record_type": "observation",
            "pillar": "Usage",
            "indicator_code": "USG_TELEBIRR_USERS",
            "value_numeric": 54.8,
            "observation_date": "2025-01-01",
            "confidence": "High"
        },
        {
            "record_id": "OBS_6",
            "record_type": "observation",
            "pillar": "Access",
            "indicator_code": "ACC_MM_ACCOUNT",
            "value_numeric": 19.4,
            "observation_date": "2025-01-01",
            "confidence": "High"
        }
    ])


def test_calculate_growth_rates(sample_eda_df):
    growth_df = calculate_growth_rates(sample_eda_df, "ACC_OWNERSHIP")
    assert not growth_df.empty
    assert len(growth_df) == 2
    # Verify deceleration check: 49 - 46 = 3pp change over 3 years
    latest = growth_df.iloc[-1]
    assert latest["change_pp"] == 3.0
    assert latest["annualized_change_pp"] == 1.0


def test_analyze_gender_gap(sample_eda_df):
    gender_df = analyze_gender_gap(sample_eda_df)
    assert not gender_df.empty
    latest = gender_df.iloc[-1]
    # Male (56) - Female (42) = 14pp gap
    assert latest["gender_gap_pp"] == 14.0


def test_analyze_registered_vs_active_gap(sample_eda_df):
    gap_result = analyze_registered_vs_active_gap(sample_eda_df)
    assert gap_result["telebirr_registered_millions"] == 54.8
    assert gap_result["findex_mm_ownership_pct"] == 19.4
    assert gap_result["registration_to_active_gap_millions"] > 0


def test_get_data_quality_summary(sample_eda_df):
    summary = get_data_quality_summary(sample_eda_df)
    assert summary["total_records"] == 6
    assert summary["confidence_levels"]["High"] == 6