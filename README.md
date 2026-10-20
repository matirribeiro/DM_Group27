# DM_Group27

Data Mining 2026/27 project: customer segmentation for Amazing Creative Desk Coworking (ACDC).

## Setup

With conda (recommended, matches the course environment):

```
conda env create -f environment.yml
conda activate dm_group27
```

Or with pip (Python 3.12):

```
pip install -r requirements.txt
```

## Structure

```
data/acdc_dataset.csv   project dataset (separator ";")
data/acdc_clean.csv     cleaned dataset, produced by notebooks/drafts/eda_martim.ipynb
notebooks/              Jupyter notebooks (drafts/ holds each member's working notebook)
docs/                   planning documents
```

Load the cleaned data with:

```python
pd.read_csv("data/acdc_clean.csv", sep=";",
            parse_dates=["membership_start", "membership_end", "last_badge_swipe"])
```

An empty `membership_end` means the member is still active (data extracted on 2024-01-01).
