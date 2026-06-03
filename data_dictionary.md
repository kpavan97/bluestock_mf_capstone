# Data Dictionary — Bluestock MF Capstone

## 01_fund_master.csv / dim_fund
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | AMFI unique scheme code (Primary Key) |
| fund_house | TEXT | AMC name (e.g. SBI Mutual Fund) |
| scheme_name | TEXT | Full official AMFI scheme name |
| category | TEXT | Equity / Debt / Hybrid |
| sub_category | TEXT | Large Cap / Mid Cap / Small Cap / Liquid etc. |
| plan | TEXT | Regular or Direct |
| launch_date | DATE | Fund launch date (YYYY-MM-DD) |
| benchmark | TEXT | Official benchmark index |
| expense_ratio_pct | REAL | Annual expense ratio in % (range: 0.1–2.5) |
| exit_load_pct | REAL | Exit load % |
| fund_manager | TEXT | Name of primary fund manager |
| risk_category | TEXT | Low / Moderate / High / Very High |
| sebi_category_code | TEXT | EC01=LargeCap, EC03=SmallCap, DC01=Liquid |

## 02_nav_history.csv / fact_nav
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Foreign key to dim_fund |
| date | DATE | NAV date (business days only) |
| nav | REAL | NAV in Rs. (e.g. 892.45) |
| daily_return_pct | REAL | Daily % change in NAV (computed) |

## 03_aum_by_fund_house.csv / fact_aum
| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Quarter end date |
| fund_house | TEXT | AMC name |
| aum_lakh_crore | REAL | Total AUM in Rs. lakh crore |
| aum_crore | REAL | Total AUM in Rs. crore |
| num_schemes | INTEGER | Number of schemes under this AMC |

## 04_monthly_sip_inflows.csv / fact_sip
| Column | Type | Description |
|--------|------|-------------|
| month | DATE | Month (YYYY-MM) |
| sip_inflow_crore | REAL | Total SIP inflows in Rs. crore |
| active_sip_accounts_crore | REAL | Active SIP accounts in crore |
| new_sip_accounts_lakh | REAL | New SIP registrations in lakh |
| sip_aum_lakh_crore | REAL | Total SIP AUM in Rs. lakh crore |
| yoy_growth_pct | REAL | YoY growth % in SIP inflows |

## 05_category_inflows.csv / fact_category
| Column | Type | Description |
|--------|------|-------------|
| month | DATE | Month (YYYY-MM) |
| category | TEXT | Fund category (Large Cap, Mid Cap etc.) |
| net_inflow_crore | REAL | Net inflows in Rs. crore |

## 06_industry_folio_count.csv / fact_folio
| Column | Type | Description |
|--------|------|-------------|
| month | DATE | Month (YYYY-MM) |
| total_folios_crore | REAL | Total MF folios in crore |
| equity_folios_crore | REAL | Equity fund folios in crore |
| debt_folios_crore | REAL | Debt fund folios in crore |
| hybrid_folios_crore | REAL | Hybrid fund folios in crore |
| others_folios_crore | REAL | Other fund folios in crore |

## 07_scheme_performance.csv / fact_performance
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Foreign key to dim_fund |
| scheme_name | TEXT | Fund name |
| fund_house | TEXT | AMC name |
| return_1yr_pct | REAL | 1-year absolute return % |
| return_3yr_pct | REAL | 3-year CAGR % |
| return_5yr_pct | REAL | 5-year CAGR % |
| benchmark_3yr_pct | REAL | Benchmark 3yr CAGR % |
| alpha | REAL | Return above benchmark |
| beta | REAL | Sensitivity to market (1.0 = same as market) |
| sharpe_ratio | REAL | Risk-adjusted return (higher is better) |
| sortino_ratio | REAL | Like Sharpe but penalises only downside |
| std_dev_ann_pct | REAL | Annualised standard deviation % |
| max_drawdown_pct | REAL | Worst peak-to-trough decline (negative) |
| aum_crore | REAL | Fund AUM in Rs. crore |
| expense_ratio_pct | REAL | Annual expense ratio % |
| morningstar_rating | INTEGER | 1–5 star rating |
| risk_grade | TEXT | Low / Moderate / High / Very High |

## 08_investor_transactions.csv / fact_transactions
| Column | Type | Description |
|--------|------|-------------|
| investor_id | TEXT | Unique investor ID (INV000001 to INV005000) |
| transaction_date | DATE | Date of transaction |
| amfi_code | TEXT | Foreign key to dim_fund |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | REAL | Transaction amount in Rs. |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| city_tier | TEXT | T30 (Top 30 cities) or B30 (Beyond Top 30) |
| age_group | TEXT | 18-25 / 26-35 / 36-45 / 46-55 / 56+ |
| gender | TEXT | Male / Female |
| annual_income_lakh | REAL | Annual income in Rs. lakh |
| payment_mode | TEXT | UPI / Net Banking / Mandate / Cheque |
| kyc_status | TEXT | Verified / Pending |

## 09_portfolio_holdings.csv / fact_portfolio
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Foreign key to dim_fund |
| stock_symbol | TEXT | NSE stock symbol |
| stock_name | TEXT | Company name |
| sector | TEXT | Sector (IT, Banking, FMCG etc.) |
| weight_pct | REAL | Weight % of stock in fund portfolio |
| market_value_cr | REAL | Market value in Rs. crore |
| current_price_inr | REAL | Current stock price in Rs. |
| portfolio_date | DATE | Portfolio as-of date |

## 10_benchmark_indices.csv / fact_benchmark
| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Trading date |
| index_name | TEXT | NIFTY50 / NIFTY100 / NIFTYMIDCAP150 etc. |
| close_value | REAL | Closing index value |
