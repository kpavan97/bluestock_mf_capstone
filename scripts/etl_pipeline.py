"""
etl_pipeline.py
Day 2: Data Cleaning + SQLite Database Load
Bluestock Fintech MF Capstone
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sqlalchemy import create_engine

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent
RAW_DIR    = BASE_DIR / "data" / "raw"
PROC_DIR   = BASE_DIR / "data" / "processed"
DB_PATH    = BASE_DIR / "data" / "db" / "bluestock_mf.db"

PROC_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════
# TASK 1 — Clean nav_history.csv
# ═══════════════════════════════════════════════════════════════════════════
def clean_nav_history():
    print("\n── TASK 1: Cleaning nav_history.csv ──")
    df = pd.read_csv(RAW_DIR / "02_nav_history.csv")

    # Parse date to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["amfi_code", "date"])
    print(f"  Duplicates removed : {before - len(df)}")

    # Sort by amfi_code + date
    df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)

    # Forward-fill missing NAV for weekends/holidays
    df = (
        df.set_index("date")
        .groupby("amfi_code")["nav"]
        .apply(lambda x: x.reindex(
            pd.date_range(x.index.min(), x.index.max(), freq="D")
        ).ffill())
        .reset_index()
    )
    df.columns = ["amfi_code", "date", "nav"]

    # Validate NAV > 0
    invalid = df[df["nav"] <= 0]
    if not invalid.empty:
        print(f"  Invalid NAV <= 0 rows: {len(invalid)} — dropping")
        df = df[df["nav"] > 0]

    # Compute daily return
    df = df.sort_values(["amfi_code", "date"])
    df["daily_return_pct"] = (
        df.groupby("amfi_code")["nav"].pct_change() * 100
    )

    out = PROC_DIR / "clean_nav.csv"
    df.to_csv(out, index=False)
    print(f"  Saved → clean_nav.csv | Shape: {df.shape}")
    return df


# ═══════════════════════════════════════════════════════════════════════════
# TASK 2 — Clean investor_transactions.csv
# ═══════════════════════════════════════════════════════════════════════════
def clean_transactions():
    print("\n── TASK 2: Cleaning investor_transactions.csv ──")
    df = pd.read_csv(RAW_DIR / "08_investor_transactions.csv")

    # Fix date format
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    # Standardise transaction_type
    df["transaction_type"] = df["transaction_type"].str.strip().str.title()
    valid_types = ["Sip", "Lumpsum", "Redemption"]
    invalid_types = df[~df["transaction_type"].isin(valid_types)]
    if not invalid_types.empty:
        print(f"  Invalid transaction types: {invalid_types['transaction_type'].unique()}")
    df = df[df["transaction_type"].isin(valid_types)]

    # Validate amount > 0
    before = len(df)
    df = df[df["amount_inr"] > 0]
    print(f"  Rows with amount <= 0 removed: {before - len(df)}")

    # Check KYC status values
    print(f"  KYC status values: {df['kyc_status'].unique()}")

    # Remove duplicates
    df = df.drop_duplicates()

    out = PROC_DIR / "clean_transactions.csv"
    df.to_csv(out, index=False)
    print(f"  Saved → clean_transactions.csv | Shape: {df.shape}")
    return df


# ═══════════════════════════════════════════════════════════════════════════
# TASK 3 — Clean scheme_performance.csv
# ═══════════════════════════════════════════════════════════════════════════
def clean_performance():
    print("\n── TASK 3: Cleaning scheme_performance.csv ──")
    df = pd.read_csv(RAW_DIR / "07_scheme_performance.csv")

    # Validate return values are numeric
    return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
                   "sharpe_ratio", "sortino_ratio", "alpha", "beta"]
    for col in return_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Flag negative Sharpe ratios
    neg_sharpe = df[df["sharpe_ratio"] < 0]
    print(f"  Funds with negative Sharpe ratio: {len(neg_sharpe)}")
    if not neg_sharpe.empty:
        print(f"  → {neg_sharpe['scheme_name'].tolist()}")

    # Check expense_ratio range (0.1% - 2.5%)
    out_of_range = df[
        (df["expense_ratio_pct"] < 0.1) | (df["expense_ratio_pct"] > 2.5)
    ]
    print(f"  Expense ratio out of range (0.1-2.5%): {len(out_of_range)}")

    out = PROC_DIR / "clean_performance.csv"
    df.to_csv(out, index=False)
    print(f"  Saved → clean_performance.csv | Shape: {df.shape}")
    return df


# ═══════════════════════════════════════════════════════════════════════════
# Clean remaining CSVs (pass-through with type fixes)
# ═══════════════════════════════════════════════════════════════════════════
def clean_remaining():
    print("\n── Cleaning remaining CSVs ──")

    # fund_master
    df = pd.read_csv(RAW_DIR / "01_fund_master.csv")
    df["launch_date"] = pd.to_datetime(df["launch_date"])
    df.to_csv(PROC_DIR / "clean_fund_master.csv", index=False)
    print(f"  clean_fund_master.csv | Shape: {df.shape}")

    # aum_by_fund_house
    df = pd.read_csv(RAW_DIR / "03_aum_by_fund_house.csv")
    df["date"] = pd.to_datetime(df["date"])
    df.to_csv(PROC_DIR / "clean_aum.csv", index=False)
    print(f"  clean_aum.csv | Shape: {df.shape}")

    # monthly_sip_inflows
    df = pd.read_csv(RAW_DIR / "04_monthly_sip_inflows.csv")
    df["month"] = pd.to_datetime(df["month"])
    df["yoy_growth_pct"] = df["yoy_growth_pct"].fillna(0)
    df.to_csv(PROC_DIR / "clean_sip.csv", index=False)
    print(f"  clean_sip.csv | Shape: {df.shape}")

    # category_inflows
    df = pd.read_csv(RAW_DIR / "05_category_inflows.csv")
    df["month"] = pd.to_datetime(df["month"])
    df.to_csv(PROC_DIR / "clean_category_inflows.csv", index=False)
    print(f"  clean_category_inflows.csv | Shape: {df.shape}")

    # industry_folio_count
    df = pd.read_csv(RAW_DIR / "06_industry_folio_count.csv")
    df["month"] = pd.to_datetime(df["month"])
    df.to_csv(PROC_DIR / "clean_folio_count.csv", index=False)
    print(f"  clean_folio_count.csv | Shape: {df.shape}")

    # portfolio_holdings
    df = pd.read_csv(RAW_DIR / "09_portfolio_holdings.csv")
    df["portfolio_date"] = pd.to_datetime(df["portfolio_date"])
    df.to_csv(PROC_DIR / "clean_portfolio_holdings.csv", index=False)
    print(f"  clean_portfolio_holdings.csv | Shape: {df.shape}")

    # benchmark_indices
    df = pd.read_csv(RAW_DIR / "10_benchmark_indices.csv")
    df["date"] = pd.to_datetime(df["date"])
    df.to_csv(PROC_DIR / "clean_benchmark_indices.csv", index=False)
    print(f"  clean_benchmark_indices.csv | Shape: {df.shape}")


# ═══════════════════════════════════════════════════════════════════════════
# TASK 5 — Load all cleaned data into SQLite
# ═══════════════════════════════════════════════════════════════════════════
def load_to_sqlite():
    print("\n── TASK 5: Loading data into SQLite ──")
    engine = create_engine(f"sqlite:///{DB_PATH}")

    tables = {
        "dim_fund"         : PROC_DIR / "clean_fund_master.csv",
        "fact_nav"         : PROC_DIR / "clean_nav.csv",
        "fact_transactions": PROC_DIR / "clean_transactions.csv",
        "fact_performance" : PROC_DIR / "clean_performance.csv",
        "fact_aum"         : PROC_DIR / "clean_aum.csv",
        "fact_sip"         : PROC_DIR / "clean_sip.csv",
        "fact_category"    : PROC_DIR / "clean_category_inflows.csv",
        "fact_folio"       : PROC_DIR / "clean_folio_count.csv",
        "fact_portfolio"   : PROC_DIR / "clean_portfolio_holdings.csv",
        "fact_benchmark"   : PROC_DIR / "clean_benchmark_indices.csv",
    }

    for table_name, filepath in tables.items():
        df = pd.read_csv(filepath)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"  Loaded {table_name} → {len(df)} rows")

    print(f"\n  Database saved → data/db/bluestock_mf.db")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("ETL PIPELINE — Bluestock MF Capstone")
    print("=" * 60)

    clean_nav_history()
    clean_transactions()
    clean_performance()
    clean_remaining()
    load_to_sqlite()

    print("\n" + "=" * 60)
    print("ETL PIPELINE COMPLETE")
    print("=" * 60)
