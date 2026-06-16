"""
compute_metrics.py
Bluestock MF Capstone — Performance Metrics Computation
Computes Sharpe, Sortino, Alpha, Beta, CAGR, Max Drawdown for all 40 funds.
Run: python scripts/compute_metrics.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
PROC_DIR = BASE_DIR / "data" / "processed"
OUT_DIR  = BASE_DIR / "data" / "processed"

RF       = 6.5 / 100        # RBI repo rate — risk free rate
RF_DAILY = RF / 252         # daily risk free rate


def load_data():
    nav   = pd.read_csv(PROC_DIR / "clean_nav.csv",   parse_dates=["date"])
    fund  = pd.read_csv(PROC_DIR / "clean_fund_master.csv")
    bench = pd.read_csv(PROC_DIR / "clean_benchmark_indices.csv", parse_dates=["date"])
    nav_named = nav.merge(fund[["amfi_code","scheme_name","fund_house","expense_ratio_pct"]], on="amfi_code", how="left")
    nav_sorted = nav_named.sort_values(["amfi_code","date"])
    nav_sorted["daily_return"] = nav_sorted.groupby("amfi_code")["nav"].pct_change()
    return nav_sorted, bench


def compute_cagr(group, years):
    end_date   = group["date"].max()
    start_date = end_date - pd.DateOffset(years=years)
    subset     = group[group["date"] >= start_date]
    if len(subset) < 2:
        return np.nan
    nav_start = subset.iloc[0]["nav"]
    nav_end   = subset.iloc[-1]["nav"]
    n_days    = (subset.iloc[-1]["date"] - subset.iloc[0]["date"]).days
    n_years   = n_days / 365.25
    if n_years <= 0 or nav_start <= 0:
        return np.nan
    return ((nav_end / nav_start) ** (1 / n_years) - 1) * 100


def compute_all_metrics(nav_sorted, bench):
    nifty100 = bench[bench["index_name"] == "NIFTY100"].sort_values("date").copy()
    nifty100["bench_return"] = nifty100["close_value"].pct_change()

    results = []
    for code, group in nav_sorted.groupby("amfi_code"):
        name    = group["scheme_name"].iloc[0]
        house   = group["fund_house"].iloc[0]
        expense = group["expense_ratio_pct"].iloc[0]
        returns = group["daily_return"].dropna()

        if len(returns) < 30:
            continue

        # CAGR
        cagr_1yr = compute_cagr(group, 1)
        cagr_3yr = compute_cagr(group, 3)
        cagr_5yr = compute_cagr(group, 5)

        # Sharpe
        excess = returns - RF_DAILY
        sharpe = (excess.mean() / excess.std()) * np.sqrt(252)

        # Sortino
        downside     = excess[excess < 0]
        downside_std = downside.std()
        sortino      = (excess.mean() / downside_std) * np.sqrt(252) if downside_std > 0 else np.nan

        # Alpha and Beta
        merged = group[["date","daily_return"]].merge(
            nifty100[["date","bench_return"]], on="date", how="inner").dropna()
        if len(merged) >= 30:
            slope, intercept, r_value, _, _ = stats.linregress(
                merged["bench_return"], merged["daily_return"])
            alpha = intercept * 252 * 100
            beta  = slope
            r_sq  = r_value ** 2
        else:
            alpha = beta = r_sq = np.nan

        # Max Drawdown
        rolling_max = group["nav"].cummax()
        drawdown    = (group["nav"] / rolling_max - 1)
        max_dd      = drawdown.min() * 100

        # VaR and CVaR
        var_95  = np.percentile(returns, 5) * 100
        cvar_95 = returns[returns <= np.percentile(returns, 5)].mean() * 100

        results.append({
            "amfi_code"       : code,
            "scheme_name"     : name,
            "fund_house"      : house,
            "expense_ratio_pct": expense,
            "cagr_1yr_pct"    : round(cagr_1yr, 2),
            "cagr_3yr_pct"    : round(cagr_3yr, 2),
            "cagr_5yr_pct"    : round(cagr_5yr, 2),
            "sharpe_ratio"    : round(sharpe, 4),
            "sortino_ratio"   : round(sortino, 4) if not np.isnan(sortino) else np.nan,
            "alpha"           : round(alpha, 4) if not np.isnan(alpha) else np.nan,
            "beta"            : round(beta, 4) if not np.isnan(beta) else np.nan,
            "r_squared"       : round(r_sq, 4) if not np.isnan(r_sq) else np.nan,
            "max_drawdown_pct": round(max_dd, 2),
            "var_95_pct"      : round(var_95, 4),
            "cvar_95_pct"     : round(cvar_95, 4),
        })

    df = pd.DataFrame(results)
    df.to_csv(OUT_DIR / "computed_metrics.csv", index=False)
    print(f"Metrics computed for {len(df)} funds")
    print(f"Saved to computed_metrics.csv")
    return df


if __name__ == "__main__":
    print("=" * 50)
    print("COMPUTING PERFORMANCE METRICS")
    print("=" * 50)
    nav_sorted, bench = load_data()
    metrics_df = compute_all_metrics(nav_sorted, bench)
    print("\nTop 5 by Sharpe Ratio:")
    print(metrics_df.nlargest(5, "sharpe_ratio")[["scheme_name","sharpe_ratio","cagr_3yr_pct"]].to_string())
    print("\nDone.")
