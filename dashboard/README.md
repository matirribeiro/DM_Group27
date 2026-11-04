# ACDC Members Dashboard

Interactive EDA dashboard built with Streamlit and Plotly on the cleaned dataset (`data/acdc_clean.csv`).

## How to run

1. Extract `Group27_EDA_Bonus_Code.zip`. The `dashboard` and `data` folders must stay side by side.
2. Install the dependencies:
   ```bash
   pip install -r dashboard/requirements.txt
   ```
3. From the extracted folder, start the app:
   ```bash
   streamlit run dashboard/app.py
   ```
   It opens in the browser (default http://localhost:8501). Stop it with `Ctrl+C`.

## What it shows

- **Sidebar filters:** plan tier, country, industry, account type (team / individual) and status (active / churned).
- **KPI row:** number of members, average lifetime value, average weekly visits and share of active members.
- **Distribution:** histogram of any numeric variable and a box plot by plan tier.
- **Category breakdown:** number of members per plan tier, country, industry or gender.
- **Member table:** drill-down table with selectable columns.

Two columns are created inside the app: `is_active` (empty `membership_end`) and `tenure_days` (days until the end date, or until the extraction date 2024-01-01 for active members).

## Bonus documentation

**Why we chose it.** The dashboard reuses the plots made in the descriptive analysis and makes them interactive, so the group and the instructors can explore segments without editing code.

**What it adds.** Filters make it quick to compare sub-populations (for example, one plan tier only, or churned vs active members), which supports the choice of variables and the expected number of clusters in Deliverable 2.

**Challenges.** Some filter combinations return no members, so the app shows a warning and stops instead of failing. The app lives outside the notebook so the notebook still runs in a fresh environment.