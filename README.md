# Customer Segmentation & Churn Pattern Analytics in European Banking

An end-to-end descriptive analytics project using the supplied `European_Bank.csv` dataset. It includes an interactive Streamlit dashboard, reproducible EDA scripts, research paper, executive summary, and technical documentation.

## Quick start (Windows / VS Code)

1. Extract the ZIP.
2. Open the `European_Bank_Churn_Analytics` folder in VS Code.
3. Open Terminal and run:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal, then activate again.
5. The dashboard should open in your browser. The CSV is included under `data/`.

## Run the reproducible analysis
```powershell
python analysis.py
```
Outputs are written to `reports/`, including segment summaries, KPI table, and charts.

## Project structure
- `app.py` — interactive Streamlit dashboard with filters, KPI cards, tabs and CSV export.
- `analysis.py` — reproducible exploratory analysis and CSV/PNG outputs.
- `data/European_Bank.csv` — supplied dataset.
- `research_paper.docx` and `.pdf` — research-style report; interpret findings as descriptive.
- `executive_summary.docx` and `.pdf` — short decision-maker summary.
- `TECHNICAL_DOCUMENTATION.md` — methodology, KPI definitions, data dictionary and limitations.
- `requirements.txt` — dependencies.

## Key results in the supplied dataset
- 10,000 customer records and 14 columns; no missing cells were detected.
- Overall observed churn rate: 20.37% (2,037 of 10,000 records).
- Germany has the highest observed geography-level churn rate (32.44%), compared with France (16.15%) and Spain (16.67%).
- Ages 46–60 have the highest observed age-band churn rate (51.12%) under the specified age bins.
- Inactive customers have a higher observed churn rate (26.85%) than active customers (14.27%).
- Product-count groups are uneven: the 3- and 4-product groups are small, so their high churn rates should be interpreted cautiously.

These are results from the provided file, not claims about all European banks. Confirm dataset provenance and definitions before external publication.

## Notes
- The `Year` column is retained in the dataset but is not required by the dashboard.
- This project is descriptive; it does not train a churn prediction model or prove causation.
- `Surname` is not used as an analytical feature in dashboard views.
