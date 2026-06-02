import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"

def explore_fund_master():
    fm = pd.read_csv(RAW_DIR / "01_fund_master.csv")

    print("=" * 60)
    print("TASK 6: FUND MASTER EXPLORATION")
    print("=" * 60)

    print(f"\nShape: {fm.shape}")
    print(f"\nColumns: {list(fm.columns)}")

    print(f"\nUnique Fund Houses ({fm.iloc[:, 0].nunique()}):")
    print(fm.iloc[:, 0].value_counts().to_string())

    print(f"\nUnique Categories:")
    for col in fm.columns:
        if "categ" in col.lower():
            print(f"\n  [{col}] — {fm[col].nunique()} unique values:")
            print(fm[col].value_counts().to_string())

    print(f"\nUnique Sub-Categories:")
    for col in fm.columns:
        if "sub" in col.lower():
            print(f"\n  [{col}] — {fm[col].nunique()} unique values:")
            print(fm[col].value_counts().to_string())

    print(f"\nRisk Grades:")
    for col in fm.columns:
        if "risk" in col.lower():
            print(f"\n  [{col}]:")
            print(fm[col].value_counts().to_string())

    return fm

def validate_amfi_codes(fm):
    print("\n" + "=" * 60)
    print("TASK 7: AMFI CODE VALIDATION")
    print("=" * 60)

    nh = pd.read_csv(RAW_DIR / "02_nav_history.csv")

    print(f"\nfund_master columns : {list(fm.columns)}")
    print(f"nav_history columns : {list(nh.columns)}")

    # Find scheme code column in fund_master
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
        print(f"WARNING: {len(missing_in_nav)} codes in fund_master are missing from nav_history.")
    print("Validation complete.")

if __name__ == "__main__":
    fm = explore_fund_master()
    validate_amfi_codes(fm)