import pandas as pd
import logging
from pathlib import Path
from loader import load_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_enrichment_records() -> list[dict]:
    """
    Defines the new observations, events, and impact_links to enrich the dataset.
    Follows schema rules:
    - Events leave 'pillar' empty.
    - Impact links populate 'parent_id', 'pillar', 'related_indicator', etc.
    """
    return [
        # --- NEW OBSERVATIONS ---
        {
            "record_id": "OBS_ENR_001",
            "record_type": "observation",
            "pillar": "Access",
            "indicator": "Mobile Money Account Ownership (% adults)",
            "indicator_code": "ACC_MM_ACCOUNT",
            "value_numeric": 19.4,
            "observation_date": "2025-01-01",
            "source_name": "World Bank Global Findex 2025 Update",
            "source_url": "https://microdata.worldbank.org/index.php/catalog/7901",
            "confidence": "High",
            "collected_by": "Team Lead",
            "collection_date": "2026-07-18",
            "notes": "Captures quadrupling of mobile money accounts from 4.7% (2021) to 19.4%."
        },
        {
            "record_id": "OBS_ENR_002",
            "record_type": "observation",
            "pillar": "Infrastructure",
            "indicator": "4G Population Coverage (%)",
            "indicator_code": "INF_4G_COVERAGE",
            "value_numeric": 70.8,
            "observation_date": "2025-07-01",
            "source_name": "Ethio Telecom Annual Performance Report FY24/25",
            "source_url": "https://www.ethiotelecom.et",
            "confidence": "High",
            "collected_by": "Data Specialist",
            "collection_date": "2026-07-18",
            "notes": "4G footprint expanded to 70.8%, critical digital payment enabler."
        },
        {
            "record_id": "OBS_ENR_003",
            "record_type": "observation",
            "pillar": "Usage",
            "indicator": "Telebirr Registered Users (Millions)",
            "indicator_code": "USG_TELEBIRR_USERS",
            "value_numeric": 54.8,
            "observation_date": "2025-06-01",
            "source_name": "Ethio Telecom FY24/25 Performance Summary",
            "source_url": "https://www.ethiotelecom.et",
            "confidence": "High",
            "collected_by": "Analyst",
            "collection_date": "2026-07-18",
            "notes": "Supply-side registered base to track against active demand-side Findex usage."
        },
        {
            "record_id": "OBS_ENR_004",
            "record_type": "observation",
            "pillar": "Infrastructure",
            "indicator": "Total Active Agent Outlets",
            "indicator_code": "INF_AGENTS_TOTAL",
            "value_numeric": 540000.0,
            "observation_date": "2025-06-01",
            "source_name": "Digital Finance Ethiopia Hub / NBE Reports",
            "source_url": "https://digitalfinance.shega.co",
            "confidence": "Medium",
            "collected_by": "Analyst",
            "collection_date": "2026-07-18",
            "notes": "Agent network coverage proxy for cash-in/cash-out liquidity access."
        },

        # --- NEW EVENTS ---
        {
            "record_id": "EVT_ENR_001",
            "record_type": "event",
            "pillar": None,  # Schema Rule: Events leave pillar empty
            "indicator": "EthSwitch Instant Payment System (EIPS) Go-Live",
            "indicator_code": "EVT_ETHSWITCH_IPS",
            "value_numeric": None,
            "observation_date": "2024-02-15",
            "source_name": "AfricaNenda SIIPS Report 2024",
            "source_url": "https://africanenda.org",
            "confidence": "High",
            "collected_by": "Policy Analyst",
            "collection_date": "2026-07-18",
            "notes": "Real-time national switch enabling instant cross-bank and PSP transfers."
        },
        {
            "record_id": "EVT_ENR_002",
            "record_type": "event",
            "pillar": None,  # Schema Rule: Events leave pillar empty
            "indicator": "National Bank Mandates Unified ETHQR Standard",
            "indicator_code": "EVT_ETHQR_MANDATE",
            "value_numeric": None,
            "observation_date": "2024-11-01",
            "source_name": "National Bank of Ethiopia Directives",
            "source_url": "https://nbe.gov.et",
            "confidence": "High",
            "collected_by": "Policy Analyst",
            "collection_date": "2026-07-18",
            "notes": "Standardized QR payment code mandatory for all financial institutions."
        },

        # --- NEW IMPACT LINKS ---
        {
            "record_id": "LNK_ENR_001",
            "record_type": "impact_link",
            "parent_id": "EVT_ENR_001",
            "pillar": "Access",
            "related_indicator": "ACC_MM_ACCOUNT",
            "impact_direction": "Positive",
            "impact_magnitude": 10.0,
            "lag_months": 12,
            "evidence_basis": "Empirical evidence from Kenya (M-Pesa) & Tanzania interbank interoperability deployment.",
            "source_name": "GSMA State of the Industry Report",
            "source_url": "https://gsma.com/sotir",
            "confidence": "Medium",
            "collected_by": "Modeling Lead",
            "collection_date": "2026-07-18",
            "notes": "Interoperability expands network utility, driving new wallet signups."
        },
        {
            "record_id": "LNK_ENR_002",
            "record_type": "impact_link",
            "parent_id": "EVT_ENR_002",
            "pillar": "Usage",
            "related_indicator": "USG_DIGITAL_PAYMENT",
            "impact_direction": "Positive",
            "impact_magnitude": 8.5,
            "lag_months": 6,
            "evidence_basis": "India UPI QR standard adoption and EthSwitch transactional volume acceleration.",
            "source_name": "EthSwitch S.C. Annual Report",
            "source_url": "https://ethswitch.com",
            "confidence": "High",
            "collected_by": "Modeling Lead",
            "collection_date": "2026-07-18",
            "notes": "Reduces merchant friction, boosting retail digital payment adoption."
        }
    ]

def validate_and_enrich(df_unified: pd.DataFrame) -> pd.DataFrame:
    """Enriches the dataset with new records while ensuring schema adherence."""
    new_records = get_enrichment_records()
    df_new = pd.DataFrame(new_records)
    
    # Combine datasets
    df_enriched = pd.concat([df_unified, df_new], ignore_index=True)
    
    # Schema check
    events_with_pillar = df_enriched[(df_enriched['record_type'] == 'event') & (df_enriched['pillar'].notna())]
    if not events_with_pillar.empty:
        logging.warning(f"Found {len(events_with_pillar)} events with non-empty pillar. Clearing them per schema rules.")
        df_enriched.loc[df_enriched['record_type'] == 'event', 'pillar'] = None
        
    logging.info(f"Dataset successfully enriched. Total records: {len(df_enriched)}")
    return df_enriched

def main():
    data_dir = Path("data")
    df_unified, _ = load_data(data_dir)
    df_enriched = validate_and_enrich(df_unified)
    
    out_dir = data_dir / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "ethiopia_fi_enriched.csv"
    
    df_enriched.to_csv(out_file, index=False)
    logging.info(f"Saved enriched dataset to {out_file}")

if __name__ == "__main__":
    main()