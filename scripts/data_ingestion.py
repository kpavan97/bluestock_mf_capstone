from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"

CSV_FILES = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

def load_all_datasets():
    datasets = {}
    for filename in CSV_FILES:
        filepath = RAW_DIR / filename
        if not filepath.exists():
            print(f"[MISSING] {filename} not found in data/raw/")
            continue
        try:
            df = pd.read_csv(filepath)
            datasets[filename] = df
            print(f"\n{'='*60}")
            print(f"FILE: {filename}")
            print(f"  Shape   : {df.shape}")
            print(f"  Dtypes  :\n{df.dtypes}")
            print(f"  Head    :\n{df.head()}")
            null_counts = df.isnull().sum()
            if null_counts.any():
                print(f"  Nulls   :\n{null_counts[null_counts > 0]}")
            else:
                print(f"  Nulls   : None")
        except Exception as e:
            print(f"[ERROR] Could not load {filename}: {e}")
    return datasets

if __name__ == "__main__":
    print("Loading all 10 datasets from data/raw/ ...")
    data = load_all_datasets()
    print(f"\n{'='*60}")
    print(f"Done. Successfully loaded {len(data)} / {len(CSV_FILES)} datasets.")