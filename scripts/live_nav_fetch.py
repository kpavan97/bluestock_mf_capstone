import requests
import pandas as pd
from pathlib import Path
import time

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SCHEMES = {
    125497: "HDFC_Top100",
    119551: "SBI_Bluechip",
    120503: "ICICI_Bluechip",
    118632: "Nippon_LargeCap",
    119092: "Axis_Bluechip",
    120841: "Kotak_Bluechip",
}

BASE_URL = "https://api.mfapi.in/mf/{}"

def fetch_nav(scheme_code, scheme_name):
    url = BASE_URL.format(scheme_code)
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        meta        = data.get("meta", {})
        nav_records = data.get("data", [])

        df = pd.DataFrame(nav_records)
        df["scheme_code"] = scheme_code
        df["scheme_name"] = meta.get("scheme_name", scheme_name)
        df["fund_house"]  = meta.get("fund_house", "")
        df["scheme_type"] = meta.get("scheme_type", "")
        df["date"]        = pd.to_datetime(df["date"], format="%d-%m-%Y")
        df["nav"]         = pd.to_numeric(df["nav"], errors="coerce")
        df = df.sort_values("date").reset_index(drop=True)

        out_path = RAW_DIR / f"nav_{scheme_name}.csv"
        df.to_csv(out_path, index=False)
        print(f"  [OK] {scheme_name} — {len(df)} rows saved → {out_path.name}")
        return df

    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] {scheme_name} (code={scheme_code}): {e}")
        return None

if __name__ == "__main__":
    print("Fetching live NAV data from mfapi.in ...\n")
    all_frames = []

    for code, name in SCHEMES.items():
        print(f"Fetching: {name} (code={code})")
        df = fetch_nav(code, name)
        if df is not None:
            all_frames.append(df)
        time.sleep(1)

    if all_frames:
        combined     = pd.concat(all_frames, ignore_index=True)
        combined_path = RAW_DIR / "nav_all_schemes_combined.csv"
        combined.to_csv(combined_path, index=False)
        print(f"\nCombined file saved → nav_all_schemes_combined.csv")
        print(f"Total records fetched: {len(combined)}")

    print("\nDone. All NAV files saved in data/raw/")