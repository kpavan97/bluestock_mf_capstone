-- ============================================================
-- schema.sql
-- Bluestock MF Capstone — SQLite Star Schema
-- ============================================================

-- Dimension: Fund Master
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code           TEXT PRIMARY KEY,
    fund_house          TEXT NOT NULL,
    scheme_name         TEXT NOT NULL,
    category            TEXT,
    sub_category        TEXT,
    plan                TEXT,
    launch_date         DATE,
    benchmark           TEXT,
    expense_ratio_pct   REAL,
    exit_load_pct       REAL,
    fund_manager        TEXT,
    risk_category       TEXT,
    sebi_category_code  TEXT
);

-- Fact: Daily NAV History
CREATE TABLE IF NOT EXISTS fact_nav (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code           TEXT NOT NULL,
    date                DATE NOT NULL,
    nav                 REAL NOT NULL,
    daily_return_pct    REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Investor Transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id         TEXT NOT NULL,
    transaction_date    DATE NOT NULL,
    amfi_code           TEXT NOT NULL,
    transaction_type    TEXT NOT NULL,
    amount_inr          REAL NOT NULL,
    state               TEXT,
    city                TEXT,
    city_tier           TEXT,
    age_group           TEXT,
    gender              TEXT,
    annual_income_lakh  REAL,
    payment_mode        TEXT,
    kyc_status          TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Scheme Performance
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code           TEXT PRIMARY KEY,
    scheme_name         TEXT,
    fund_house          TEXT,
    return_1yr_pct      REAL,
    return_3yr_pct      REAL,
    return_5yr_pct      REAL,
    benchmark_3yr_pct   REAL,
    alpha               REAL,
    beta                REAL,
    sharpe_ratio        REAL,
    sortino_ratio       REAL,
    std_dev_ann_pct     REAL,
    max_drawdown_pct    REAL,
    aum_crore           REAL,
    expense_ratio_pct   REAL,
    morningstar_rating  INTEGER,
    risk_grade          TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: AUM by Fund House
CREATE TABLE IF NOT EXISTS fact_aum (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date            DATE NOT NULL,
    fund_house      TEXT NOT NULL,
    aum_lakh_crore  REAL,
    aum_crore       REAL,
    num_schemes     INTEGER
);

-- Fact: Monthly SIP Inflows
CREATE TABLE IF NOT EXISTS fact_sip (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    month                       DATE NOT NULL,
    sip_inflow_crore            REAL,
    active_sip_accounts_crore   REAL,
    new_sip_accounts_lakh       REAL,
    sip_aum_lakh_crore          REAL,
    yoy_growth_pct              REAL
);

-- Fact: Portfolio Holdings
CREATE TABLE IF NOT EXISTS fact_portfolio (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code           TEXT NOT NULL,
    stock_symbol        TEXT,
    stock_name          TEXT,
    sector              TEXT,
    weight_pct          REAL,
    market_value_cr     REAL,
    current_price_inr   REAL,
    portfolio_date      DATE,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Benchmark Indices
CREATE TABLE IF NOT EXISTS fact_benchmark (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        DATE NOT NULL,
    index_name  TEXT NOT NULL,
    close_value REAL NOT NULL
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_nav_code ON fact_nav(amfi_code);
CREATE INDEX IF NOT EXISTS idx_nav_date ON fact_nav(date);
CREATE INDEX IF NOT EXISTS idx_txn_date ON fact_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_txn_code ON fact_transactions(amfi_code);
CREATE INDEX IF NOT EXISTS idx_bench_date ON fact_benchmark(date);