

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

def run_script(script_path, description):
    print(f"\n{'='*55}")
    print(f"Running: {description}")
    print(f"{'='*55}")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=False
    )
    if result.returncode == 0:
        print(f"DONE: {description}")
    else:
        print(f"ERROR in: {description}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 55)
    print("BLUESTOCK MF CAPSTONE — MASTER PIPELINE")
    print("=" * 55)

    run_script(BASE_DIR / "scripts" / "data_ingestion.py",
               "Step 1: Data Ingestion")

    run_script(BASE_DIR / "scripts" / "live_nav_fetch.py",
               "Step 2: Live NAV Fetch")

    run_script(BASE_DIR / "scripts" / "etl_pipeline.py",
               "Step 3: ETL Pipeline — Clean + Load DB")

    run_script(BASE_DIR / "scripts" / "recommender.py",
               "Step 4: Fund Recommender")

    print("\n" + "=" * 55)
    print("PIPELINE COMPLETE")
    print("All cleaned CSVs saved to data/processed/")
    print("Database saved to data/db/bluestock_mf.db")
    print("=" * 55)
