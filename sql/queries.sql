-- ============================================================
-- queries.sql
-- Bluestock MF Capstone — 10 Analytical SQL Queries
-- ============================================================

-- Query 1: Top 5 funds by AUM
SELECT scheme_name, fund_house, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- Query 2: Average NAV per month for each fund
SELECT
    amfi_code,
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 4) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- Query 3: SIP inflow YoY growth
SELECT
    strftime('%Y', month) AS year,
    ROUND(SUM(sip_inflow_crore), 2) AS total_sip_inflow_crore,
    ROUND(AVG(yoy_growth_pct), 2) AS avg_yoy_growth_pct
FROM fact_sip
GROUP BY year
ORDER BY year;

-- Query 4: Total transactions by state
SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;

-- Query 5: Funds with expense_ratio < 1%
SELECT
    amfi_code,
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Query 6: Top 5 funds by Sharpe ratio
SELECT
    scheme_name,
    fund_house,
    ROUND(sharpe_ratio, 4) AS sharpe_ratio,
    ROUND(return_3yr_pct, 2) AS return_3yr_pct
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 5;

-- Query 7: Transaction split by type (SIP vs Lumpsum vs Redemption)
SELECT
    transaction_type,
    COUNT(*) AS count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS avg_amount_inr
FROM fact_transactions
GROUP BY transaction_type;

-- Query 8: AUM growth by fund house 2022 vs 2025
SELECT
    fund_house,
    ROUND(SUM(CASE WHEN strftime('%Y', date) = '2022' THEN aum_crore END), 0) AS aum_2022_crore,
    ROUND(SUM(CASE WHEN strftime('%Y', date) = '2025' THEN aum_crore END), 0) AS aum_2025_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY aum_2025_crore DESC;

-- Query 9: Top 10 stocks by total portfolio weight across all funds
SELECT
    stock_name,
    sector,
    ROUND(SUM(weight_pct), 2) AS total_weight_pct,
    COUNT(DISTINCT amfi_code) AS num_funds_holding
FROM fact_portfolio
GROUP BY stock_name, sector
ORDER BY total_weight_pct DESC
LIMIT 10;

-- Query 10: Investor count and avg SIP amount by age group
SELECT
    age_group,
    COUNT(DISTINCT investor_id) AS num_investors,
    ROUND(AVG(amount_inr), 2) AS avg_transaction_amount,
    ROUND(SUM(amount_inr), 2) AS total_invested
FROM fact_transactions
WHERE transaction_type = 'Sip'
GROUP BY age_group
ORDER BY total_invested DESC;