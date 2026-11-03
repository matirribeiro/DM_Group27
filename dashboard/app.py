from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "acdc_clean.csv"
EXTRACTION_DATE = pd.Timestamp("2024-01-01")
PLAN_ORDER = ["hot_desk", "flex", "full_time", "dedicated_desk", "private_office"]

st.set_page_config(page_title="ACDC Members Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_PATH,
        sep=";",
        parse_dates=["membership_start", "membership_end", "last_badge_swipe"],
    )
    df["is_active"] = df["membership_end"].isna()
    end = df["membership_end"].fillna(EXTRACTION_DATE)
    df["tenure_days"] = (end - df["membership_start"]).dt.days
    return df


df = load_data()

st.title("ACDC Members Dashboard")
st.write(f"Loaded {len(df):,} members and {df.shape[1]} columns.")

#Sidebar filters
st.sidebar.header("Filters")

plans = st.sidebar.multiselect("Plan tier", PLAN_ORDER, default=PLAN_ORDER)

country_options = sorted(df["country"].unique())
countries = st.sidebar.multiselect("Country", country_options, default=country_options)

industry_options = sorted(df["industry"].unique())
industries = st.sidebar.multiselect("Industry", industry_options, default=industry_options)

account = st.sidebar.selectbox("Account type", ["All", "Team", "Individual"])
status = st.sidebar.selectbox("Status", ["All", "Active", "Churned"])

#Apply the filters
mask = (
    df["plan_tier"].isin(plans)
    & df["country"].isin(countries)
    & df["industry"].isin(industries)
)

if account == "Team":
    mask = mask & df["is_team_account"]
elif account == "Individual":
    mask = mask & ~df["is_team_account"]

if status == "Active":
    mask = mask & df["is_active"]
elif status == "Churned":
    mask = mask & ~df["is_active"]

filtered = df[mask]

st.sidebar.write(f"{len(filtered):,} of {len(df):,} members selected")

if filtered.empty:
    st.warning("No members match these filters. Widen the selection on the left.")
    st.stop()

#KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("Members", f"{len(filtered):,}")
k2.metric("Average LTV", f"{filtered['lifetime_value'].mean():,.0f} €")
k3.metric("Avg weekly visits", f"{filtered['avg_weekly_visits'].mean():.2f}")
k4.metric("Active share", f"{filtered['is_active'].mean():.1%}")

#Distribution of any variable
st.subheader("Distribution")

numeric_cols = filtered.select_dtypes(include="number").columns.tolist()
var = st.selectbox("Choose a variable", numeric_cols, index=numeric_cols.index("age"))

col_a, col_b = st.columns(2)

fig_hist = px.histogram(filtered, x=var, nbins=40, title=f"Histogram of {var}")
col_a.plotly_chart(fig_hist, width="stretch")

fig_box = px.box(
    filtered, x="plan_tier", y=var,
    category_orders={"plan_tier": PLAN_ORDER},
    title=f"{var} by plan tier",
)
col_b.plotly_chart(fig_box, width="stretch")

#Category breakdown
st.subheader("Category breakdown")

cat = st.selectbox("Choose a category", ["plan_tier", "country", "industry", "gender"])

counts = filtered[cat].astype(str).value_counts().reset_index()
counts.columns = [cat, "members"]

fig_cat = px.bar(counts, x=cat, y="members", title=f"Members by {cat}")
st.plotly_chart(fig_cat, width="stretch")

#Member table
st.subheader("Member table")

default_cols = [
    "member_id", "plan_tier", "country", "industry", "age",
    "tenure_days", "total_visits", "lifetime_value",
]
shown = st.multiselect("Columns to show", list(filtered.columns), default=default_cols)

st.dataframe(filtered[shown])