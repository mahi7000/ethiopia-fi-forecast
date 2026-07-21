import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_data(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads ethiopia_fi_unified_data.csv and reference_codes.csv.
    Handles potential multi-sheet files or standard CSVs seamlessly.
    """
    data_path = data_dir / "raw" / "ethiopia_fi_unified_data.csv"
    ref_path = data_dir / "raw" / "reference_codes.csv"
    
    if not data_path.exists():
        raise FileNotFoundError(f"Unified dataset not found at {data_path}")
    if not ref_path.exists():
        raise FileNotFoundError(f"Reference codes file not found at {ref_path}")

    # Load unified dataset
    df_unified = pd.read_csv(data_path)
    df_ref = pd.read_csv(ref_path)
    
    logging.info(f"Loaded unified dataset with {len(df_unified)} records.")
    logging.info(f"Loaded reference codes with {len(df_ref)} entries.")
    
    return df_unified, df_ref

if __name__ == "__main__":
    df, ref = load_data(Path("data"))
    print(df.head())