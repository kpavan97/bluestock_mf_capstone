import pandas as pd
from pathlib import Path

PROC_DIR = Path('P:/bluestock_mf_capstone/data/processed')

def recommend_funds(risk_appetite):
    perf = pd.read_csv(PROC_DIR / 'clean_performance.csv')
    
    if risk_appetite not in ['Low','Moderate','High']:
        print("Invalid input. Choose: Low / Moderate / High")
        return
    
    filtered = perf[perf['risk_grade'] == risk_appetite].copy()
    
    top3 = filtered.nlargest(3, 'sharpe_ratio')[
        ['scheme_name','fund_house','sharpe_ratio',
         'return_3yr_pct','risk_grade','expense_ratio_pct']
    ].reset_index(drop=True)
    
    top3.index = top3.index + 1
    
    print(f"\nTop 3 Recommendations for {risk_appetite} Risk:")
    print("=" * 60)
    print(top3.to_string())
    print("=" * 60)

if __name__ == "__main__":
    risk = input("Enter risk appetite (Low / Moderate / High): ")
    recommend_funds(risk)