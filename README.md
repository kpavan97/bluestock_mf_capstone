# Bluestock MF Capstone — Mutual Fund Analytics Platform

**Bluestock Fintech Pvt. Ltd. | Individual Capstone | June 2026**

---

## Project Overview

A full-stack Mutual Fund Analytics Platform built using publicly available Indian mutual fund data from AMFI India and mfapi.in. The platform ingests raw NAV, AUM, and SIP data, cleans and stores it in a relational database, performs exploratory and performance analytics, and presents insights via an interactive Power BI dashboard.

---

## Tech Stack

Python 3.10 · Pandas · NumPy · Matplotlib · Seaborn · Plotly · SQLite · SQLAlchemy · SciPy · Jupyter · Power BI Desktop · Git + GitHub · mfapi.in REST API

---

## Folder Structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw/           — original downloaded CSV files
│   ├── processed/     — cleaned, merged CSVs
│   └── db/            — bluestock_mf.db (SQLite)
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── etl_pipeline.py      — master ETL script
│   ├── live_nav_fetch.py    — mfapi.in NAV fetcher
│   ├── data_ingestion.py    — load and validate CSVs
│   ├── compute_metrics.py   — performance metrics
│   └── recommender.py       — fund recommendation engine
├── sql/
│   ├── schema.sql            — CREATE TABLE statements
│   └── queries.sql           — 10 analytical SQL queries
├── dashboard/
│   └── bluestock_mf_dashboard.pbix
├── reports/
│   ├── Final_Report.pdf
│   ├── Presentation.pptx
│   └── charts/              — exported PNG charts
├── run_pipeline.py           — master run script
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/kpavan97/bluestock_mf_capstone.git
cd bluestock_mf_capstone
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add raw CSV files
Copy all 10 provided CSV files into:
```
data/raw/
```

### 5. Run the full ETL pipeline
```bash
python run_pipeline.py
```

This will:
- Load and validate all 10 CSV files
- Fetch live NAV from mfapi.in
- Clean all datasets
- Load into SQLite database at data/db/bluestock_mf.db

### 6. Run Jupyter Notebooks
```bash
jupyter notebook
```
Open notebooks in order: 03 → 04 → 05

### 7. Open Power BI Dashboard
Open `dashboard/bluestock_mf_dashboard.pbix` in Power BI Desktop.

---

## Dataset Descriptions

| File | Rows | Description |
|------|------|-------------|
| 01_fund_master.csv | 40 | 40 AMFI schemes with codes, fund house, expense ratio |
| 02_nav_history.csv | 46,000 | Daily NAV Jan 2022 to May 2026 |
| 03_aum_by_fund_house.csv | 90 | Quarterly AUM for top 10 AMCs |
| 04_monthly_sip_inflows.csv | 48 | Monthly SIP inflows Jan 2022 to Dec 2025 |
| 05_category_inflows.csv | 144 | Net inflows by fund category |
| 06_industry_folio_count.csv | 21 | Total MF folios growth |
| 07_scheme_performance.csv | 40 | Sharpe, Sortino, Alpha, Beta, CAGR |
| 08_investor_transactions.csv | 32,000+ | SIP/Lumpsum/Redemption transactions |
| 09_portfolio_holdings.csv | 320 | Top stock holdings per fund |
| 10_benchmark_indices.csv | 8,050 | Nifty 50, Nifty 100, BSE SmallCap daily values |

---

## Key Results

- SBI MF leads AUM at Rs.12.5 lakh crore (Dec 2025)
- Industry SIP inflows hit all-time high of Rs.31,002 crore (Dec 2025)
- Total MF folios doubled from 13.26 Cr to 26.12 Cr (2022-2025)
- 26-35 age group accounts for highest SIP investor share
- Banking sector dominates equity fund portfolios at 25%+

---

## Deliverables

| ID | Deliverable | File |
|----|-------------|------|
| D1 | ETL Pipeline | scripts/etl_pipeline.py |
| D2 | SQLite Database | data/db/bluestock_mf.db |
| D3 | EDA Notebook | notebooks/03_eda_analysis.ipynb |
| D4 | Performance Metrics | notebooks/04_performance_analytics.ipynb |
| D5 | Interactive Dashboard | dashboard/bluestock_mf_dashboard.pbix |
| D6 | Advanced Analytics | notebooks/05_advanced_analytics.ipynb |
| D7 | Final Report + Slides | reports/Final_Report.pdf + Presentation.pptx |

---

## Author

Intern — Data Analyst
Bluestock Fintech Pvt. Ltd.
June 2026
