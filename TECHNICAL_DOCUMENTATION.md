# Technical Documentation

## Objective
Describe customer churn patterns across geography, age, gender, credit score, tenure, activity, products, balance and salary in the supplied customer-level dataset.

## Data validation
The analysis checks the required columns, missing values, duplicates and the binary target (`Exited`: 1 = churned, 0 = retained). The supplied file contains 10,000 rows and 14 columns; no missing cells were observed at preparation time. The dashboard validates required columns and removes rows where the target is missing.

## Derived segments
- Age: Under 30 (≤29), 30–45, 46–60, Over 60.
- Credit score: Low ≤579, Medium 580–669, High ≥670.
- Tenure: New 0–2 years, Mid-term 3–6 years, Long-term 7–10 years.
- Balance: zero balance; low balance; high balance. In the dashboard's premium explorer, high balance is the top quartile of the filtered sample and is recalculated after filters.

## KPIs
- Overall churn rate = sum(Exited) / number of valid customers × 100.
- Segment churn rate = churned customers in segment / all customers in segment × 100.
- High-balance churn = churn rate among customers at or above the filtered balance 75th percentile.
- Geographic risk index = geography churn rate / overall filtered churn rate × 100. An index of 100 represents the filtered average.
- Engagement drop indicator = compare churn rates for inactive and active members. This is an association, not evidence that inactivity causes churn.

## Application
Streamlit + pandas for data handling, Plotly Express for interactive charts. Filters apply to geography, gender, age range and activity status. CSV export downloads the filtered records.

## Reproducibility
Install dependencies with `pip install -r requirements.txt`, run `streamlit run app.py`, and run `python analysis.py` for static CSV/PNG outputs.

## Privacy and responsible use
Avoid exposing customer-level exports to unauthorized people. Customer IDs and other fields should be handled according to applicable privacy rules. Use aggregate views for presentations. Validate data origin, consent, and permitted use before sharing results.

## Limitations
The analysis is descriptive and does not infer causality. The supplied file's provenance is not verified here. Small groups, especially customers with 3 or 4 products, can produce unstable rates. Balance is only a proxy for customer value; it does not account for margin, liabilities, product profitability, service cost or lifetime value. No model validation or out-of-time testing is included.
