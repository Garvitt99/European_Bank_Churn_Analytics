"""Reproducible EDA report generator for European banking churn dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "European_Bank.csv"
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA)
df["AgeGroup"] = pd.cut(df["Age"], [0,29,45,60,120], labels=["Under 30","30–45","46–60","Over 60"])
df["CreditBand"] = pd.cut(df["CreditScore"], [-1,579,669,850], labels=["Low","Medium","High"])
df["TenureGroup"] = pd.cut(df["Tenure"], [-1,2,6,10], labels=["New (0–2y)","Mid-term (3–6y)","Long-term (7–10y)"])
summary = pd.DataFrame({
    "Metric": ["Rows", "Columns", "Missing cells", "Duplicate rows", "Churned", "Retained", "Overall churn rate (%)"],
    "Value": [len(df), len(df.columns), int(df.isna().sum().sum()), int(df.duplicated().sum()),
              int(df.Exited.sum()), int((df.Exited==0).sum()), round(df.Exited.mean()*100, 2)]
})
summary.to_csv(OUT/"data_quality_and_kpis.csv", index=False)
for col in ["Geography","Gender","AgeGroup","CreditBand","TenureGroup","NumOfProducts","IsActiveMember"]:
    out = df.groupby(col, observed=False).agg(Customers=("Exited","size"), Churned=("Exited","sum"), Churn_Rate=("Exited","mean")).reset_index()
    out["Churn_Rate_Pct"] = (out["Churn_Rate"]*100).round(2)
    out.to_csv(OUT/f"segment_{str(col).lower()}.csv", index=False)
plt.figure(figsize=(8,5))
(df.groupby("Geography").Exited.mean()*100).sort_values(ascending=False).plot(kind="bar")
plt.title("Churn Rate by Geography"); plt.ylabel("Churn rate (%)"); plt.tight_layout()
plt.savefig(OUT/"churn_by_geography.png", dpi=160); plt.close()
plt.figure(figsize=(8,5))
(df.groupby("AgeGroup", observed=False).Exited.mean()*100).plot(kind="bar")
plt.title("Churn Rate by Age Group"); plt.ylabel("Churn rate (%)"); plt.tight_layout()
plt.savefig(OUT/"churn_by_age.png", dpi=160); plt.close()
print(f"EDA outputs saved to {OUT}")
