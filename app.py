from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="European Banking | Churn Analytics", page_icon="🏦", layout="wide")
ROOT = Path(__file__).resolve().parent
DATA_CANDIDATES = [ROOT / "data" / "European_Bank.csv", ROOT / "European_Bank.csv", ROOT.parent / "data" / "European_Bank.csv"]

@st.cache_data
def load_data():
    for path in DATA_CANDIDATES:
        if path.exists():
            data = pd.read_csv(path)
            break
    else:
        uploaded = st.file_uploader("Upload European_Bank.csv", type=["csv"])
        if uploaded is None:
            return pd.DataFrame()
        data = pd.read_csv(uploaded)
    required = {"CustomerId","CreditScore","Geography","Gender","Age","Tenure","Balance","NumOfProducts","HasCrCard","IsActiveMember","EstimatedSalary","Exited"}
    missing = required - set(data.columns)
    if missing:
        st.error(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
        return pd.DataFrame()
    data = data.copy()
    data["Exited"] = pd.to_numeric(data["Exited"], errors="coerce")
    data = data.dropna(subset=["Exited"])
    data["Exited"] = data["Exited"].astype(int)
    data["AgeGroup"] = pd.cut(data["Age"], bins=[0,29,45,60,120], labels=["Under 30","30–45","46–60","Over 60"], include_lowest=True)
    data["CreditBand"] = pd.cut(data["CreditScore"], bins=[-1,579,669,850], labels=["Low","Medium","High"])
    data["TenureGroup"] = pd.cut(data["Tenure"], bins=[-1,2,6,10], labels=["New (0–2y)","Mid-term (3–6y)","Long-term (7–10y)"])
    data["BalanceSegment"] = pd.cut(data["Balance"], bins=[-0.01,0,75000, float("inf")], labels=["Zero balance","Low balance","High balance"])
    data["CustomerStatus"] = data["Exited"].map({0:"Retained",1:"Churned"})
    return data

df = load_data()
st.title("Customer Segmentation & Churn Pattern Analytics")
st.caption("European Banking • Interactive descriptive analytics • Dataset supplied for this project")
if df.empty:
    st.info("Place the dataset at data/European_Bank.csv or upload it above.")
    st.stop()

st.sidebar.header("Explore segments")
geographies = sorted(df["Geography"].dropna().astype(str).unique().tolist())
genders = sorted(df["Gender"].dropna().astype(str).unique().tolist())
geo = st.sidebar.multiselect("Geography", geographies, default=geographies)
gender = st.sidebar.multiselect("Gender", genders, default=genders)
age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))
active_choice = st.sidebar.selectbox("Activity status", ["All","Active","Inactive"])
filtered = df[df["Geography"].isin(geo) & df["Gender"].isin(gender) & df["Age"].between(*age_range)].copy()
if active_choice == "Active":
    filtered = filtered[filtered["IsActiveMember"] == 1]
elif active_choice == "Inactive":
    filtered = filtered[filtered["IsActiveMember"] == 0]
if filtered.empty:
    st.warning("No customers match these filters.")
    st.stop()

n = len(filtered)
churn_n = int(filtered["Exited"].sum())
churn_rate = filtered["Exited"].mean() * 100
high_value = filtered[filtered["Balance"] >= filtered["Balance"].quantile(.75)]
high_value_churn = high_value["Exited"].mean() * 100 if len(high_value) else 0
inactive_rate = filtered.loc[filtered["IsActiveMember"] == 0, "Exited"].mean() * 100 if (filtered["IsActiveMember"] == 0).any() else 0

c1,c2,c3,c4 = st.columns(4)
c1.metric("Customers in view", f"{n:,}")
c2.metric("Churn rate", f"{churn_rate:.1f}%")
c3.metric("Churned customers", f"{churn_n:,}")
c4.metric("High-balance segment churn", f"{high_value_churn:.1f}%")
st.caption("High-balance is defined dynamically as the top quartile of balances within the filtered view; this is a relative segment, not a bank-defined premium tier.")

tab1, tab2, tab3, tab4 = st.tabs(["Overview","Geography & demographics","Engagement & products","High-value explorer"])
with tab1:
    left,right = st.columns(2)
    with left:
        status = filtered["CustomerStatus"].value_counts().rename_axis("Status").reset_index(name="Customers")
        st.plotly_chart(px.pie(status, names="Status", values="Customers", hole=.45, title="Retained vs churned customers"), use_container_width=True)
    with right:
        geo_stats = filtered.groupby("Geography", observed=False).agg(Customers=("Exited","size"), Churn_Rate=("Exited","mean")).reset_index()
        geo_stats["Churn Rate (%)"] = geo_stats["Churn_Rate"]*100
        st.plotly_chart(px.bar(geo_stats, x="Geography", y="Churn Rate (%)", text_auto=".1f", title="Churn rate by geography"), use_container_width=True)
    st.dataframe(filtered.groupby("Geography", observed=False).agg(Customers=("CustomerId","count"), Churned=("Exited","sum"), Churn_Rate=("Exited","mean")).assign(Churn_Rate=lambda x:(x.Churn_Rate*100).round(2)).reset_index(), use_container_width=True)
with tab2:
    a,b = st.columns(2)
    age_stats = filtered.groupby("AgeGroup", observed=False).agg(Customers=("Exited","size"), Churn_Rate=("Exited","mean")).reset_index()
    age_stats["Churn Rate (%)"] = age_stats["Churn_Rate"]*100
    gender_stats = filtered.groupby("Gender", observed=False).agg(Customers=("Exited","size"), Churn_Rate=("Exited","mean")).reset_index()
    gender_stats["Churn Rate (%)"] = gender_stats["Churn_Rate"]*100
    a.plotly_chart(px.bar(age_stats, x="AgeGroup", y="Churn Rate (%)", text_auto=".1f", title="Churn rate by age group"), use_container_width=True)
    b.plotly_chart(px.bar(gender_stats, x="Gender", y="Churn Rate (%)", text_auto=".1f", title="Churn rate by gender"), use_container_width=True)
    st.plotly_chart(px.density_heatmap(filtered, x="Geography", y="AgeGroup", z="Exited", histfunc="avg", title="Geography × age: average churn indicator", color_continuous_scale="Blues"), use_container_width=True)
with tab3:
    a,b = st.columns(2)
    active_stats = filtered.groupby("IsActiveMember", observed=False).agg(Customers=("Exited","size"), Churn_Rate=("Exited","mean")).reset_index()
    active_stats["Activity"] = active_stats["IsActiveMember"].map({0:"Inactive",1:"Active"})
    active_stats["Churn Rate (%)"] = active_stats["Churn_Rate"]*100
    prod_stats = filtered.groupby("NumOfProducts", observed=False).agg(Customers=("Exited","size"), Churn_Rate=("Exited","mean")).reset_index()
    prod_stats["Churn Rate (%)"] = prod_stats["Churn_Rate"]*100
    a.plotly_chart(px.bar(active_stats, x="Activity", y="Churn Rate (%)", text_auto=".1f", title="Churn by activity status"), use_container_width=True)
    b.plotly_chart(px.bar(prod_stats, x="NumOfProducts", y="Churn Rate (%)", text_auto=".1f", title="Churn by number of products"), use_container_width=True)
    tenure_stats = filtered.groupby("TenureGroup", observed=False).agg(Customers=("Exited","size"), Churn_Rate=("Exited","mean")).reset_index()
    tenure_stats["Churn Rate (%)"] = tenure_stats["Churn_Rate"]*100
    st.plotly_chart(px.bar(tenure_stats, x="TenureGroup", y="Churn Rate (%)", text_auto=".1f", title="Churn by tenure group"), use_container_width=True)
with tab4:
    q = filtered["Balance"].quantile(.75)
    premium = filtered[filtered["Balance"] >= q].copy()
    st.write(f"Relative high-balance threshold in current view: **{q:,.2f}**")
    p1,p2,p3 = st.columns(3)
    p1.metric("High-balance customers", f"{len(premium):,}")
    p2.metric("Churned high-balance customers", f"{int(premium.Exited.sum()):,}")
    p3.metric("Average balance of churned customers", f"{filtered.loc[filtered.Exited==1,'Balance'].mean():,.2f}" if (filtered.Exited==1).any() else "N/A")
    if not premium.empty:
        premium_stats = premium.groupby("Geography", observed=False).agg(Customers=("Exited","size"), Churned=("Exited","sum"), Churn_Rate=("Exited","mean")).reset_index()
        premium_stats["Churn Rate (%)"] = premium_stats["Churn_Rate"]*100
        st.plotly_chart(px.bar(premium_stats, x="Geography", y="Churn Rate (%)", text_auto=".1f", title="High-balance churn by geography"), use_container_width=True)
    st.dataframe(premium.sort_values(["Exited","Balance"], ascending=[False,False])[["CustomerId","Geography","Age","Balance","EstimatedSalary","IsActiveMember","NumOfProducts","Exited"]], use_container_width=True)

st.divider()
st.subheader("Download filtered records")
st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"), file_name="filtered_customer_churn.csv", mime="text/csv")
with st.expander("Definitions and limitations"):
    st.markdown("""
    - **Churn rate:** mean of `Exited` × 100; `Exited=1` is churned.
    - **Geographic risk index:** geography churn rate divided by overall filtered churn rate × 100 (relative index; 100 means equal to overall).
    - **High-value proxy:** top-quartile balance within the current filtered sample. It is not a verified profitability measure.
    - Results are descriptive associations, not causal claims or a predictive model. Customer-level rows may be synthetic or sample data; validate provenance before external or policy use.
    """)
geo_risk = filtered.groupby("Geography", observed=False)["Exited"].mean() / filtered["Exited"].mean() * 100 if filtered["Exited"].mean() else None
if geo_risk is not None:
    with st.expander("Geographic Risk Index"):
        st.dataframe((geo_risk*1).rename("Risk Index (100 = filtered average)").round(1).reset_index())
