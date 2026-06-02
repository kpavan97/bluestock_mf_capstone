import pandas as pd
from pathlib import Path

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

# ─────────────────────────────────────────
# TASK 3: Load all 10 CSV datasets
# ─────────────────────────────────────────
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


# ─────────────────────────────────────────
# TASK 6: Explore fund_master
# ─────────────────────────────────────────
def explore_fund_master():
    fm = pd.read_csv(RAW_DIR / "01_fund_master.csv")

    print("\n" + "=" * 60)
    print("TASK 6: FUND MASTER EXPLORATION")
    print("=" * 60)
    print(f"\nShape   : {fm.shape}")
    print(f"Columns : {list(fm.columns)}")

    for col in fm.columns:
        if "fund" in col.lower() and "house" in col.lower():
            print(f"\nUnique Fund Houses ({fm[col].nunique()}):")
            print(fm[col].value_counts().to_string())

    for col in fm.columns:
        if "categ" in col.lower() and "sub" not in col.lower():
            print(f"\nUnique Categories ({fm[col].nunique()}):")
            print(fm[col].value_counts().to_string())

    for col in fm.columns:
        if "sub" in col.lower() and "categ" in col.lower():
            print(f"\nUnique Sub-Categories ({fm[col].nunique()}):")
            print(fm[col].value_counts().to_string())

    for col in fm.columns:
        if "risk" in col.lower():
            print(f"\nRisk Grades ({fm[col].nunique()}):")
            print(fm[col].value_counts().to_string())

    return fm


# ─────────────────────────────────────────
# TASK 7: Validate AMFI codes
# ─────────────────────────────────────────
def validate_amfi_codes(fm):
    print("\n" + "=" * 60)
    print("TASK 7: AMFI CODE VALIDATION")
    print("=" * 60)

    nh = pd.read_csv(RAW_DIR / "02_nav_history.csv")

    fm_code_col = [c for c in fm.columns if "code" in c.lower() or "amfi" in c.lower()][0]
    nh_code_col = [c for c in nh.columns if "code" in c.lower() or "amfi" in c.lower()][0]

    fm_codes  = set(fm[fm_code_col].astype(str).str.strip())
    nav_codes = set(nh[nh_code_col].astype(str).str.strip())

    missing_in_nav = fm_codes - nav_codes
    extra_in_nav   = nav_codes - fm_codes

    print(f"\nTotal schemes in fund_master : {len(fm_codes)}")
    print(f"Total schemes in nav_history : {len(nav_codes)}")
    print(f"\nCodes in fund_master MISSING from nav_history : {len(missing_in_nav)}")
    if missing_in_nav:
        print(f"  → {list(missing_in_nav)[:10]}")
    print(f"Codes in nav_history NOT in fund_master       : {len(extra_in_nav)}")

    print("\n--- DATA QUALITY SUMMARY ---")
    if not missing_in_nav:
        print("PASS: All fund_master AMFI codes exist in nav_history.")
    else:
        print(f"WARNING: {len(missing_in_nav)} codes in fund_master missing from nav_history.")


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("Loading all 10 datasets from data/raw/ ...")
    data = load_all_datasets()
    print(f"\nDone. Successfully loaded {len(data)} / {len(CSV_FILES)} datasets.")

    fm = explore_fund_master()
    validate_amfi_codes(fm)