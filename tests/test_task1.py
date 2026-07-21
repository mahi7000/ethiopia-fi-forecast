import pytest
import pandas as pd
from pathlib import Path
import sys

# Ensure src module is discoverable
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from enrichment import get_enrichment_records, validate_and_enrich
from loader import load_data


@pytest.fixture
def project_data_dir():
    """Fixture providing the path to project data folder."""
    return Path(__file__).resolve().parent.parent / "data"


# --- Task 1 Data Loading Tests ---

def test_raw_data_loading(project_data_dir):
    """Test loading of unified dataset and reference codes."""
    raw_path = project_data_dir / "raw" / "ethiopia_fi_unified_data.csv"
    ref_path = project_data_dir / "raw" / "reference_codes.csv"
    
    if raw_path.exists() and ref_path.exists():
        df_unified, df_ref = load_data(project_data_dir)
        assert isinstance(df_unified, pd.DataFrame)
        assert isinstance(df_ref, pd.DataFrame)
        assert len(df_unified) > 0
        assert len(df_ref) > 0
        assert "record_type" in df_unified.columns
    else:
        pytest.skip("Raw starter files not found in data/raw/")


# --- Task 1 Schema Validation & Rule Tests ---

def test_enrichment_records_exist():
    """Verify that enrichment records are properly structured."""
    records = get_enrichment_records()
    assert isinstance(records, list)
    assert len(records) >= 8, "Task 1 requires at least 8 new enriched records (obs, events, links)"


def test_schema_record_types():
    """Ensure all enriched records use valid record types."""
    valid_types = {"observation", "event", "impact_link", "target"}
    records = get_enrichment_records()
    
    for rec in records:
        assert rec["record_type"] in valid_types, f"Invalid record_type: {rec.get('record_type')}"


def test_event_pillar_schema_rule():
    """
    CRITICAL RULE: Events must NOT have pre-assigned pillars.
    Pillars for events must be None / Empty to maintain unbiased data.
    """
    records = get_enrichment_records()
    events = [r for r in records if r["record_type"] == "event"]
    
    assert len(events) >= 2, "Must include at least 2 cataloged events in Task 1 enrichment"
    for evt in events:
        assert evt.get("pillar") is None or pd.isna(evt.get("pillar")), \
            f"Event {evt.get('record_id')} must have empty pillar according to schema rules"


def test_impact_links_schema_rules():
    """
    Verify impact_link structure:
    - Must have parent_id linking to a valid event
    - Must specify pillar, impact_direction, and impact_magnitude
    """
    records = get_enrichment_records()
    impact_links = [r for r in records if r["record_type"] == "impact_link"]
    
    assert len(impact_links) >= 2, "Must include at least 2 impact links in Task 1 enrichment"
    for link in impact_links:
        assert link.get("parent_id") is not None, "Impact link missing parent_id"
        assert link.get("pillar") in ["Access", "Usage", "Infrastructure"], f"Invalid pillar in link {link.get('record_id')}"
        assert link.get("impact_direction") in ["Positive", "Negative"], "Impact direction must be Positive/Negative"
        assert isinstance(link.get("impact_magnitude"), (int, float)), "Impact magnitude must be numeric"


def test_required_fields_documented():
    """Verify that documentation fields (source, confidence, collected_by) are present."""
    records = get_enrichment_records()
    
    for rec in records:
        assert rec.get("source_name") is not None, f"Record {rec.get('record_id')} missing source_name"
        assert rec.get("confidence") in ["High", "Medium", "Low"], f"Record {rec.get('record_id')} has invalid confidence"
        assert rec.get("collected_by") is not None, f"Record {rec.get('record_id')} missing collected_by"


def test_validate_and_enrich_pipeline():
    """Test end-to-end enrichment execution with mock raw dataset."""
    mock_raw = pd.DataFrame([
        {
            "record_id": "OBS_001",
            "record_type": "observation",
            "pillar": "Access",
            "indicator": "Account Ownership",
            "indicator_code": "ACC_OWNERSHIP",
            "value_numeric": 49.0,
            "observation_date": "2024-01-01",
            "source_name": "Findex",
            "source_url": "http://example.com",
            "confidence": "High",
            "collected_by": "Starter",
            "collection_date": "2024-01-01"
        }
    ])
    
    df_enriched = validate_and_enrich(mock_raw)
    
    # Check total records increased
    assert len(df_enriched) > len(mock_raw)
    
    # Check that rule enforcement cleared any accidental event pillars
    events = df_enriched[df_enriched["record_type"] == "event"]
    assert events["pillar"].isna().all(), "All event pillars in enriched dataframe must be NaN"


# --- Task 1 Processed Output File Test ---

def test_processed_file_exists_and_valid(project_data_dir):
    """Verify processed dataset file output if Task 1 has been executed."""
    processed_path = project_data_dir / "processed" / "ethiopia_fi_enriched.csv"
    
    if processed_path.exists():
        df_proc = pd.read_csv(processed_path)
        assert len(df_proc) > 0
        assert "record_type" in df_proc.columns
        assert "confidence" in df_proc.columns
        
        # Verify enriched codes are in the processed CSV
        codes = df_proc["indicator_code"].tolist()
        assert "ACC_MM_ACCOUNT" in codes
        assert "EVT_ETHSWITCH_IPS" in codes
    else:
        pytest.skip("Processed dataset not generated yet. Run 'python src/enrichment.py' first.")